"""Fetch the .def files from the QE GitLab repo."""

import base64
import os
import shutil
import warnings
from collections.abc import Iterable

from pathlib import Path
import gitlab
from gitlab.v4.objects import Project, ProjectCommit, ProjectTag

from pydantic_espresso.def_files import directory as def_directory


OWNER = "QEF"
REPO = "q-e"
TOKEN = os.getenv("GITLAB_TOKEN")
URL = os.getenv("GITLAB_URL", "https://gitlab.com")


def create_gitlab_session(token: str | None = None, url: str = "https://gitlab.com") -> gitlab.Gitlab:
    """Create a GitLab session with optional authentication."""
    if token is None:
        gl = gitlab.Gitlab(url)
    else:
        gl = gitlab.Gitlab(url, private_token=token)
    gl.auth()
    return gl


def download_file(
    project: Project,
    ref: str,
    file_path: str,
    folder: str
) -> None:
    """Download a specific file from a given GitLab repository at a specified tag."""
    print(f"Downloading {file_path} from {ref}...")

    # Fetch the file content
    file_content = project.files.get(file_path=file_path, ref=ref)

    # Create the directory (skip already-fetched commits)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if file_content:
        decoded_content = base64.b64decode(file_content.content)
        with open(folder / Path(file_path).name, "wb") as f:
            f.write(decoded_content)


def fetch_defs(project, ref, folder):
    # First, try to get the xsl file
    try:
        file = project.files.get(file_path="dev-tools/input_xx.xsl", ref=ref)
        download_file(project, ref, file.file_path, folder)
    except gitlab.exceptions.GitlabGetError:
        # Without an xsl file, we cannot convert the def files to XML
        print("No xsl file found for {ref}. Skipping...")
        return

    for file in project.repository_tree(ref=ref, recursive=True, get_all=True, iterator=True):
        if file['path'].endswith(".def"):
            # Download the file
            download_file(project, ref, file['path'], folder)



def fetch_all_defs() -> None:
    """Fetch the def files from the Wannier90 GitLab repo."""
    # Create a GitLab session
    session = create_gitlab_session(token=TOKEN)
    project: Project = session.projects.get(f"{OWNER}/{REPO}")

    # Download *.def files for the latest commit
    latest_commit = project.commits.list(ref=project.default_branch, per_page=1, get_all=False)[0]
    fetch_defs(project, ref=latest_commit.id, folder = def_directory / latest_commit.id[:7])

    # Download all *.def files for all tags
    for tag in project.tags.list(get_all=True):
        # Find all *.def files in the tag
        fetch_defs(project, ref=tag.name, folder=def_directory / tag.name)

    # Copy the latest commit to the folder "latest"
    src = def_directory / latest_commit.id[:7]
    dst = def_directory / "latest"
    if dst.exists():
        # Remove the existing folder
        shutil.rmtree(dst)
    shutil.copy(src, dst)
