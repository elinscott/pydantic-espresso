"""Pydantic model for the card in `pw.x` input files."""

prebuilt_cards = {
    "k_points": {
        "type": "KPointsCard",
        "default": 'Field(discriminator="kind")',
        "import_str": "from pydantic_espresso.card.pw.k_points import KPointsCard",
    }
}
