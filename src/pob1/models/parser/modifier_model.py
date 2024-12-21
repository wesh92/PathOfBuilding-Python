from typing import Optional, List, Tuple
from pydantic import BaseModel, Field, validator
from enum import Enum
import re

class ModifierForm(Enum):
    """
    Enum representing the different forms a modifier can take.
    Copied from previous implementation for reference.
    """
    BASE = "BASE"
    INCREASE = "INC"
    REDUCE = "RED"
    MORE = "MORE"
    LESS = "LESS"
    GAIN = "GAIN"
    LOSE = "LOSE"
    GRANTS = "GRANTS"
    REMOVES = "REMOVES"
    CHANCE = "CHANCE"
    FLAG = "FLAG"
    TOTAL_COST = "TOTALCOST"
    BASE_COST = "BASECOST"
    PENETRATION = "PEN"
    DAMAGE = "DMG"
    DAMAGE_ATTACKS = "DMGATTACKS"
    DAMAGE_SPELLS = "DMGSPELLS"
    DAMAGE_BOTH = "DMGBOTH"
    REGEN_FLAT = "REGENFLAT"
    REGEN_PERCENT = "REGENPERCENT"
    DEGEN_FLAT = "DEGENFLAT"
    DEGEN_PERCENT = "DEGENPERCENT"
    DEGEN = "DEGEN"
    OVERRIDE = "OVERRIDE"

class ModifierPattern(BaseModel):
    """
    Represents a single modifier pattern and its form.
    """
    pattern: str = Field(..., description="The regular expression pattern to match")
    form: ModifierForm = Field(..., description="The form this pattern corresponds to")
    
    @validator('pattern')
    def validate_pattern(cls, v: str) -> str:
        """
        Validates that the pattern is a valid regular expression and
        converts Lua pattern syntax to Python regex syntax.
        """
        # Convert Lua pattern syntax to Python regex syntax
        pattern = (v
            .replace("%d", "\\d")
            .replace("%a", "[a-zA-Z]")
            .replace("%+", "\\+")
            .replace("%-", "\\-")
            .replace("%.", "\\.")
            .replace("%?", "\\?")
            .replace("%s", "\\s")
            .replace("%%", "%")
        )
        
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regular expression pattern: {e}")
        return pattern

    def match(self, text: str) -> Optional[List[str]]:
        """
        Attempts to match the given text against this pattern.
        
        Args:
            text: The text to match against the pattern
            
        Returns:
            Optional[List[str]]: List of captured groups if matched, None otherwise
        """
        match = re.match(self.pattern, text)
        if match:
            return list(match.groups())
        return None

class ModifierType(BaseModel):
    """
    Base class for different types of modifiers.
    Each subclass represents a specific modifier structure.
    """
    text: str = Field(..., description="The original modifier text")
    form: ModifierForm = Field(..., description="The form of this modifier")

class NumericModifier(ModifierType):
    """
    Represents modifiers that have a single numeric value.
    Examples: "50% increased", "+10% to"
    """
    value: float = Field(..., description="The numeric value of the modifier")

class DamageModifier(ModifierType):
    """
    Represents damage range modifiers.
    Examples: "adds 1 to 10 physical damage"
    """
    min_damage: float = Field(..., description="Minimum damage value")
    max_damage: float = Field(..., description="Maximum damage value")
    damage_type: str = Field(..., description="Type of damage")

class RegenerationModifier(ModifierType):
    """
    Represents regeneration/degeneration modifiers.
    Examples: "2.5 life regenerated per second"
    """
    value: float = Field(..., description="The regeneration/degeneration value")
    resource: str = Field(..., description="The resource being regenerated/degenerated")

class ModifierManager:
    """
    Manages the collection of modifier patterns and handles parsing modifier strings.
    """
    def __init__(self):
        self.patterns: List[ModifierPattern] = []
        
    def add_pattern(self, pattern: str, form: ModifierForm) -> None:
        """
        Adds a new modifier pattern to the manager.
        
        Args:
            pattern: The pattern string (in Lua pattern syntax)
            form: The ModifierForm this pattern corresponds to
        """
        self.patterns.append(ModifierPattern(pattern=pattern, form=form))
        
    def parse_modifier(self, text: str) -> Optional[ModifierType]:
        """
        Attempts to parse a modifier string into a structured modifier object.
        
        Args:
            text: The modifier text to parse
            
        Returns:
            Optional[ModifierType]: A modifier object if successfully parsed, None otherwise
        """
        for pattern in self.patterns:
            if matches := pattern.match(text):
                # Handle different forms with their specific structures
                if pattern.form in {ModifierForm.DAMAGE, ModifierForm.DAMAGE_ATTACKS, 
                                  ModifierForm.DAMAGE_SPELLS, ModifierForm.DAMAGE_BOTH}:
                    return DamageModifier(
                        text=text,
                        form=pattern.form,
                        min_damage=float(matches[0]),
                        max_damage=float(matches[1]),
                        damage_type=matches[2]
                    )
                elif pattern.form in {ModifierForm.REGEN_FLAT, ModifierForm.REGEN_PERCENT,
                                    ModifierForm.DEGEN_FLAT, ModifierForm.DEGEN_PERCENT}:
                    return RegenerationModifier(
                        text=text,
                        form=pattern.form,
                        value=float(matches[0]),
                        resource=matches[1]
                    )
                else:
                    # Default to numeric modifier for simple cases
                    return NumericModifier(
                        text=text,
                        form=pattern.form,
                        value=float(matches[0]) if matches else 0
                    )
        return None

def create_modifier_manager() -> ModifierManager:
    """Creates and initializes a ModifierManager with predefined modifier patterns.

    Creates a new ModifierManager instance and initializes it with all known modifier
    patterns converted from the original Lua patterns. It handles various types of
    modifiers including damage, regeneration, percentage-based modifiers, and status
    flags.

    :return: A fully initialized manager ready to parse modifier strings
    :rtype: ModifierManager

    :Example:

    Basic usage with different types of modifiers::

        modifiers = create_modifier_manager()

        # Parse a simple numeric modifier
        result = modifiers.parse_modifier("50% increased")
        assert isinstance(result, NumericModifier)
        assert result.value == 50
        assert result.form == ModifierForm.INCREASE

        # Parse a damage modifier
        damage_mod = modifiers.parse_modifier("adds 5 to 10 fire damage")
        assert isinstance(damage_mod, DamageModifier)
        assert damage_mod.min_damage == 5
        assert damage_mod.max_damage == 10
        assert damage_mod.damage_type == "fire"

        # Parse a regeneration modifier
        regen_mod = modifiers.parse_modifier("2.5 mana regenerated per second")
        assert isinstance(regen_mod, RegenerationModifier)
        assert regen_mod.value == 2.5
        assert regen_mod.resource == "mana"

        # Handle an unknown modifier
        unknown = modifiers.parse_modifier("some invalid modifier")
        assert unknown is None

    .. note::
        The pattern matching is case-sensitive and requires exact matches based on
        the predefined patterns. Make sure your modifier strings match the expected
        format exactly.
    """
    manager = ModifierManager()
    
    # Add patterns from the Lua formList
    patterns = {
        # Basic increases and reductions
        "^(\\d+)% increased": ModifierForm.INCREASE,
        "^(\\d+)% faster": ModifierForm.INCREASE,
        "^(\\d+)% reduced": ModifierForm.REDUCE,
        "^(\\d+)% slower": ModifierForm.REDUCE,
        "^(\\d+)% more": ModifierForm.MORE,
        "^(\\d+)% less": ModifierForm.LESS,
        
        # Base value modifications
        "^([\\+\\-][\\d\\.]+)%?": ModifierForm.BASE,
        "^([\\+\\-][\\d\\.]+)%? to": ModifierForm.BASE,
        "^([\\+\\-]?[\\d\\.]+)%? of": ModifierForm.BASE,
        "^([\\+\\-][\\d\\.]+)%? base": ModifierForm.BASE,
        "^([\\+\\-]?[\\d\\.]+)%? additional": ModifierForm.BASE,
        "(\\d+) additional hits?": ModifierForm.BASE,
        "^throw up to (\\d+)": ModifierForm.BASE,
        
        # Gain and lose modifiers
        "^you gain ([\\d\\.]+)": ModifierForm.GAIN,
        "^gains? ([\\d\\.]+)%? of": ModifierForm.GAIN,
        "^gain ([\\d\\.]+)": ModifierForm.GAIN,
        "^gain \\+(\\d+)% to": ModifierForm.GAIN,
        "^you lose ([\\d\\.]+)": ModifierForm.LOSE,
        "^loses? ([\\d\\.]+)% of": ModifierForm.LOSE,
        "^lose ([\\d\\.]+)": ModifierForm.LOSE,
        "^lose \\+(\\d+)% to": ModifierForm.LOSE,
        
        # Grants and removes
        "^grants ([\\d\\.]+)": ModifierForm.GRANTS,
        "^removes? ([\\d\\.]+) ?o?f? ?y?o?u?r?": ModifierForm.REMOVES,
        
        # Simple numeric
        "^(\\d+)": ModifierForm.BASE,
        
        # Chance and flag modifiers
        "^([\\+\\-]?\\d+)% chance": ModifierForm.CHANCE,
        "^([\\+\\-]?\\d+)% chance to gain ": ModifierForm.FLAG,
        "^([\\+\\-]?\\d+)% additional chance": ModifierForm.CHANCE,
        
        # Cost modifiers
        "costs? ([\\+\\-]?\\d+)": ModifierForm.TOTAL_COST,
        "skills cost ([\\+\\-]?\\d+)": ModifierForm.BASE_COST,
        
        # Penetration modifiers
        "penetrates? (\\d+)%": ModifierForm.PENETRATION,
        "penetrates (\\d+)% of": ModifierForm.PENETRATION,
        "penetrates (\\d+)% of enemy": ModifierForm.PENETRATION,
        
        # Regeneration modifiers
        "^([\\d\\.]+) (.+) regenerated per second": ModifierForm.REGEN_FLAT,
        "^([\\d\\.]+)% (.+) regenerated per second": ModifierForm.REGEN_PERCENT,
        "^([\\d\\.]+)% of (.+) regenerated per second": ModifierForm.REGEN_PERCENT,
        "^regenerate ([\\d\\.]+) (.-) per second": ModifierForm.REGEN_FLAT,
        "^regenerate ([\\d\\.]+)% (.-) per second": ModifierForm.REGEN_PERCENT,
        "^regenerate ([\\d\\.]+)% of (.-) per second": ModifierForm.REGEN_PERCENT,
        "^regenerate ([\\d\\.]+)% of your (.-) per second": ModifierForm.REGEN_PERCENT,
        "^you regenerate ([\\d\\.]+)% of (.-) per second": ModifierForm.REGEN_PERCENT,
        
        # Degeneration modifiers
        "^([\\d\\.]+) (.+) lost per second": ModifierForm.DEGEN_FLAT,
        "^([\\d\\.]+)% (.+) lost per second": ModifierForm.DEGEN_PERCENT,
        "^([\\d\\.]+)% of (.+) lost per second": ModifierForm.DEGEN_PERCENT,
        "^lose ([\\d\\.]+) (.-) per second": ModifierForm.DEGEN_FLAT,
        "^lose ([\\d\\.]+)% (.-) per second": ModifierForm.DEGEN_PERCENT,
        "^lose ([\\d\\.]+)% of (.-) per second": ModifierForm.DEGEN_PERCENT,
        "^lose ([\\d\\.]+)% of your (.-) per second": ModifierForm.DEGEN_PERCENT,
        "^you lose ([\\d\\.]+)% of (.-) per second": ModifierForm.DEGEN_PERCENT,
        
        # Generic degeneration
        "^([\\d\\.]+) ([a-zA-Z]+) damage taken per second": ModifierForm.DEGEN,
        "^([\\d\\.]+) ([a-zA-Z]+) damage per second": ModifierForm.DEGEN,
        
        # Damage modifiers
        "(\\d+) to (\\d+) added ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "(\\d+)-(\\d+) added ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "(\\d+) to (\\d+) additional ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "(\\d+)-(\\d+) additional ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "^(\\d+) to (\\d+) ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage": ModifierForm.DAMAGE,
        
        # Attack damage modifiers
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage to attacks": ModifierForm.DAMAGE_ATTACKS,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage to attacks": ModifierForm.DAMAGE_ATTACKS,
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) attack damage": ModifierForm.DAMAGE_ATTACKS,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) attack damage": ModifierForm.DAMAGE_ATTACKS,
        "(\\d+) to (\\d+) added attack ([a-zA-Z]+) damage": ModifierForm.DAMAGE_ATTACKS,
        
        # Spell damage modifiers
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage to spells": ModifierForm.DAMAGE_SPELLS,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage to spells": ModifierForm.DAMAGE_SPELLS,
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) spell damage": ModifierForm.DAMAGE_SPELLS,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) spell damage": ModifierForm.DAMAGE_SPELLS,
        "(\\d+) to (\\d+) added spell ([a-zA-Z]+) damage": ModifierForm.DAMAGE_SPELLS,
        
        # Combined damage modifiers
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage to attacks and spells": ModifierForm.DAMAGE_BOTH,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage to attacks and spells": ModifierForm.DAMAGE_BOTH,
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage to spells and attacks": ModifierForm.DAMAGE_BOTH,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage to spells and attacks": ModifierForm.DAMAGE_BOTH,
        "adds (\\d+) to (\\d+) ([a-zA-Z]+) damage to hits": ModifierForm.DAMAGE_BOTH,
        "adds (\\d+)-(\\d+) ([a-zA-Z]+) damage to hits": ModifierForm.DAMAGE_BOTH,
        
        # Flag modifiers
        "^you have ": ModifierForm.FLAG,
        "^have ": ModifierForm.FLAG,
        "^you are ": ModifierForm.FLAG,
        "^are ": ModifierForm.FLAG,
        "^gain ": ModifierForm.FLAG,
        "^you gain ": ModifierForm.FLAG,
        
        # Override modifier
        "is (-?\\d+)%? ": ModifierForm.OVERRIDE,
    }
    
    for pattern, form in patterns.items():
        manager.add_pattern(pattern, form)
    
    return manager