"""Pydantic model for the input of `postahc.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    prefix: str = Field(
        "pwscf",
        description=(
            "Prepended to input/output filenames; must be the same used in the calculation of "
            "unperturbed system."
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR environment variable is set",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "current directory ('./')"},
            ],
        },
        description=(
            "Directory containing input, output, and scratch files; must be the same as specified "
            "in the calculation of the unperturbed system."
        ),
    )
    ahc_dir: str | None = Field(None, description="Directory where the binary files are located.")
    use_irr_q: bool = Field(
        False,
        description=(
            "If .true., assume that the q points are on the irreducible grid. In this case, the "
            "data in ahc_dir must have been actually generated from a calculation on an "
            "irreducible q grid. Off-diagonal self-energies cannot be computed if use_irr_q = "
            ".true."
        ),
    )
    ahc_nbnd: int | None = Field(
        None,
        description=(
            "Number of bands for which the electron self-energy is to be computed. Must be "
            "identical to ahc_nbnd of the ph.x run with electron_phonon='ahc'."
        ),
    )
    ahc_nbndskip: int = Field(
        0,
        description=(
            "Number of bands to exclude when computing the self-energy. Must be identical to "
            "ahc_nbndskip of the ph.x run with electron_phonon='ahc'."
        ),
    )
    flvec: str | None = Field(
        None, description="File containing the normalized phonon displacements written by matdyn.x."
    )
    eta_eV: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(  # noqa: N815
        None,
        description=(
            "Magnitude of the small imaginary component included to smooth the energy denominators."
        ),
    )
    temp_kelvin: Annotated[float | None, Quantity(units="K", dimensionality="temperature")] = Field(
        None, description="Temperature at which the electron self-energy is calculated."
    )
    efermi_eV: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(  # noqa: N815
        None, description="Fermi energy of the electrons."
    )
    ahc_win_min_eV: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(  # noqa: N815
        -1.0e8, description="Lower bound of active AHC window for the lower Fan term."
    )
    ahc_win_max_eV: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(  # noqa: N815
        1.0e8, description="Upper bound of active AHC window for the lower Fan term."
    )
    skip_upper: bool = Field(
        False,
        description=(
            "If .true., skip calculation of the upper Fan self-energy. Also, truncate the "
            "Debye-Waller self-energy to include only the low-energy band contribution. "
            "(Corresponds to the second term (lower Fan + lower DW) of Eq. (G1-revised) of J.-M. "
            "Lihm and C.-H. Park, PRX 12, 039901(E) (2022).) If .false., calculate the "
            "contribution of both the high-energy and low-energy bands. In this case, "
            "ahc_upfan_iq#.bin files must be present in ahc_dir."
        ),
    )
    skip_dw: bool = Field(
        False,
        description=(
            "If .true., skip calculation of the Debye-Waller self-energy. If .false., ahc_dw.bin "
            "file must be present in ahc_dir."
        ),
    )
    adiabatic: bool = Field(
        False,
        description=(
            "If .true., use the adiabatic approximation when computing the Fan self-energy by "
            "ignoring the phonon frequency in the denominator. This approximation is known to be "
            "inaccurate and even divergent in some materials (S. PoncÃ© et al., J. Chem. Phys. "
            "143, 102813 (2015)). Therefore, this keyword should be used only for experimental or "
            "debugging purposes."
        ),
    )
    amass_amu: Annotated[list[float] | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None, description="Mass for each atom type. (start = 1, end = ntyp)"
    )


class POSTAHCEspressoInput(EspressoInput):
    """Pydantic model for the input of `postahc.x`."""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
