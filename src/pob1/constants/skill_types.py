"""
Skill type constants used in Path of Building.

This module defines the skill types from ActiveSkills.dat and GrantedEffects.dat.
Names are taken from ActiveSkillType.dat as of PoE 3.17.
"""
from enum import IntEnum, auto
from typing import Dict, Optional


class SkillType(IntEnum):
    """Skill types used to determine skill behavior and compatibility."""
    ATTACK = auto()
    SPELL = auto()
    PROJECTILE = auto()  # Specifically skills which fire projectiles
    DUAL_WIELD_ONLY = auto()  # Attack requires dual wielding, only used on Dual Strike
    BUFF = auto()
    REMOVED6 = auto()  # Now removed, was CanDualWield
    MAIN_HAND_ONLY = auto()  # Attack only uses main hand; removed in 3.5 but needed for 2.6
    REMOVED8 = auto()  # Now removed, was only used on Cleave
    MINION = auto()
    DAMAGE = auto()  # Skill hits (not used on attacks because all of them hit)
    AREA = auto()
    DURATION = auto()
    REQUIRES_SHIELD = auto()
    PROJECTILE_SPEED = auto()
    HAS_RESERVATION = auto()
    RESERVATION_BECOMES_COST = auto()
    TRAPPABLE = auto()  # Skill can be turned into a trap
    TOTEMABLE = auto()  # Skill can be turned into a totem
    MINEABLE = auto()  # Skill can be turned into a mine
    ELEMENTAL_STATUS = auto()  # Causes elemental status effects, but doesn't hit
    MINIONS_CAN_EXPLODE = auto()
    REMOVED22 = auto()  # Now removed, was AttackCanTotem
    CHAINS = auto()
    MELEE = auto()
    MELEE_SINGLE_TARGET = auto()
    MULTICASTABLE = auto()  # Spell can repeat via Spell Echo
    TOTEM_CASTS_ALONE = auto()
    MULTISTRIKEABLE = auto()  # Attack can repeat via Multistrike
    CAUSES_BURNING = auto()  # Deals burning damage
    SUMMONS_TOTEM = auto()
    TOTEM_CASTS_WHEN_NOT_DETACHED = auto()
    FIRE = auto()
    COLD = auto()
    LIGHTNING = auto()
    TRIGGERABLE = auto()
    TRAPPED = auto()
    MOVEMENT = auto()
    DAMAGE_OVER_TIME = auto()
    REMOTE_MINED = auto()
    TRIGGERED = auto()
    VAAL = auto()
    AURA = auto()
    CAN_TARGET_UNUSABLE_CORPSE = auto()
    RANGED_ATTACK = auto()
    CHAOS = auto()
    FIXED_SPEED_PROJECTILE = auto()
    THRESHOLD_JEWEL_AREA = auto()
    THRESHOLD_JEWEL_PROJECTILE = auto()
    THRESHOLD_JEWEL_DURATION = auto()
    THRESHOLD_JEWEL_RANGED_ATTACK = auto()
    CHANNEL = auto()
    DEGEN_ONLY_SPELL_DAMAGE = auto()
    INBUILT_TRIGGER = auto()
    GOLEM = auto()
    HERALD = auto()
    AURA_AFFECTS_ENEMIES = auto()
    NO_RUTHLESS = auto()
    THRESHOLD_JEWEL_SPELL_DAMAGE = auto()
    CASCADABLE = auto()
    PROJECTILES_FROM_USER = auto()
    MIRAGE_ARCHER_CAN_USE = auto()
    PROJECTILE_SPIRAL = auto()
    SINGLE_MAIN_PROJECTILE = auto()
    MINIONS_PERSIST_WHEN_SKILL_REMOVED = auto()
    PROJECTILE_NUMBER = auto()
    WARCRY = auto()
    INSTANT = auto()
    BRAND = auto()
    DESTROYS_CORPSE = auto()
    NON_HIT_CHILL = auto()
    CHILLING_AREA = auto()
    APPLIES_CURSE = auto()
    CAN_RAPID_FIRE = auto()
    AURA_DURATION = auto()
    AREA_SPELL = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    PHYSICAL = auto()
    APPLIES_MAIM = auto()
    CREATES_MINION = auto()
    GUARD = auto()
    TRAVEL = auto()
    BLINK = auto()
    CAN_HAVE_BLESSING = auto()
    PROJECTILES_NOT_FROM_USER = auto()
    ATTACK_IN_PLACE_IS_DEFAULT = auto()
    NOVA = auto()
    INSTANT_NO_REPEAT_WHEN_HELD = auto()
    INSTANT_SHIFT_ATTACK_FOR_LEFT_MOUSE = auto()
    AURA_NOT_ON_CASTER = auto()
    BANNER = auto()
    RAIN = auto()
    COOLDOWN = auto()
    THRESHOLD_JEWEL_CHAINING = auto()
    SLAM = auto()
    STANCE = auto()
    NON_REPEATABLE = auto()
    OTHER_THING_USES_SKILL = auto()
    STEEL = auto()
    HEX = auto()
    MARK = auto()
    AEGIS = auto()
    ORB = auto()
    KILL_NO_DAMAGE_MODIFIERS = auto()
    RANDOM_ELEMENT = auto()  # means elements cannot repeat
    LATE_CONSUME_COOLDOWN = auto()
    ARCANE = auto()  # means it is reliant on amount of mana spent
    FIXED_CAST_TIME = auto()
    REQUIRES_OFF_HAND_NOT_WEAPON = auto()
    LINK = auto()
    BLESSING = auto()
    ZERO_RESERVATION = auto()
    DYNAMIC_COOLDOWN = auto()
    MICROTRANSACTION = auto()
    OWNER_CANNOT_USE = auto()
    PROJECTILES_NOT_FIRED = auto()
    TOTEMS_ARE_BALLISTAE = auto()
    SKILL_GRANTED_BY_SUPPORT = auto()
    PREVENT_HEX_TRANSFER = auto()
    MINIONS_ARE_UNDAMAGEABLE = auto()
    INNATE_TRAUMA = auto()
    DUAL_WIELD_REQUIRES_DIFFERENT_TYPES = auto()
    NO_VOLLEY = auto()
    RETALIATION = auto()
    NEVER_EXERTABLE = auto()

    def __str__(self) -> str:
        """Return a clean string representation of the skill type."""
        return self.name.replace('_', ' ').title()

    @classmethod
    def get_description(cls, skill_type: 'SkillType') -> Optional[str]:
        """
        Get a human-readable description of a skill type.
        
        Args:
            skill_type: The SkillType to describe
            
        Returns:
            A string description of the skill type if available, None otherwise
        """
        descriptions: Dict[SkillType, str] = {
            cls.PROJECTILE: "Skills which fire projectiles",
            cls.DUAL_WIELD_ONLY: "Attack requires dual wielding",
            cls.MAIN_HAND_ONLY: "Attack only uses main hand",
            cls.MINION: "Creates or affects minions",
            cls.DAMAGE: "Skill hits (not used on attacks as they all hit)",
            cls.TRAPPABLE: "Can be turned into a trap",
            cls.TOTEMABLE: "Can be turned into a totem",
            cls.MINEABLE: "Can be turned into a mine",
            cls.ELEMENTAL_STATUS: "Causes elemental status effects without hitting",
            cls.MULTICASTABLE: "Can repeat via Spell Echo",
            cls.MULTISTRIKEABLE: "Can repeat via Multistrike",
            cls.CAUSES_BURNING: "Deals burning damage",
            cls.RANDOM_ELEMENT: "Elements cannot repeat",
            cls.ARCANE: "Relies on amount of mana spent",
        }
        return descriptions.get(skill_type)


# Global cache for optimization
class GlobalCache:
    """Global cache for storing computed data."""
    cached_data = {
        "MAIN": {},
        "CALCS": {},
        "CALCULATOR": {},
        "CACHE": {},
    }