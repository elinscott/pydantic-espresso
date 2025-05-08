"""Pre-built pydantic models for Quantum ESPRESSO input cards."""

def cards_to_import(program: str, found_cards: list[str] = []) -> list[str]:

    # Attempt to import the cards for the given program from the submodule of the same name
    try:
        module = __import__(f".{program}", fromlist=[""])
        implemented_cards = getattr(module, "implemented_cards")
    except ImportError:
        implemented_cards = {}

    if found_cards:
        # If found_cards is not empty, filter the implemented cards
        cards = [card for card in implemented_cards if card in found_cards]
    else:
        # If found_cards is empty, use all implemented cards
        cards = implemented_cards

    return cards