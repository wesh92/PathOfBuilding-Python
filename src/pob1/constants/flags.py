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


def match_keyword_flags(keyword_flags: int, mod_keyword_flags: int) -> bool:
    """
    Compare KeywordFlags to determine if the mod's flags are satisfied.
    
    Args:
        keyword_flags: The KeywordFlags to be compared to
        mod_keyword_flags: The KeywordFlags stored in the mod
        
    Returns:
        Whether the KeywordFlags in the mod are satisfied
        
    Note:
        If MATCH_ALL is set in mod_keyword_flags, all flags must match.
        Otherwise, any matching flag satisfies the condition.
    """
    match_all = bool(mod_keyword_flags & KeywordFlag.MATCH_ALL)
    mod_keyword_flags &= ~KeywordFlag.MATCH_ALL
    keyword_flags &= ~KeywordFlag.MATCH_ALL
    
    if match_all:
        return (keyword_flags & mod_keyword_flags) == mod_keyword_flags
    return mod_keyword_flags == 0 or (keyword_flags & mod_keyword_flags) != 0