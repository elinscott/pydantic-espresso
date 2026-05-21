"""Pydantic model for the input of `band_interpolation.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from textwrap import dedent
from typing import Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist


class InterpolationNamelist(Namelist):
    """Pydantic model for the `INTERPOLATION` namelist."""

    method: Literal["fourier-diff", "fourier", "idw", "idw-sphere"] = Field(
        "fourier-diff",
        description=dedent(
            """\
            The interpolation method to be used Available options are:
            - 'fourier-diff': band energies, as functions of k, are expanded in reciprocal space
              using a Star function basis set (algorithm from Pickett W. E., Krakauer H., Allen P.
              B., Phys. Rev. B, vol. 38, issue 4, page 2721, 1988,
              https://link.aps.org/doi/10.1103/PhysRevB.38.2721 ). WARNING: The pwscf.xml file must
              be generated with nosym == .false. .
            - 'fourier': band energies, as functions of k, are expanded in reciprocal space using a
              Star function basis set (algorithm from D. D. Koelling, J. H. Wood, J. Comput. Phys.,
              67, 253-262 (1986). https://ui.adsabs.harvard.edu/abs/1986JCoPh..67..253K ). WARNING:
              The pwscf.xml file must be generated with nosym == .false. .
            - 'idw': inverse distance weighting interpolation with Shepard metric (ACM 68:
              Proceedings of the 1968 23rd ACM national conference, January 1968, Pages 517â524,
              https://doi.org/10.1145/800186.810616 ). WARNING: The pwscf.xml file must be
              generated with nosym == .true. . WARNING: This method is REALLY simple and provides
              only a very rough estimate of the band structure.
            - 'idw-sphere': inverse distance weighting interpolation inside a sphere of given
              radius. WARNING: The pwscf.xml file must be generated with nosym == .true. . WARNING:
              This method is REALLY simple and provides only a very rough estimate of the band
              structure."""
        ),
    )
    miller_max: int = Field(
        6,
        description=dedent(
            """\
            The maximum Miller index used to automatically generate the set of symmetry
            inequivalent Star vectors (only for method == 'fourier-diff' or 'fourier')"""
        ),
    )
    check_periodicity: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. a (time consuming) step is performed, to check whether all the Star functions
            have the correct lattice periodicity (only for method == 'fourier-diff' or 'fourier') .
             For automatically generated Star functions this should never occur by construction,
            and the program will stop and exit in case one Star function with wrong periodicity is
            found (useful for debugging and program sanity check).  If additional user-defined Star
            vectors are specified (see optional card USER_STARS), the program will print a WARNING
            in case one Star function with wrong periodicity is found."""
        ),
    )
    p_metric: int = Field(
        2,
        description=dedent(
            """\
            The exponent of the distance in the IDW method ( only for method == 'idw' or
            'idw-sphere')"""
        ),
    )
    scale_sphere: float = Field(
        4.0e0,
        description=dedent(
            """\
            The search radius for method == 'idw-sphere', is Rmin * scale_sphere, where Rmin is the
            minimum distance found between the uniform grid of k-points.  If scale_sphere is too
            small, some k-points of the path might not see enough uniform grid points to average
            energies, whereas for large values the method becomes equal to method == 'idw'."""
        ),
    )


class BANDINTERPOLATIONEspressoInput(EspressoInput):
    """Pydantic model for the input of `band_interpolation.x`."""

    interpolation: InterpolationNamelist = Field(default_factory=lambda: InterpolationNamelist())
