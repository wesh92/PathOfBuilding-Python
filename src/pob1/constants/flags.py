"""
Flag constants used for modifiers and keywords in Path of Building.

This module defines the flag constants used throughout the application for
determining modifier and keyword behaviors.
"""
from enum import IntFlag
from typing import Optional


class ModFlag(IntFlag):
    """Modifier flags used to specify behavior and applicability of mods."""
    # Damage modes
    ATTACK = 0x00000001
    SPELL = 0x00000002
    HIT = 0x00000004
    DOT = 0x00000008
    CAST = 0x00000010
    
    # Damage sources
    MELEE = 0x00000100
    AREA = 0x00000200
    PROJECTILE = 0x00000400
    SOURCE_MASK = 0x00000600
    AILMENT = 0x00000800
    MELEE_HIT = 0x00001000
    WEAPON = 0x00002000
    
    # Weapon types
    AXE = 0x00010000
    BOW = 0x00020000
    CLAW = 0x00040000
    DAGGER = 0x00080000
    MACE = 0x00100000
    STAFF = 0x00200000
    SWORD = 0x00400000
    WAND = 0x00800000
    UNARMED = 0x01000000
    FISHING = 0x02000000
    
    # Weapon classes
    WEAPON_MELEE = 0x04000000
    WEAPON_RANGED = 0x08000000
    WEAPON_1H = 0x10000000
    WEAPON_2H = 0x20000000
    WEAPON_MASK = 0x2FFF0000
    
    @classmethod
    def verify_weapon_flags(cls, flags: 'ModFlag') -> bool:
        """Verify weapon flags are consistent."""
        weapon_type_flags = (cls.AXE | cls.BOW | cls.CLAW | cls.DAGGER | 
                           cls.MACE | cls.STAFF | cls.SWORD | cls.WAND | 
                           cls.UNARMED | cls.FISHING)
        weapon_class_flags = cls.WEAPON_MELEE | cls.WEAPON_RANGED | cls.WEAPON_1H | cls.WEAPON_2H
        
        # A weapon flag cannot be both melee and ranged
        assert not (flags & cls.WEAPON_MELEE and flags & cls.WEAPON_RANGED), \
            "Weapon cannot be both melee and ranged"
            
        # A weapon flag cannot be both 1H and 2H
        assert not (flags & cls.WEAPON_1H and flags & cls.WEAPON_2H), \
            "Weapon cannot be both one-handed and two-handed"
            
        # If any weapon type is set, the WEAPON flag should be set
        if flags & weapon_type_flags:
            assert flags & cls.WEAPON, "WEAPON flag must be set when weapon type is specified"
            
        # If weapon class flags are set, at least one weapon type should be set
        if flags & weapon_class_flags:
            assert flags & weapon_type_flags, "Weapon type must be specified with weapon class"
            
        return True


class KeywordFlag(IntFlag):
    """Keyword flags used to specify skill properties and behaviors."""
    # Skill keywords
    AURA = 0x00000001
    CURSE = 0x00000002
    WARCRY = 0x00000004
    MOVEMENT = 0x00000008
    PHYSICAL = 0x00000010
    FIRE = 0x00000020
    COLD = 0x00000040
    LIGHTNING = 0x00000080
    CHAOS = 0x00000100
    VAAL = 0x00000200
    BOW = 0x00000400
    
    # Skill types
    TRAP = 0x00001000
    MINE = 0x00002000
    TOTEM = 0x00004000
    MINION = 0x00008000
    ATTACK = 0x00010000
    SPELL = 0x00020000
    HIT = 0x00040000
    AILMENT = 0x00080000
    BRAND = 0x00100000
    
    # Other effects
    POISON = 0x00200000
    BLEED = 0x00400000
    IGNITE = 0x00800000
    
    # Damage over Time types
    PHYSICAL_DOT = 0x01000000
    LIGHTNING_DOT = 0x02000000
    COLD_DOT = 0x04000000
    FIRE_DOT = 0x08000000
    CHAOS_DOT = 0x10000000
    
    # Special flags
    MATCH_ALL = 0x40000000
    
    @classmethod
    def verify_damage_types(cls, flags: 'KeywordFlag') -> bool:
        """Verify damage type flags are consistent."""
        element_flags = cls.FIRE | cls.COLD | cls.LIGHTNING | cls.CHAOS | cls.PHYSICAL
        
        # If a DOT type is specified, the base damage type should also be specified
        if flags & cls.PHYSICAL_DOT:
            assert flags & cls.PHYSICAL, "Physical base type required for physical DOT"
        if flags & cls.FIRE_DOT:
            assert flags & cls.FIRE, "Fire base type required for fire DOT"
        if flags & cls.COLD_DOT:
            assert flags & cls.COLD, "Cold base type required for cold DOT"
        if flags & cls.LIGHTNING_DOT:
            assert flags & cls.LIGHTNING, "Lightning base type required for lightning DOT"
        if flags & cls.CHAOS_DOT:
            assert flags & cls.CHAOS, "Chaos base type required for chaos DOT"
            
        # If it's an ailment, it should have a damage type
        if flags & cls.AILMENT:
            assert flags & element_flags, "Ailment requires a damage type"
            
        return True



def match_keyword_flags(keyword_flags: int, mod_keyword_flags: int) -> bool:
    """Compare KeywordFlags to determine if the mod's flags are satisfied."""
    # Pre-condition assertions
    assert isinstance(keyword_flags, int), f"keyword_flags must be int, got {type(keyword_flags)}"
    assert isinstance(mod_keyword_flags, int), f"mod_keyword_flags must be int, got {type(mod_keyword_flags)}"
    
    match_all = bool(mod_keyword_flags & KeywordFlag.MATCH_ALL)
    mod_keyword_flags &= ~KeywordFlag.MATCH_ALL
    keyword_flags &= ~KeywordFlag.MATCH_ALL
    
    # Assert the masks are properly cleared
    assert not (keyword_flags & KeywordFlag.MATCH_ALL), "MATCH_ALL not properly cleared from keyword_flags"
    assert not (mod_keyword_flags & KeywordFlag.MATCH_ALL), "MATCH_ALL not properly cleared from mod_keyword_flags"
    
    result = (keyword_flags & mod_keyword_flags) == mod_keyword_flags if match_all \
        else mod_keyword_flags == 0 or (keyword_flags & mod_keyword_flags) != 0
        
    return result