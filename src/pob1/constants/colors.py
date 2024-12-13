"""
Color constants and color-related functionality for Path of Building.

This module contains all the color codes used throughout the application for
consistent styling and visual feedback.
"""
from enum import Enum
from typing import Dict, Optional, Tuple

from pydantic import BaseModel, field_validator


class ColorCode(str, Enum):
    """Color code identifiers used throughout the application."""
    NORMAL = "NORMAL"
    MAGIC = "MAGIC"
    RARE = "RARE"
    UNIQUE = "UNIQUE"
    RELIC = "RELIC"
    GEM = "GEM"
    PROPHECY = "PROPHECY"
    CURRENCY = "CURRENCY"
    CRAFTED = "CRAFTED"
    CUSTOM = "CUSTOM"
    SOURCE = "SOURCE"
    UNSUPPORTED = "UNSUPPORTED"
    WARNING = "WARNING"
    TIP = "TIP"
    FIRE = "FIRE"
    COLD = "COLD"
    LIGHTNING = "LIGHTNING"
    CHAOS = "CHAOS"
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    HIGHLIGHT = "HIGHLIGHT"
    OFFENCE = "OFFENCE"
    DEFENCE = "DEFENCE"
    # Character classes
    SCION = "SCION"
    MARAUDER = "MARAUDER"
    RANGER = "RANGER"
    WITCH = "WITCH"
    DUELIST = "DUELIST"
    TEMPLAR = "TEMPLAR"
    SHADOW = "SHADOW"
    # Equipment slots
    MAINHAND = "MAINHAND"
    MAINHANDBG = "MAINHANDBG"
    OFFHAND = "OFFHAND"
    OFFHANDBG = "OFFHANDBG"
    # Influence types
    SHAPER = "SHAPER"
    ELDER = "ELDER"
    FRACTURED = "FRACTURED"
    ADJUDICATOR = "ADJUDICATOR"
    BASILISK = "BASILISK"
    CRUSADER = "CRUSADER"
    EYRIE = "EYRIE"
    # Status effects
    CLEANSING = "CLEANSING"
    TANGLE = "TANGLE"
    CHILLBG = "CHILLBG"
    FREEZEBG = "FREEZEBG"
    SHOCKBG = "SHOCKBG"
    SCORCHBG = "SCORCHBG"
    BRITTLEBG = "BRITTLEBG"
    SAPBG = "SAPBG"
    # Other
    SCOURGE = "SCOURGE"
    CRUCIBLE = "CRUCIBLE"


class ColorCodes(BaseModel):
    """
    Container for all color codes used in the application.
    Uses Pydantic for validation and type safety.
    """
    codes: Dict[str, str]
    rgb_highlight: Optional[Tuple[float, float, float]] = None

    def __init__(self):
        """Initialize with default color values."""
        super().__init__(codes={
            ColorCode.NORMAL: "^xC8C8C8",
            ColorCode.MAGIC: "^x8888FF",
            ColorCode.RARE: "^xFFFF77",
            ColorCode.UNIQUE: "^xAF6025",
            ColorCode.RELIC: "^x60C060",
            ColorCode.GEM: "^x1AA29B",
            ColorCode.PROPHECY: "^xB54BFF",
            ColorCode.CURRENCY: "^xAA9E82",
            ColorCode.CRAFTED: "^xB8DAF1",
            ColorCode.CUSTOM: "^x5CF0BB",
            ColorCode.SOURCE: "^x88FFFF",
            ColorCode.UNSUPPORTED: "^xF05050",
            ColorCode.WARNING: "^xFF9922",
            ColorCode.TIP: "^x80A080",
            ColorCode.FIRE: "^xB97123",
            ColorCode.COLD: "^x3F6DB3",
            ColorCode.LIGHTNING: "^xADAA47",
            ColorCode.CHAOS: "^xD02090",
            ColorCode.POSITIVE: "^x33FF77",
            ColorCode.NEGATIVE: "^xDD0022",
            ColorCode.HIGHLIGHT: "^xFF0000",
            ColorCode.OFFENCE: "^xE07030",
            ColorCode.DEFENCE: "^x8080E0",
            # Character classes
            ColorCode.SCION: "^xFFF0F0",
            ColorCode.MARAUDER: "^xE05030",
            ColorCode.RANGER: "^x70FF70",
            ColorCode.WITCH: "^x7070FF",
            ColorCode.DUELIST: "^xE0E070",
            ColorCode.TEMPLAR: "^xC040FF",
            ColorCode.SHADOW: "^x30C0D0",
            # Equipment slots
            ColorCode.MAINHAND: "^x50FF50",
            ColorCode.MAINHANDBG: "^x071907",
            ColorCode.OFFHAND: "^xB7B7FF",
            ColorCode.OFFHANDBG: "^x070719",
            # Influence types
            ColorCode.SHAPER: "^x55BBFF",
            ColorCode.ELDER: "^xAA77CC",
            ColorCode.FRACTURED: "^xA29160",
            ColorCode.ADJUDICATOR: "^xE9F831",
            ColorCode.BASILISK: "^x00CB3A",
            ColorCode.CRUSADER: "^x2946FC",
            ColorCode.EYRIE: "^xAAB7B8",
            # Status effects
            ColorCode.CLEANSING: "^xF24141",
            ColorCode.TANGLE: "^x038C8C",
            ColorCode.CHILLBG: "^x151e26",
            ColorCode.FREEZEBG: "^x0c262b",
            ColorCode.SHOCKBG: "^x191732",
            ColorCode.SCORCHBG: "^x270b00",
            ColorCode.BRITTLEBG: "^x00122b",
            ColorCode.SAPBG: "^x261500",
            # Other
            ColorCode.SCOURGE: "^xFF6E25",
            ColorCode.CRUCIBLE: "^xFFA500"
        })

        # Add derived color codes
        derived_mappings = {
            "STRENGTH": ColorCode.MARAUDER,
            "DEXTERITY": ColorCode.RANGER,
            "INTELLIGENCE": ColorCode.WITCH,
            "LIFE": ColorCode.MARAUDER,
            "MANA": ColorCode.WITCH,
            "ES": ColorCode.SOURCE,
            "WARD": ColorCode.RARE,
            "ARMOUR": ColorCode.NORMAL,
            "EVASION": ColorCode.POSITIVE,
            "RAGE": ColorCode.WARNING,
            "PHYS": ColorCode.NORMAL
        }
        
        # Assert and add derived colors
        for derived, base in derived_mappings.items():
            assert base in self.codes, f"Base color {base} not found for derived color {derived}"
            self.codes[derived] = self.codes[base]
    
    @field_validator('codes')
    def validate_color_codes(cls, codes: Dict[str, str]) -> Dict[str, str]:
        """Validate all color codes follow the correct format."""
        for code_name, color_value in codes.items():
            # Assert color codes start with the prefix
            assert color_value.startswith("^x"), f"Color code {code_name} must start with '^x'"
            # Assert color codes are the correct length (prefix + 6 hex chars)
            assert len(color_value) == 8, f"Color code {code_name} must be 8 characters (^x + 6 hex)"
            # Assert the hex portion contains valid hex characters
            hex_part = color_value[2:]
            assert all(c in "0123456789ABCDEFabcdef" for c in hex_part), \
                f"Color code {code_name} contains invalid hex characters"
        return codes

    @field_validator('rgb_highlight')
    def validate_rgb_values(cls, rgb: Optional[Tuple[float, float, float]]) -> Optional[Tuple[float, float, float]]:
        """Validate RGB values are within the correct range."""
        if rgb is not None:
            for component in rgb:
                assert 0 <= component <= 1, f"RGB value {component} must be between 0 and 1"
        return rgb

    def update_color_code(self, code: str, color: str) -> None:
            """Update a specific color code."""
            # Pre-condition assertions
            assert code in self.codes, f"Invalid color code: {code}"
            assert color.startswith(("^", "0", "#")), f"Invalid color format: {color}"
            
            # Clean the color value
            color = color.replace("^0", "^")
            if color.startswith(("0", "#")):
                color = f"^x{color.replace('0x', '').replace('#', '')}"
            
            # Post-condition assertions
            assert len(color) == 8, f"Invalid color length after processing: {color}"
            assert color.startswith("^x"), f"Invalid color prefix after processing: {color}"
            
            self.codes[code] = color
            if code == ColorCode.HIGHLIGHT:
                self.rgb_highlight = self.hex_to_rgb(color)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Optional[Tuple[float, float, float]]:
        """Convert a hex color string to RGB values."""
        # Pre-condition assertions
        assert isinstance(hex_color, str), f"Expected string, got {type(hex_color)}"
        
        hex_color = hex_color.replace("0x", "").replace("#", "")
        if len(hex_color) != 6:
            return None
            
        try:
            rgb_values = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
            # Post-condition assertions
            assert len(rgb_values) == 3, "RGB conversion failed to produce 3 values"
            assert all(0 <= v <= 1 for v in rgb_values), "RGB values out of range"
            return rgb_values  # type: ignore[return-value] # Tuple[float, float, float]
        except ValueError:
            return None


# Global instance
COLOR_CODES = ColorCodes()
DEFAULT_COLOR_CODES = ColorCodes()  # For reset capability

# Verify global instances are properly initialized
assert COLOR_CODES.codes == DEFAULT_COLOR_CODES.codes, "Default and active color codes should match on initialization"
assert all(code in COLOR_CODES.codes for code in ColorCode), "Missing color codes in global instance"