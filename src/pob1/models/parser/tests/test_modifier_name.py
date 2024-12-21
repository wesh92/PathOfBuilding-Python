"""
Tests for the ModifierNameMap pydantic model and its component models.

This test suite follows several key principles from Tiger Style:
1. Tests both positive space (valid inputs/expected behavior) and negative space (invalid inputs/error cases)
2. Uses explicit assertions with clear failure messages
3. Tests both simple and compound cases to ensure robustness
4. Provides high assertion density to catch potential issues early
5. Tests relationships between components to ensure system integrity

The test structure is organized into classes that test:
- Basic model instantiation and validation
- Complex nested structures
- Edge cases and error conditions
- Integration between different components
"""

import pytest
from pydantic import ValidationError
from pob1.models.parser.modifier_name_model import (
    ModifierTag,
    ModifierValue,
    ModifierNameMap,
    SkillType,
    ModFlag,
    KeywordFlag,
)

class TestModifierTag:
    """Tests for the ModifierTag model component."""
    
    def test_basic_tag_creation(self):
        """Tests creation of ModifierTag with minimum required fields.
        
        Validates the positive space of basic tag creation.
        """
        tag = ModifierTag(type="SkillType")
        assert tag.type == "SkillType"
        assert tag.var is None
        assert tag.skillType is None
        assert tag.neg is None

    def test_complete_tag_creation(self):
        """Tests creation of ModifierTag with all fields populated.
        
        Validates the positive space of full tag creation with all optional fields.
        """
        tag = ModifierTag(
            type="SkillType",
            var="TestVar",
            skillType=SkillType.ATTACK,
            neg=True
        )
        assert tag.type == "SkillType"
        assert tag.var == "TestVar"
        assert tag.skillType == SkillType.ATTACK
        assert tag.neg is True

    def test_invalid_tag_type(self):
        """Tests that invalid tag types are rejected.
        
        Validates the negative space by ensuring improper types raise validation errors.
        """
        with pytest.raises(ValidationError):
            ModifierTag(type=123)  # type must be string

    def test_skillType_without_type(self):
        """Tests that skillType requires appropriate type field.
        
        Validates the negative space by ensuring skillType isn't accepted without
        proper context.
        """
        with pytest.raises(ValidationError):
            ModifierTag(type="Condition", skillType=SkillType.ATTACK)

class TestModifierValue:
    """Tests for the ModifierValue model component."""

    def test_basic_modifier_value(self):
        """Tests creation of ModifierValue with only required fields.
        
        Validates the positive space of minimal modifier creation.
        """
        mod = ModifierValue(value="Life")
        assert mod.value == "Life"
        assert mod.flags is None
        assert mod.keywordFlags is None
        assert mod.tag is None
        assert mod.tagList is None
        assert mod.addToMinion is None
        assert mod.addToSkill is None

    def test_complete_modifier_value(self):
        """Tests creation of ModifierValue with all fields populated.
        
        Validates the positive space of full modifier creation with optional fields.
        """
        tag = ModifierTag(type="SkillType", skillType=SkillType.ATTACK)
        mod = ModifierValue(
            value="Damage",
            flags=ModFlag.ATTACK,
            keywordFlags=KeywordFlag.ATTACK,
            tag=tag,
            addToMinion=True,
            addToSkill={"SkillName": "Clarity"}
        )
        
        assert mod.value == "Damage"
        assert mod.flags == ModFlag.ATTACK
        assert mod.keywordFlags == KeywordFlag.ATTACK
        assert mod.tag.type == "SkillType"
        assert mod.tag.skillType == SkillType.ATTACK
        assert mod.addToMinion is True
        assert mod.addToSkill == {"SkillName": "Clarity"}

    def test_invalid_flags(self):
        """Tests that invalid flag values are rejected.
        
        Validates the negative space by ensuring improper flag values raise errors.
        """
        with pytest.raises(ValidationError):
            ModifierValue(value="Life", flags="InvalidFlag")

class TestModifierNameMap:
    """Tests for the ModifierNameMap model."""

    def test_empty_map_creation(self):
        """Tests creation of an empty ModifierNameMap.
        
        Validates the positive space of minimal map creation.
        """
        mod_map = ModifierNameMap()
        assert isinstance(mod_map.attributes, dict)
        assert isinstance(mod_map.life_mana, dict)
        assert isinstance(mod_map.defences, dict)
        # Verify all categories are initialized as empty dicts
        assert len(mod_map.attributes) == 0
        assert len(mod_map.life_mana) == 0
        assert len(mod_map.defences) == 0

    def test_basic_attribute_mapping(self):
        """Tests basic attribute mapping functionality.
        
        Validates the positive space of simple attribute mappings.
        """
        mod_map = ModifierNameMap(attributes={
            "strength": "Str",
            "dexterity": "Dex",
            "intelligence": "Int"
        })
        assert mod_map.attributes["strength"] == "Str"
        assert mod_map.attributes["dexterity"] == "Dex"
        assert mod_map.attributes["intelligence"] == "Int"

    def test_complex_life_mana_mapping(self):
        """Tests complex life/mana modifier mappings.
        
        Validates the positive space of complex modifier structures with nested objects.
        """
        mod_map = ModifierNameMap(life_mana={
            "life": ModifierValue(value="Life"),
            "mana cost": ModifierValue(
                value="ManaCost",
                tag=ModifierTag(
                    type="SkillType",
                    skillType=SkillType.ATTACK
                )
            )
        })
        
        assert isinstance(mod_map.life_mana["life"], ModifierValue)
        assert mod_map.life_mana["life"].value == "Life"
        assert isinstance(mod_map.life_mana["mana cost"], ModifierValue)
        assert mod_map.life_mana["mana cost"].tag.skillType == SkillType.ATTACK

    def test_modifier_list_handling(self):
        """Tests handling of modifier lists.
        
        Validates the positive space of list-based modifier mappings.
        """
        mod_map = ModifierNameMap(attributes={
            "all attributes": ["Str", "Dex", "Int", "All"]
        })
        assert isinstance(mod_map.attributes["all attributes"], list)
        assert len(mod_map.attributes["all attributes"]) == 4
        assert "All" in mod_map.attributes["all attributes"]

    def test_invalid_category_type(self):
        """Tests rejection of invalid category types.
        
        Validates the negative space by ensuring improper category types raise errors.
        """
        with pytest.raises(ValidationError):
            ModifierNameMap(attributes=["invalid", "type"])  # Must be dict

    def test_invalid_modifier_structure(self):
        """Tests rejection of invalid modifier structures.
        
        Validates the negative space by ensuring improper modifier structures raise errors.
        """
        with pytest.raises(ValidationError):
            ModifierNameMap(life_mana={
                "life": {"invalid": "structure"}  # Must be ModifierValue
            })

    def test_cross_category_integrity(self):
        """Tests integrity across different modifier categories.
        
        Validates both positive and negative space by ensuring categories maintain
        proper structure and don't interfere with each other.
        """
        mod_map = ModifierNameMap(
            attributes={"strength": "Str"},
            life_mana={"life": ModifierValue(value="Life")},
            defences={"armour": ModifierValue(value="Armour")}
        )
        
        # Verify each category maintains its expected type and structure
        assert isinstance(mod_map.attributes["strength"], str)
        assert isinstance(mod_map.life_mana["life"], ModifierValue)
        assert isinstance(mod_map.defences["armour"], ModifierValue)

if __name__ == "__main__":
    pytest.main([__file__])