"""
Tests for the Modifier models and pattern matching system.

This test suite follows Tiger Style principles:
1. Tests both positive and negative spaces comprehensively
2. Uses explicit assertions with clear error messages
3. Tests both simple and complex cases
4. Provides high assertion density
5. Tests relationships between components
6. Tests edge cases and error conditions

The test structure is organized by component and complexity:
- ModifierPattern tests
- Individual Modifier Type tests
- ModifierManager integration tests
- Complex pattern matching scenarios
"""

import pytest
from pydantic import ValidationError
from src.pob1.models.parser.modifier_model import (
    ModifierForm,
    ModifierPattern,
    ModifierType,
    NumericModifier,
    DamageModifier,
    RegenerationModifier,
    ModifierManager,
    ErrorModifier,
    create_modifier_manager,
)

class TestModifierPattern:
    """Tests for the ModifierPattern model and its pattern validation."""
    
    def test_valid_pattern_creation(self):
        """Tests creation of ModifierPattern with valid regex patterns.
        
        Validates the positive space of pattern creation with proper regex syntax.
        """
        pattern = ModifierPattern(
            pattern=r"^(\d+)% increased",
            form=ModifierForm.INCREASE
        )
        assert pattern.pattern == r"^(\d+)% increased"
        assert pattern.form == ModifierForm.INCREASE

    def test_lua_pattern_conversion(self):
        """Tests conversion of Lua patterns to Python regex.
        
        Ensures Lua pattern syntax is correctly translated to Python regex.
        """
        # Test various Lua pattern constructs
        conversions = [
            ("%d", "\\d"),
            ("%a", "[a-zA-Z]"),
            ("%-", "\\-"),
            ("%+", "\\+"),
            ("%.", "\\."),
            ("%%", "%"),
        ]
        
        for lua, python in conversions:
            pattern = ModifierPattern(
                pattern=f"^{lua}",
                form=ModifierForm.BASE
            )
            assert python in pattern.pattern

    def test_invalid_pattern_rejection(self):
        """Tests rejection of invalid regex patterns.
        
        Validates the negative space by ensuring improper patterns raise errors.
        """
        with pytest.raises(expected_exception=ValueError, match="Invalid regular expression pattern"):
            ModifierPattern(
                pattern="^[unmatched",  # Invalid regex due to unmatched bracket
                form=ModifierForm.BASE
            )

    def test_pattern_matching(self):
        """Tests pattern matching functionality.
        
        Tests both positive and negative matching cases.
        """
        pattern = ModifierPattern(
            pattern=r"^(\d+)% increased",
            form=ModifierForm.INCREASE
        )
        
        # Positive space - valid matches
        assert pattern.match("50% increased") == ["50"]
        assert pattern.match("100% increased") == ["100"]
        
        # Negative space - invalid matches
        assert pattern.match("50% more") is None
        assert pattern.match("increased 50%") is None

class TestModifierTypes:
    """Tests for different ModifierType implementations."""
    
    def test_numeric_modifier(self):
        """Tests NumericModifier creation and validation.
        
        Tests both valid and invalid numeric modifier scenarios.
        """
        # Positive space
        mod = NumericModifier(
            text="50% increased",
            form=ModifierForm.INCREASE,
            value=50.0
        )
        assert mod.value == 50.0
        assert mod.form == ModifierForm.INCREASE
        
        # Negative space - invalid value type
        with pytest.raises(ValidationError):
            NumericModifier(
                text="invalid",
                form=ModifierForm.INCREASE,
                value="not a number"
            )

    def test_damage_modifier(self):
        """Tests DamageModifier creation and validation.
        
        Tests both positive space (valid damage ranges) and negative space
        (invalid ranges and type combinations).
        """
        # Positive space - valid damage range
        valid_mod = DamageModifier(
            text="adds 5 to 10 fire damage",
            form=ModifierForm.DAMAGE,
            min_damage=5.0,
            max_damage=10.0,
            damage_type="fire"
        )
        assert valid_mod.min_damage == 5.0
        assert valid_mod.max_damage == 10.0
        assert valid_mod.damage_type == "fire"
        
        # Test equal min/max (edge case, but should be valid)
        equal_mod = DamageModifier(
            text="adds 5 to 5 fire damage",
            form=ModifierForm.DAMAGE,
            min_damage=5.0,
            max_damage=5.0,
            damage_type="fire"
        )
        assert equal_mod.min_damage == equal_mod.max_damage
        
        # Negative space - invalid ranges
        invalid_cases = [
            (10.0, 5.0,),  # Inverted range
            (-5.0, 10.0,),  # Negative damage
        ]
        
        for min_dmg, max_dmg in invalid_cases:
            with pytest.raises(ValidationError):
                DamageModifier(
                    text="invalid damage modifier",
                    form=ModifierForm.DAMAGE,
                    min_damage=min_dmg,
                    max_damage=max_dmg,
                    damage_type="fire"
                )

    def test_regeneration_modifier(self):
        """Tests RegenerationModifier creation and validation.
        
        Tests both flat and percentage-based regeneration modifiers.
        """
        # Positive space - flat regen
        mod = RegenerationModifier(
            text="2.5 life regenerated per second",
            form=ModifierForm.REGEN_FLAT,
            value=2.5,
            resource="life"
        )
        assert mod.value == 2.5
        assert mod.resource == "life"
        
        # Positive space - percentage regen
        mod = RegenerationModifier(
            text="1.5% mana regenerated per second",
            form=ModifierForm.REGEN_PERCENT,
            value=1.5,
            resource="mana"
        )
        assert mod.value == 1.5
        assert mod.resource == "mana"

class TestModifierManager:
    """Tests for the ModifierManager's pattern matching and parsing capabilities."""
    
    @pytest.fixture
    def manager(self):
        """Creates a ModifierManager with some test patterns."""
        return create_modifier_manager()

    def test_basic_numeric_parsing(self, manager):
        """Tests parsing of simple numeric modifiers.
        
        Ensures basic increase/decrease patterns are correctly parsed.
        """
        # Positive space - basic increases
        mod = manager.parse_modifier("50% increased")
        assert isinstance(mod, NumericModifier)
        assert mod.value == 50.0
        assert mod.form == ModifierForm.INCREASE
        
        # Positive space - basic reductions
        mod = manager.parse_modifier("25% reduced")
        assert isinstance(mod, NumericModifier)
        assert mod.value == 25.0
        assert mod.form == ModifierForm.REDUCE

    def test_damage_parsing(self, manager):
        """Tests parsing of damage modifiers.
        
        Validates various damage modifier patterns and forms.
        """
        cases = [
            ("adds 5 to 10 fire damage", ModifierForm.DAMAGE, 5.0, 10.0, "fire"),
            ("adds 1 to 6 chaos damage to spells", ModifierForm.DAMAGE_SPELLS, 1.0, 6.0, "chaos"),
            ("adds 10 to 20 cold damage to attacks", ModifierForm.DAMAGE_ATTACKS, 10.0, 20.0, "cold"),
        ]
        
        for text, form, min_dmg, max_dmg, dmg_type in cases:
            mod = manager.parse_modifier(text)
            assert isinstance(mod, DamageModifier)
            assert mod.form == form
            assert mod.min_damage == min_dmg
            assert mod.max_damage == max_dmg
            assert mod.damage_type == dmg_type

    def test_regeneration_parsing(self, manager):
        """Tests parsing of regeneration modifiers.
        
        Tests various regeneration and degeneration patterns.
        Includes both positive and negative space testing.
        """
        # Positive space - valid regeneration patterns
        cases = [
            (
                "regenerate 2.5 life per second",
                ModifierForm.REGEN_FLAT,
                2.5,
                "life"
            ),
            (
                "regenerate 1.5% mana per second",
                ModifierForm.REGEN_PERCENT,
                1.5,
                "mana"
            ),
            (
                "lose 4.0 energy shield per second",
                ModifierForm.DEGEN_FLAT,
                4.0,
                "energy shield"
            ),
        ]
        
        manager = create_modifier_manager()
        
        for text, expected_form, expected_value, expected_resource in cases:
            mod = manager.parse_modifier(text)
            assert isinstance(mod, RegenerationModifier)

        
        # Negative space - invalid regeneration patterns
        invalid_cases = [
            "regenerate some life per second",  # Missing numeric value
            "1.5% regeneration",  # Incomplete pattern
            "regenerate life",  # Missing rate
        ]
        
        for text in invalid_cases:
            mod = manager.parse_modifier(text)
            assert isinstance(mod, ErrorModifier)
            assert mod.form != expected_form

    def test_negative_space(self, manager):
        """Tests handling of invalid or unknown modifier texts.
        
        Validates the negative space by testing pattern matching failures.
        """
        invalid_cases = [
            "not a real modifier",
            "50% someunknownmodifier",
            "adds damage",  # Missing required numbers
            "regenerates stuff",  # Missing required pattern elements
        ]
        
        for text in invalid_cases:
            assert isinstance(manager.parse_modifier(text), ErrorModifier)

if __name__ == "__main__":
    pytest.main([__file__])