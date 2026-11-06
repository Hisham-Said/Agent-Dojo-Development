"""
Defense registry — maps defense names to classes.
"""

from defenses.no_defense import NoDefense
from defenses.delimiter import DelimiterDefense
from defenses.detector import DetectorDefense


DEFENSES = {
    "no_defense": NoDefense,
    "delimiter": DelimiterDefense,
    "detector": DetectorDefense,
}


def create_defense(name):
    """Instantiate a defense by name."""
    cls = DEFENSES.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown defense: {name}. "
            f"Available: {list(DEFENSES.keys())}"
        )
    return cls()

