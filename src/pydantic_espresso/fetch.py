"""Fetch the .def files from the QE GitLab repo."""

import base64
import os
import warnings
from pathlib import Path

import gitlab
from gitlab.v4.objects import Project, ProjectCommit
from packaging.version import Version

from pydantic_espresso.def_files import directory as def_directory

OWNER = "QEF"
REPO = "q-e"
TOKEN = os.getenv("GITLAB_TOKEN")
URL = os.getenv("GITLAB_URL", "https://gitlab.com")


def create_gitlab_session(
    token: str | None = None, url: str = "https://gitlab.com"
) -> gitlab.Gitlab:
    """Create a GitLab session with optional authentication."""
    if token is None:
        gl = gitlab.Gitlab(url)
    else:
        gl = gitlab.Gitlab(url, private_token=token)
    gl.auth()
    return gl


def download_file(project: Project, ref: str, file_path: str, folder: Path) -> None:
    """Download a specific file from a given GitLab repository at a specified tag."""
    # Fetch the file content
    file_content = project.files.get(file_path=file_path, ref=ref)

    # Create the directory (skip already-fetched commits)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if file_content:
        decoded_content = base64.b64decode(file_content.content)
        with open(folder / Path(file_path).name, "wb") as f:
            f.write(decoded_content)


def fetch_defs(project: Project, ref: str, folder: Path) -> None:
    """Fetch the xsl and def files for a particular commit or tag from the GitLab repo."""
    # First, try to get the xsl file
    try:
        xsl_file = project.files.get(file_path="dev-tools/input_xx.xsl", ref=ref)
        download_file(project, ref, xsl_file.file_path, folder)
    except gitlab.exceptions.GitlabGetError:
        # Without an xsl file, we cannot convert the def files to XML
        warnings.warn(f"No xsl file found for {ref}. Skipping...", stacklevel=2)
        return

    for file in project.repository_tree(ref=ref, recursive=True, get_all=True, iterator=True):
        if not isinstance(file, dict):
            raise TypeError("Expected a dictionary for the file object.")
        if "path" not in file:
            raise KeyError("Expected 'path' key in the file dictionary.")
        if file["path"].endswith(".def"):
            # Download the file
            download_file(project, ref, file["path"], folder)


def fetch_all_defs() -> None:
    """Fetch the def files from the Wannier90 GitLab repo."""
    # Create a GitLab session
    session = create_gitlab_session(token=TOKEN)
    project: Project = session.projects.get(f"{OWNER}/{REPO}")

    # Download *.def files for the latest commit
    commit_list = project.commits.list(ref=project.default_branch, per_page=1, get_all=False)
    if isinstance(commit_list, list):
        latest_commit = commit_list[0]
    else:
        latest_commit = commit_list.next()
    if not isinstance(latest_commit, ProjectCommit):
        raise TypeError("Expected a ProjectCommit object.")
    fetch_defs(project, ref=latest_commit.id, folder=def_directory / "develop")

    # Download all *.def files for all tags with clean version numbering
    for tag in project.tags.list(get_all=True):
        try:
            # Check that we can convert the tag to a Version object
            version = Version(tag.name[3:])
        except ValueError:
            continue
        if version.is_devrelease:
            continue
        existing_tags = [t.name for t in def_directory.iterdir() if t.is_dir()]
        if tag.name not in existing_tags:
            # Find all *.def files in the tag
            fetch_defs(project, ref=tag.name, folder=def_directory / tag.name)
