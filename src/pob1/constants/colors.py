"""
Color constants and color-related functionality for Path of Building.

This module contains all the color codes used throughout the application for
consistent styling and visual feedback.
"""
from enum import Enum
from typing import Dict, Optional, Tuple

from pydantic import BaseModel


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
            # ... (remaining color codes)
        })

        # Add derived color codes
        self.codes["STRENGTH"] = self.codes[ColorCode.MARAUDER]
        self.codes["DEXTERITY"] = self.codes[ColorCode.RANGER]
        self.codes["INTELLIGENCE"] = self.codes[ColorCode.WITCH]
        
        self.codes["LIFE"] = self.codes[ColorCode.MARAUDER]
        self.codes["MANA"] = self.codes[ColorCode.WITCH]
        self.codes["ES"] = self.codes[ColorCode.SOURCE]
        self.codes["WARD"] = self.codes[ColorCode.RARE]
        self.codes["ARMOUR"] = self.codes[ColorCode.NORMAL]
        self.codes["EVASION"] = self.codes[ColorCode.POSITIVE]
        self.codes["RAGE"] = self.codes[ColorCode.WARNING]
        self.codes["PHYS"] = self.codes[ColorCode.NORMAL]

    def update_color_code(self, code: str, color: str) -> None:
        """
        Update a specific color code.
        
        Args:
            code: The color code to update
            color: The new color value
            
        Note:
            Updates the RGB highlight color if the HIGHLIGHT code is modified
        """
        if code in self.codes:
            color = color.replace("^0", "^")
            self.codes[code] = color
            if code == ColorCode.HIGHLIGHT:
                self.rgb_highlight = self.hex_to_rgb(color)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Optional[Tuple[float, float, float]]:
        """
        Convert a hex color string to RGB values.
        
        Args:
            hex_color: Hex color string (with or without 0x/# prefix)
            
        Returns:
            Tuple of RGB values normalized to 0-1 range, or None if invalid
        """
        hex_color = hex_color.replace("0x", "").replace("#", "")
        if len(hex_color) != 6:
            return None
            
        try:
            r = int(hex_color[0:2], 16) / 255
            g = int(hex_color[2:4], 16) / 255
            b = int(hex_color[4:6], 16) / 255
            return (r, g, b)
        except ValueError:
            return None


# Global instance
COLOR_CODES = ColorCodes()
DEFAULT_COLOR_CODES = ColorCodes()  # For reset capability