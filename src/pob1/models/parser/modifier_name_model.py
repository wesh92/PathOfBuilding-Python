from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, ValidationInfo, field_validator, ConfigDict
from src.pob1.constants.flags import ModFlag, KeywordFlag
from src.pob1.constants.skill_types import SkillType


class ModifierTag(BaseModel):
    """Represents a tag that can be applied to a modifier."""    
    type: str = Field(..., description="The type of tag (e.g., 'SkillType', 'Condition')")
    var: Optional[str] = Field(None, description="Variable name for the condition if applicable")
    skillType: Optional[SkillType] = Field(None, description="Skill type if tag type is SkillType")
    neg: Optional[bool] = Field(None, description="Whether this is a negative condition")

    @field_validator('skillType')
    def validate_skill_type(cls, v: Optional[SkillType], info: ValidationInfo) -> Optional[SkillType]:
        """Validates that skillType is only set when type is 'SkillType'.
        
        This enforces the relationship between type and skillType fields to maintain
        data integrity and prevent invalid combinations.
        
        Args:
            v: The skillType value to validate
            info: ValidationInfo object containing data about other fields

        Returns:
            The validated skillType value

        Raises:
            ValueError: If skillType is set but type is not 'SkillType'
        """
        if v is not None and info.data.get('type') != 'SkillType':
            raise ValueError("skillType can only be set when type is 'SkillType'")
        return v


class ModifierValue(BaseModel):
    """Represents a single modifier value with its associated metadata."""
    value: str = Field(..., description="The internal name of the modifier")
    flags: Optional[ModFlag] = Field(None, description="Modifier flags if applicable")
    keywordFlags: Optional[KeywordFlag] = Field(None, description="Keyword flags if applicable")
    tag: Optional[ModifierTag] = Field(None, description="Single tag for this modifier")
    tagList: Optional[List[ModifierTag]] = Field(None, description="List of tags for this modifier")
    addToMinion: Optional[bool] = Field(None, description="Whether this modifier adds to minions")
    addToSkill: Optional[Dict[str, str]] = Field(None, description="Skill-specific modifier additions")


class ModifierNameMap(BaseModel):
    """Maps textual modifier descriptions to their internal representations."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    attributes: Dict[str, Union[str, List[str]]] = Field(default_factory=dict, description="Attribute modifiers")
    life_mana: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict, 
        description="Life and mana related modifiers"
    )
    defences: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Defence-related modifiers"
    )
    damage_taken: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Damage taken modifiers"
    )
    resistances: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Resistance modifiers"
    )
    charges: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Charge-related modifiers"
    )
    dot_effects: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Damage over time modifiers"
    )
    skills: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Skill-related modifiers"
    )
    buffs: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Buff-related modifiers"
    )
    damage: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Damage modifiers"
    )
    ailments: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Ailment-related modifiers"
    )
    flask: Dict[str, Union[ModifierValue, List[ModifierValue]]] = Field(
        default_factory=dict,
        description="Flask-related modifiers"
    )


def create_modifier_map() -> ModifierNameMap:
    """Creates and initializes the complete ModifierNameMap.
    
    This function creates a new ModifierNameMap instance and initializes it with every
    modifier from the original Lua modNameList. The modifiers are categorized for better
    organization while maintaining complete coverage.
    
    Returns:
        ModifierNameMap: Fully populated map containing all modifiers from the Lua code.
    """
    # Create dictionary for the initial mapping
    # We'll organize these into categories for better maintenance and clarity
    # while ensuring we don't miss any modifiers from the original Lua
    return ModifierNameMap(
        attributes={
            "strength": "Str",
            "dexterity": "Dex",
            "intelligence": "Int",
            "omniscience": "Omni",
            "strength and dexterity": ["Str", "Dex", "StrDex"],
            "strength and intelligence": ["Str", "Int", "StrInt"],
            "dexterity and intelligence": ["Dex", "Int", "DexInt"],
            "attributes": ["Str", "Dex", "Int", "All"],
            "all attributes": ["Str", "Dex", "Int", "All"],
            "devotion": "Devotion",
        },
        life_mana={
            "life": ModifierValue(value="Life"),
            "maximum life": ModifierValue(value="Life"),
            "life regeneration rate": ModifierValue(value="LifeRegen"),
            "mana": ModifierValue(value="Mana"),
            "maximum mana": ModifierValue(value="Mana"),
            "mana regeneration": ModifierValue(value="ManaRegen"),
            "mana regeneration rate": ModifierValue(value="ManaRegen"),
            "mana cost": ModifierValue(value="ManaCost"),
            "mana cost of": ModifierValue(value="ManaCost"),
            "mana cost of skills": ModifierValue(value="ManaCost"),
            "mana cost of attacks": ModifierValue(
                value="ManaCost",
                tag=ModifierTag(type="SkillType", skillType=SkillType.ATTACK)
            ),
            "total cost": ModifierValue(value="Cost"),
            "total mana cost": ModifierValue(value="ManaCost"),
            "total mana cost of skills": ModifierValue(value="ManaCost"),
            "life cost of skills": ModifierValue(value="LifeCost"),
            "rage cost of skills": ModifierValue(value="RageCost"),
            "cost of": ModifierValue(value="Cost"),
            "cost of skills": ModifierValue(value="Cost"),
            "cost of attacks": ModifierValue(
                value="Cost",
                tag=ModifierTag(type="SkillType", skillType=SkillType.ATTACK)
            ),
            "cost of retaliation skills": ModifierValue(
                value="Cost",
                tag=ModifierTag(type="SkillType", skillType=SkillType.RETALIATION)
            ),
            "mana reserved": ModifierValue(value="ManaReserved"),
            "mana reservation": ModifierValue(value="ManaReserved"),
            "mana reservation of skills": ModifierValue(
                value="ManaReserved",
                tag=ModifierTag(type="SkillType", skillType=SkillType.AURA)
            ),
            "mana reservation efficiency of skills": ModifierValue(value="ManaReservationEfficiency"),
            "life reservation efficiency of skills": ModifierValue(value="LifeReservationEfficiency"),
            "reservation of skills": ModifierValue(value="Reserved"),
            "mana reservation if cast as an aura": ModifierValue(
                value="ManaReserved",
                tag=ModifierTag(type="SkillType", skillType=SkillType.AURA)
            ),
            "reservation if cast as an aura": ModifierValue(
                value="Reserved",
                tag=ModifierTag(type="SkillType", skillType=SkillType.AURA)
            ),
            "reservation": ModifierValue(value="Reserved"),
            "reservation efficiency": ModifierValue(value="ReservationEfficiency"),
            "reservation efficiency of skills": ModifierValue(value="ReservationEfficiency"),
            "mana reservation efficiency": ModifierValue(value="ManaReservationEfficiency"),
            "life reservation efficiency": ModifierValue(value="LifeReservationEfficiency"),
            "life recovery rate": ModifierValue(value="LifeRecoveryRate"),
            "mana recovery rate": ModifierValue(value="ManaRecoveryRate"),
            "energy shield recovery rate": ModifierValue(value="EnergyShieldRecoveryRate"),
            "recovery rate of life, mana and energy shield": [
                ModifierValue(value="LifeRecoveryRate"),
                ModifierValue(value="ManaRecoveryRate"),
                ModifierValue(value="EnergyShieldRecoveryRate")
            ],
        },
        defences={
            "maximum energy shield": ModifierValue(value="EnergyShield"),
            "energy shield recharge rate": ModifierValue(value="EnergyShieldRecharge"),
            "start of energy shield recharge": ModifierValue(value="EnergyShieldRechargeFaster"),
            "restoration of ward": ModifierValue(value="WardRechargeFaster"),
            "armour": ModifierValue(value="Armour"),
            "evasion": ModifierValue(value="Evasion"),
            "evasion rating": ModifierValue(value="Evasion"),
            "energy shield": ModifierValue(value="EnergyShield"),
            "ward": ModifierValue(value="Ward"),
            "armour and evasion": ModifierValue(value="ArmourAndEvasion"),
            "armour and evasion rating": ModifierValue(value="ArmourAndEvasion"),
            "evasion rating and armour": ModifierValue(value="ArmourAndEvasion"),
            "armour and energy shield": ModifierValue(value="ArmourAndEnergyShield"),
            "evasion rating and energy shield": ModifierValue(value="EvasionAndEnergyShield"),
            "evasion and energy shield": ModifierValue(value="EvasionAndEnergyShield"),
            "armour, evasion and energy shield": ModifierValue(value="Defences"),
            "defences": ModifierValue(value="Defences"),
            "to evade": ModifierValue(value="EvadeChance"),
            "chance to evade": ModifierValue(value="EvadeChance"),
            "to evade attacks": ModifierValue(value="EvadeChance"),
            "to evade attack hits": ModifierValue(value="EvadeChance"),
            "chance to evade attacks": ModifierValue(value="EvadeChance"),
            "chance to evade attack hits": ModifierValue(value="EvadeChance"),
            "chance to evade projectile attacks": ModifierValue(value="ProjectileEvadeChance"),
            "chance to evade melee attacks": ModifierValue(value="MeleeEvadeChance"),
            "evasion rating against melee attacks": ModifierValue(value="MeleeEvasion"),
            "evasion rating against projectile attacks": ModifierValue(value="ProjectileEvasion"),
            "to block": ModifierValue(value="BlockChance"),
            "to block attacks": ModifierValue(value="BlockChance"),
            "block chance": ModifierValue(value="BlockChance"),
            "chance to block": ModifierValue(value="BlockChance"),
            "block chance with staves": ModifierValue(
                value="BlockChance",
                tag=ModifierTag(type="Condition", var="UsingStaff")
            ),
            "to block with staves": ModifierValue(
                value="BlockChance",
                tag=ModifierTag(type="Condition", var="UsingStaff")
            ),
            "block chance against projectiles": ModifierValue(value="ProjectileBlockChance"),
            "to block projectile attack damage": ModifierValue(value="ProjectileBlockChance"),
            "spell block chance": ModifierValue(value="SpellBlockChance"),
            "to block spells": ModifierValue(value="SpellBlockChance"),
            "maximum block chance": ModifierValue(value="BlockChanceMax"),
            "life gained when you block": ModifierValue(value="LifeOnBlock"),
            "mana gained when you block": ModifierValue(value="ManaOnBlock"),
            "energy shield when you block": ModifierValue(value="EnergyShieldOnBlock"),
        },
        resistances={
            "physical damage reduction": ModifierValue(value="PhysicalDamageReduction"),
            "physical damage reduction from hits": ModifierValue(value="PhysicalDamageReductionWhenHit"),
            "elemental damage reduction": ModifierValue(value="ElementalDamageReduction"),
            "fire resistance": ModifierValue(value="FireResist"),
            "maximum fire resistance": ModifierValue(value="FireResistMax"),
            "cold resistance": ModifierValue(value="ColdResist"),
            "maximum cold resistance": ModifierValue(value="ColdResistMax"),
            "lightning resistance": ModifierValue(value="LightningResist"),
            "maximum lightning resistance": ModifierValue(value="LightningResistMax"),
            "chaos damage taken over time": ModifierValue(value="ChaosDamageTakenOverTime"),
            "chaos damage over time taken": ModifierValue(value="ChaosDamageTakenOverTime"),
            "elemental damage taken": ModifierValue(value="ElementalDamageTaken"),
            "elemental damage from hits taken": ModifierValue(value="ElementalDamageFromHitsTaken"),
            "elemental damage taken when hit": ModifierValue(value="ElementalDamageTakenWhenHit"),
            "elemental damage taken from hits": ModifierValue(value="ElementalDamageTakenWhenHit"),
            "elemental damage taken over time": ModifierValue(value="ElementalDamageTakenOverTime"),
            "cold and lightning damage taken": [
                ModifierValue(value="ColdDamageTaken"),
                ModifierValue(value="LightningDamageTaken")
            ],
            "fire and lightning damage taken": [
                ModifierValue(value="FireDamageTaken"),
                ModifierValue(value="LightningDamageTaken")
            ],
            "fire and cold damage taken": [
                ModifierValue(value="FireDamageTaken"),
                ModifierValue(value="ColdDamageTaken")
            ],
            "physical and chaos damage taken": [
                ModifierValue(value="PhysicalDamageTaken"),
                ModifierValue(value="ChaosDamageTaken")
            ],
            "reflected elemental damage taken": ModifierValue(value="ElementalReflectedDamageTaken"),
            "damage is taken from mana before life": ModifierValue(value="DamageTakenFromManaBeforeLife"),
            "lightning damage is taken from mana before life": ModifierValue(value="LightningDamageTakenFromManaBeforeLife"),
            "damage taken from mana before life": ModifierValue(value="DamageTakenFromManaBeforeLife"),
            "chaos resistance": ModifierValue(value="ChaosResist"),
            "maximum chaos resistance": ModifierValue(value="ChaosResistMax"),
            "fire and cold resistances": [
                ModifierValue(value="FireResist"),
                ModifierValue(value="ColdResist")
            ],
            "fire and lightning resistances": [
                ModifierValue(value="FireResist"),
                ModifierValue(value="LightningResist")
            ],
            "cold and lightning resistances": [
                ModifierValue(value="ColdResist"),
                ModifierValue(value="LightningResist")
            ],
            "elemental resistance": ModifierValue(value="ElementalResist"),
            "elemental resistances": ModifierValue(value="ElementalResist"),
            "all elemental resistances": ModifierValue(value="ElementalResist"),
            "all resistances": [
                ModifierValue(value="ElementalResist"),
                ModifierValue(value="ChaosResist")
            ],
            "all maximum elemental resistances": ModifierValue(value="ElementalResistMax"),
            "all maximum resistances": [
                ModifierValue(value="ElementalResistMax"),
                ModifierValue(value="ChaosResistMax")
            ],
            "all elemental resistances and maximum elemental resistances": [
                ModifierValue(value="ElementalResist"),
                ModifierValue(value="ElementalResistMax")
            ],
            "fire and chaos resistances": [
                ModifierValue(value="FireResist"),
                ModifierValue(value="ChaosResist")
            ],
            "cold and chaos resistances": [
                ModifierValue(value="ColdResist"),
                ModifierValue(value="ChaosResist")
            ],
            "lightning and chaos resistances": [
                ModifierValue(value="LightningResist"),
                ModifierValue(value="ChaosResist")
            ],
        },
        charges={
            "maximum power charge": ModifierValue(value="PowerChargesMax"),
            "maximum power charges": ModifierValue(value="PowerChargesMax"),
            "minimum power charge": ModifierValue(value="PowerChargesMin"),
            "minimum power charges": ModifierValue(value="PowerChargesMin"),
            "power charge duration": ModifierValue(value="PowerChargesDuration"),
            "maximum frenzy charge": ModifierValue(value="FrenzyChargesMax"),
            "maximum frenzy charges": ModifierValue(value="FrenzyChargesMax"),
            "minimum frenzy charge": ModifierValue(value="FrenzyChargesMin"),
            "minimum frenzy charges": ModifierValue(value="FrenzyChargesMin"),
            "frenzy charge duration": ModifierValue(value="FrenzyChargesDuration"),
            "maximum endurance charge": ModifierValue(value="EnduranceChargesMax"),
            "maximum endurance charges": ModifierValue(value="EnduranceChargesMax"),
            "minimum endurance charge": ModifierValue(value="EnduranceChargesMin"),
            "minimum endurance charges": ModifierValue(value="EnduranceChargesMin"),
            "minimum endurance, frenzy and power charges": [
                ModifierValue(value="PowerChargesMin"),
                ModifierValue(value="FrenzyChargesMin"),
                ModifierValue(value="EnduranceChargesMin")
            ],
            "endurance charge duration": ModifierValue(value="EnduranceChargesDuration"),
            "maximum frenzy charges and maximum power charges": [
                ModifierValue(value="FrenzyChargesMax"),
                ModifierValue(value="PowerChargesMax")
            ],
            "maximum power charges and maximum endurance charges": [
                ModifierValue(value="PowerChargesMax"),
                ModifierValue(value="EnduranceChargesMax")
            ],
            "maximum endurance, frenzy and power charges": [
                ModifierValue(value="EnduranceChargesMax"),
                ModifierValue(value="PowerChargesMax"),
                ModifierValue(value="FrenzyChargesMax")
            ],
            "endurance, frenzy and power charge duration": [
                ModifierValue(value="PowerChargesDuration"),
                ModifierValue(value="FrenzyChargesDuration"),
                ModifierValue(value="EnduranceChargesDuration")
            ],
            "maximum siphoning charge": ModifierValue(value="SiphoningChargesMax"),
            "maximum siphoning charges": ModifierValue(value="SiphoningChargesMax"),
            "maximum challenger charges": ModifierValue(value="ChallengerChargesMax"),
            "maximum blitz charges": ModifierValue(value="BlitzChargesMax"),
            "maximum number of crab barriers": ModifierValue(value="CrabBarriersMax"),
            "maximum blood charges": ModifierValue(value="BloodChargesMax"),
            "maximum spirit charges": ModifierValue(value="SpiritChargesMax"),
            "charge duration": ModifierValue(value="ChargeDuration"),
        },
        dot_effects={
            "damage over time": ModifierValue(value="Damage", flags=ModFlag.DOT),
            "physical damage over time": ModifierValue(
                value="PhysicalDamage",
                keywordFlags=KeywordFlag.PHYSICAL_DOT
            ),
            "cold damage over time": ModifierValue(
                value="ColdDamage",
                keywordFlags=KeywordFlag.COLD_DOT
            ),
            "fire damage over time": ModifierValue(
                value="FireDamage",
                keywordFlags=KeywordFlag.FIRE_DOT
            ),
            "chaos damage over time": ModifierValue(
                value="ChaosDamage",
                keywordFlags=KeywordFlag.CHAOS_DOT
            ),
            "physical damage over time multiplier": ModifierValue(value="PhysicalDotMultiplier"),
            "fire damage over time multiplier": ModifierValue(value="FireDotMultiplier"),
            "cold damage over time multiplier": ModifierValue(value="ColdDotMultiplier"),
            "chaos damage over time multiplier": ModifierValue(value="ChaosDotMultiplier"),
            "damage over time multiplier": ModifierValue(value="DotMultiplier"),
        },
        skills={
            "radius": ModifierValue(value="AreaOfEffect"),
            "radius of area skills": ModifierValue(value="AreaOfEffect"),
            "area of effect radius": ModifierValue(value="AreaOfEffect"),
            "area of effect": ModifierValue(value="AreaOfEffect"),
            "area of effect of skills": ModifierValue(value="AreaOfEffect"),
            "area of effect of area skills": ModifierValue(value="AreaOfEffect"),
            "duration": ModifierValue(value="Duration"),
            "skill effect duration": ModifierValue(value="Duration"),
            "chaos skill effect duration": ModifierValue(
                value="Duration",
                keywordFlags=KeywordFlag.CHAOS
            ),
            "cooldown recovery": ModifierValue(value="CooldownRecovery"),
            "cooldown recovery speed": ModifierValue(value="CooldownRecovery"),
            "cooldown recovery rate": ModifierValue(value="CooldownRecovery"),
            "weapon range": ModifierValue(value="WeaponRange"),
            "melee range": ModifierValue(value="MeleeWeaponRange"),
            "melee weapon range": ModifierValue(value="MeleeWeaponRange"),
            "to deal double damage": ModifierValue(value="DoubleDamageChance"),
            "to deal triple damage": ModifierValue(value="TripleDamageChance"),
            "critical strike chance": ModifierValue(value="CritChance"),
            "attack critical strike chance": ModifierValue(
                value="CritChance",
                flags=ModFlag.ATTACK
            ),
            "critical strike multiplier": ModifierValue(value="CritMultiplier"),
            "attack critical strike multiplier": ModifierValue(
                value="CritMultiplier",
                flags=ModFlag.ATTACK
            ),
            "accuracy": ModifierValue(value="Accuracy"),
            "accuracy rating": ModifierValue(value="Accuracy"),
            "minion accuracy rating": ModifierValue(value="Accuracy", addToMinion=True),
            "attack speed": ModifierValue(value="Speed", flags=ModFlag.ATTACK),
            "cast speed": ModifierValue(value="Speed", flags=ModFlag.CAST),
            "attack and cast speed": ModifierValue(value="Speed"),
            "metres to weapon range": ModifierValue(value="WeaponRangeMetre"),
            "metre to melee strike range": [
                ModifierValue(value="MeleeWeaponRangeMetre"),
                ModifierValue(value="UnarmedRangeMetre")
            ],
            "projectile damage": ModifierValue(value="Damage", flags=ModFlag.PROJECTILE),
            "projectile attack damage": ModifierValue(value="Damage", flags=ModFlag.PROJECTILE | ModFlag.ATTACK),
        },
        leech={
            "damage as life": ModifierValue(value="DamageLifeLeech"),
            "life leeched per second": ModifierValue(value="LifeLeechRate"),
            "mana leeched per second": ModifierValue(value="ManaLeechRate"), 
            "total recovery per second from life leech": ModifierValue(value="LifeLeechRate"),
            "recovery per second from life leech": ModifierValue(value="LifeLeechRate"),
            "total recovery per second from energy shield leech": ModifierValue(value="EnergyShieldLeechRate"),
            "recovery per second from energy shield leech": ModifierValue(value="EnergyShieldLeechRate"),
            "total recovery per second from mana leech": ModifierValue(value="ManaLeechRate"),
            "recovery per second from mana leech": ModifierValue(value="ManaLeechRate"),
            "total recovery per second from life, mana, or energy shield leech": [
                ModifierValue(value="LifeLeechRate"),
                ModifierValue(value="ManaLeechRate"),
                ModifierValue(value="EnergyShieldLeechRate")
            ],
            "maximum recovery per life leech": ModifierValue(value="MaxLifeLeechInstance"),
            "maximum recovery per energy shield leech": ModifierValue(value="MaxEnergyShieldLeechInstance"),
            "maximum recovery per mana leech": ModifierValue(value="MaxManaLeechInstance"),
            "maximum total recovery per second from life leech": ModifierValue(value="MaxLifeLeechRate"),
            "maximum total life recovery per second from leech": ModifierValue(value="MaxLifeLeechRate"),
            "maximum total recovery per second from energy shield leech": ModifierValue(value="MaxEnergyShieldLeechRate"),
            "maximum total energy shield recovery per second from leech": ModifierValue(value="MaxEnergyShieldLeechRate"),
            "maximum total recovery per second from mana leech": ModifierValue(value="MaxManaLeechRate"),
            "maximum total mana recovery per second from leech": ModifierValue(value="MaxManaLeechRate"),
            "maximum total life, mana and energy shield recovery per second from leech": [
                ModifierValue(value="MaxLifeLeechRate"),
                ModifierValue(value="MaxManaLeechRate"),
                ModifierValue(value="MaxEnergyShieldLeechRate")
            ],
            "life and mana leech is instant": [
                ModifierValue(value="InstantManaLeech"),
                ModifierValue(value="InstantLifeLeech")
            ],
            "life leech is instant": ModifierValue(value="InstantLifeLeech"),
            "mana leech is instant": ModifierValue(value="InstantManaLeech"),
            "energy shield leech is instant": ModifierValue(value="InstantEnergyShieldLeech"),
            "leech is instant": [
                ModifierValue(value="InstantEnergyShieldLeech"),
                ModifierValue(value="InstantManaLeech"),
                ModifierValue(value="InstantLifeLeech")
            ],
        },
        minions={
            "maximum number of skeletons": ModifierValue(value="ActiveSkeletonLimit"),
            "maximum number of zombies": ModifierValue(value="ActiveZombieLimit"),
            "maximum number of raised zombies": ModifierValue(value="ActiveZombieLimit"),
            "number of zombies allowed": ModifierValue(value="ActiveZombieLimit"),
            "maximum number of spectres": ModifierValue(value="ActiveSpectreLimit"),
            "maximum number of golems": ModifierValue(value="ActiveGolemLimit"),
            "maximum number of summoned golems": ModifierValue(value="ActiveGolemLimit"),
            "maximum number of summoned raging spirits": ModifierValue(value="ActiveRagingSpiritLimit"),
            "maximum number of raging spirits": ModifierValue(value="ActiveRagingSpiritLimit"),
            "maximum number of summoned phantasms": ModifierValue(value="ActivePhantasmLimit"),
            "maximum number of summoned holy relics": ModifierValue(value="ActiveHolyRelicLimit"),
            "number of summoned arbalists": ModifierValue(value="ActiveArbalistLimit"),
            "minion duration": ModifierValue(
                value="Duration",
                tag=ModifierTag(type="SkillType", skillType=SkillType.CREATES_MINION)
            ),
        },
        on_hit={
            "life gained on kill": ModifierValue(value="LifeOnKill"),
            "life per enemy killed": ModifierValue(value="LifeOnKill"),
            "life on kill": ModifierValue(value="LifeOnKill"),
            "life per enemy hit": ModifierValue(value="LifeOnHit", flags=ModFlag.HIT),
            "life gained for each enemy hit": ModifierValue(value="LifeOnHit", flags=ModFlag.HIT),
            "mana gained on kill": ModifierValue(value="ManaOnKill"),
            "mana per enemy killed": ModifierValue(value="ManaOnKill"),
            "mana on kill": ModifierValue(value="ManaOnKill"),
            "mana per enemy hit": ModifierValue(value="ManaOnHit", flags=ModFlag.HIT),
            "mana gained for each enemy hit": ModifierValue(value="ManaOnHit", flags=ModFlag.HIT),
            "energy shield gained on kill": ModifierValue(value="EnergyShieldOnKill"),
            "energy shield per enemy killed": ModifierValue(value="EnergyShieldOnKill"),
            "energy shield on kill": ModifierValue(value="EnergyShieldOnKill"),
            "energy shield per enemy hit": ModifierValue(value="EnergyShieldOnHit", flags=ModFlag.HIT),
            "energy shield gained for each enemy hit": ModifierValue(value="EnergyShieldOnHit", flags=ModFlag.HIT),
        },
        curses={
            "effect of your curses": ModifierValue(value="CurseEffect"),
            "effect of curses on you": ModifierValue(value="CurseEffectOnSelf"),
            "effect of curses on them": ModifierValue(value="CurseEffectOnSelf"),
            "curse effect": ModifierValue(value="CurseEffect"),
            "curse duration": ModifierValue(
                value="Duration",
                keywordFlags=KeywordFlag.CURSE
            ),
            "effect of curses applied by bane": ModifierValue(
                value="CurseEffect",
                tag=ModifierTag(type="Condition", var="AppliedByBane")
            ),
            "radius of curses": ModifierValue(
                value="AreaOfEffect",
                keywordFlags=KeywordFlag.CURSE
            ),
        },
        ailments={
            "to shock": ModifierValue(value="EnemyShockChance"),
            "shock chance": ModifierValue(value="EnemyShockChance"),
            "to freeze": ModifierValue(value="EnemyFreezeChance"),
            "freeze chance": ModifierValue(value="EnemyFreezeChance"),
            "to ignite": ModifierValue(value="EnemyIgniteChance"),
            "ignite chance": ModifierValue(value="EnemyIgniteChance"),
            "to freeze, shock and ignite": [
                ModifierValue(value="EnemyFreezeChance"),
                ModifierValue(value="EnemyShockChance"),
                ModifierValue(value="EnemyIgniteChance")
            ],
            "effect of shock": ModifierValue(value="EnemyShockEffect"),
            "effect of shock on you": ModifierValue(value="SelfShockEffect"),
            "effect of shock you inflict": ModifierValue(value="EnemyShockEffect"),
            "effect of shocks you inflict": ModifierValue(value="EnemyShockEffect"),
            "effect of chill": ModifierValue(value="EnemyChillEffect"),
            "effect of chill on you": ModifierValue(value="SelfChillEffect"),
            "effect of chill you inflict": ModifierValue(value="EnemyChillEffect"),
            "shock duration": ModifierValue(value="EnemyShockDuration"),
            "freeze duration": ModifierValue(value="EnemyFreezeDuration"),
            "chill duration": ModifierValue(value="EnemyChillDuration"),
            "ignite duration": ModifierValue(value="EnemyIgniteDuration"),
            "duration of elemental ailments": ModifierValue(value="EnemyElementalAilmentDuration"),
            "effect of non-damaging ailments": [
                ModifierValue(value="EnemyShockEffect"),
                ModifierValue(value="EnemyChillEffect"),
                ModifierValue(value="EnemyFreezeEffect"),
                ModifierValue(value="EnemyScorchEffect"),
                ModifierValue(value="EnemyBrittleEffect"),
                ModifierValue(value="EnemySapEffect")
            ],
        },
        flask={
            "effect": ModifierValue(value="LocalEffect"),
            "effect of flasks": ModifierValue(value="FlaskEffect"),
            "effect of tinctures": ModifierValue(value="TinctureEffect"),
            "amount recovered": ModifierValue(value="FlaskRecovery"),
            "life recovered": ModifierValue(value="FlaskRecovery"),
            "life recovery from flasks used": ModifierValue(value="FlaskLifeRecovery"),
            "recovery": ModifierValue(value="FlaskLifeRecoveryLowLife"),
            "mana recovered": ModifierValue(value="FlaskRecovery"),
            "flask effect duration": ModifierValue(value="FlaskDuration"),
            "recovery speed": ModifierValue(value="FlaskRecoveryRate"),
            "recovery rate": ModifierValue(value="FlaskRecoveryRate"),
            "flask recovery rate": ModifierValue(value="FlaskRecoveryRate"),
            "flask recovery speed": ModifierValue(value="FlaskRecoveryRate"),
            "flask life recovery rate": ModifierValue(value="FlaskLifeRecoveryRate"),
            "flask mana recovery rate": ModifierValue(value="FlaskManaRecoveryRate"),
            "extra charges": ModifierValue(value="FlaskCharges"),
            "maximum charges": ModifierValue(value="FlaskCharges"),
            "charges used": ModifierValue(value="FlaskChargesUsed"),
            "charges per use": ModifierValue(value="FlaskChargesUsed"),
            "flask charges used": ModifierValue(value="FlaskChargesUsed"),
            "flask charges gained": ModifierValue(value="FlaskChargesGained"),
            "charge recovery": ModifierValue(value="FlaskChargeRecovery"),
            "for flasks you use to not consume charges": ModifierValue(value="FlaskChanceNotConsumeCharges"),
            "for tinctures to not inflict mana burn": ModifierValue(value="TincturesNotInflictManaBurn"),
            "mana burn rate": ModifierValue(value="TinctureManaBurnRate"),
        },
        traps_mines={
            "trap throwing speed": ModifierValue(value="TrapThrowingSpeed"),
            "trap and mine throwing speed": [
                ModifierValue(value="TrapThrowingSpeed"),
                ModifierValue(value="MineLayingSpeed")
            ],
            "trap trigger area of effect": ModifierValue(value="TrapTriggerAreaOfEffect"),
            "trap duration": ModifierValue(value="TrapDuration"),
            "cooldown recovery speed for throwing traps": ModifierValue(
                value="CooldownRecovery",
                keywordFlags=KeywordFlag.TRAP
            ),
            "cooldown recovery rate for throwing traps": ModifierValue(
                value="CooldownRecovery",
                keywordFlags=KeywordFlag.TRAP
            ),
            "additional trap": ModifierValue(value="TrapThrowCount"),
            "additional traps": ModifierValue(value="TrapThrowCount"),
            "mine laying speed": ModifierValue(value="MineLayingSpeed"),
            "mine throwing speed": ModifierValue(value="MineLayingSpeed"),
            "mine detonation area of effect": ModifierValue(value="MineDetonationAreaOfEffect"),
            "mine duration": ModifierValue(value="MineDuration"),
            "additional mine": ModifierValue(value="MineThrowCount"),
            "additional mines": ModifierValue(value="MineThrowCount"),
        },
        miscellaneous={
            "movement speed": ModifierValue(value="MovementSpeed"),
            "attack, cast and movement speed": [
                ModifierValue(value="Speed"),
                ModifierValue(value="MovementSpeed")
            ],
            "action speed": ModifierValue(value="ActionSpeed"),
            "light radius": ModifierValue(value="LightRadius"),
            "rarity of items found": ModifierValue(value="LootRarity"),
            "rarity of items dropped": ModifierValue(value="LootRarity"),
            "quantity of items found": ModifierValue(value="LootQuantity"),
            "quantity of items dropped": ModifierValue(value="LootQuantity"),
            "item quantity": ModifierValue(value="LootQuantity"),
            "strength requirement": ModifierValue(value="StrRequirement"),
            "dexterity requirement": ModifierValue(value="DexRequirement"),
            "intelligence requirement": ModifierValue(value="IntRequirement"),
            "omni requirement": ModifierValue(value="OmniRequirement"),
            "strength and intelligence requirement": [
                ModifierValue(value="StrRequirement"),
                ModifierValue(value="IntRequirement")
            ],
            "attribute requirements": [
                ModifierValue(value="StrRequirement"),
                ModifierValue(value="DexRequirement"),
                ModifierValue(value="IntRequirement")
            ],
            "effect of socketed jewels": ModifierValue(value="SocketedJewelEffect"),
            "effect of socketed abyss jewels": ModifierValue(value="SocketedJewelEffect"),
        },
        condition_flags={
            "adrenaline": ModifierValue(value="Condition:Adrenaline"),
            "elusive": ModifierValue(value="Condition:CanBeElusive"),
            "onslaught": ModifierValue(value="Condition:Onslaught"),
            "rampage": ModifierValue(value="Condition:Rampage"),
            "soul eater": ModifierValue(value="Condition:CanHaveSoulEater"),
            "phasing": ModifierValue(value="Condition:Phasing"),
            "arcane surge": ModifierValue(value="Condition:ArcaneSurge"),
            "unholy might": [
                ModifierValue(value="Condition:UnholyMight"),
                ModifierValue(value="Condition:CanWither")
            ],
            "chaotic might": ModifierValue(value="Condition:ChaoticMight"),
            "lesser brutal shrine buff": ModifierValue(value="Condition:LesserBrutalShrine"),
            "lesser massive shrine buff": ModifierValue(value="Condition:LesserMassiveShrine"),
            "diamond shrine buff": ModifierValue(value="Condition:DiamondShrine"),
            "massive shrine buff": ModifierValue(value="Condition:MassiveShrine"),
        },        
        # damage taken modifiers
        damage_taken= {
            "damage taken": ModifierValue(value="DamageTaken"),
            "damage taken when hit": ModifierValue(value="DamageTakenWhenHit"),
            "damage taken from hits": ModifierValue(value="DamageTakenWhenHit"),
            "damage over time taken": ModifierValue(value="DamageTakenOverTime"),
            "damage taken from damage over time": ModifierValue(value="DamageTakenOverTime"),
            "attack damage taken": ModifierValue(value="AttackDamageTaken"),
            "spell damage taken": ModifierValue(value="SpellDamageTaken"),
            "physical damage taken from attacks": ModifierValue(value="PhysicalDamageTakenFromAttacks"),
            "physical damage taken from attack hits": ModifierValue(value="PhysicalDamageTakenFromAttacks"),
            "physical damage taken from projectile attacks": ModifierValue(value="PhysicalDamageTakenFromProjectileAttacks"),
            "physical damage taken from projectile attack hits": ModifierValue(value="PhysicalDamageTakenFromProjectileAttacks"),
            "fire, cold and lightning damage taken from spell hits": [
                ModifierValue(value="FireDamageTakenFromSpells"),
                ModifierValue(value="ColdDamageTakenFromSpells"),
                ModifierValue(value="LightningDamageTakenFromSpells")
            ],
            "reflected physical damage taken": ModifierValue(value="PhysicalReflectedDamageTaken"),
            "non-chaos damage taken bypasses energy shield": [
                ModifierValue(value="PhysicalEnergyShieldBypass"),
                ModifierValue(value="LightningEnergyShieldBypass"), 
                ModifierValue(value="ColdEnergyShieldBypass"),
                ModifierValue(value="FireEnergyShieldBypass")
            ],
        },

        # Dodge modifiers 
        dodge={
            "to dodge attacks": ModifierValue(value="AttackDodgeChance"),
            "to dodge attack hits": ModifierValue(value="AttackDodgeChance"),
            "to dodge spells": ModifierValue(value="SpellDodgeChance"),
            "to dodge spell hits": ModifierValue(value="SpellDodgeChance"),
            "to dodge spell damage": ModifierValue(value="SpellDodgeChance"),
            "to dodge attacks and spells": [
                ModifierValue(value="AttackDodgeChance"),
                ModifierValue(value="SpellDodgeChance")
            ],
            "to dodge attacks and spell damage": [
                ModifierValue(value="AttackDodgeChance"),
                ModifierValue(value="SpellDodgeChance")
            ],
            "to dodge attack and spell hits": [
                ModifierValue(value="AttackDodgeChance"),
                ModifierValue(value="SpellDodgeChance")
            ],
            "maximum chance to dodge spell hits": ModifierValue(value="SpellDodgeChanceMax"),
        },

        # Avoidance modifiers
        avoid={
            "to avoid physical damage from hits": ModifierValue(value="AvoidPhysicalDamageChance"),
            "to avoid fire damage when hit": ModifierValue(value="AvoidFireDamageChance"),
            "to avoid fire damage from hits": ModifierValue(value="AvoidFireDamageChance"),
            "to avoid cold damage when hit": ModifierValue(value="AvoidColdDamageChance"),
            "to avoid cold damage from hits": ModifierValue(value="AvoidColdDamageChance"),
            "to avoid lightning damage when hit": ModifierValue(value="AvoidLightningDamageChance"),
            "to avoid lightning damage from hits": ModifierValue(value="AvoidLightningDamageChance"),
            "to avoid elemental damage when hit": [
                ModifierValue(value="AvoidFireDamageChance"),
                ModifierValue(value="AvoidColdDamageChance"),
                ModifierValue(value="AvoidLightningDamageChance")
            ],
            "to avoid elemental damage from hits": [
                ModifierValue(value="AvoidFireDamageChance"),
                ModifierValue(value="AvoidColdDamageChance"),
                ModifierValue(value="AvoidLightningDamageChance")
            ],
            "to avoid projectiles": ModifierValue(value="AvoidProjectilesChance"),
            "to avoid being stunned": ModifierValue(value="AvoidStun"),
            "to avoid interruption from stuns while casting": ModifierValue(value="AvoidInterruptStun"),
            "to ignore stuns while casting": ModifierValue(value="AvoidInterruptStun"),
            "to avoid being shocked": ModifierValue(value="AvoidShock"),
            "to avoid being frozen": ModifierValue(value="AvoidFreeze"),
            "to avoid being chilled": ModifierValue(value="AvoidChill"),
            "to avoid being ignited": ModifierValue(value="AvoidIgnite"),
            "to avoid blind": ModifierValue(value="AvoidBlind"),
            "to avoid elemental ailments": ModifierValue(value="AvoidElementalAilments"),
            "to avoid elemental status ailments": ModifierValue(value="AvoidElementalAilments"),
            "to avoid ailments": ModifierValue(value="AvoidAilments"),
            "to avoid status ailments": ModifierValue(value="AvoidAilments"),
            "to avoid bleeding": ModifierValue(value="AvoidBleed"),
            "to avoid being poisoned": ModifierValue(value="AvoidPoison"),
            "to avoid being impaled": ModifierValue(value="AvoidImpale"),
        },

        # Rage and fortification modifiers
        rage_and_fortification={
            "maximum rage": ModifierValue(value="MaximumRage"),
            "minimum rage": ModifierValue(value="MinimumRage"),
            "rage effect": ModifierValue(value="RageEffect"),
            "maximum fortification": ModifierValue(value="MaximumFortification"),
            "fortification": ModifierValue(value="MinimumFortification"),
            "maximum valour": ModifierValue(value="MaximumValour"),
        },

        # Poison and bleed modifiers
        poison_and_bleed={
            "to poison": ModifierValue(value="PoisonChance"),
            "to cause poison": ModifierValue(value="PoisonChance"),
            "to poison on hit": ModifierValue(value="PoisonChance"),
            "poison duration": ModifierValue(value="EnemyPoisonDuration"),
            "to cause bleeding": ModifierValue(value="BleedChance"),
            "to cause bleeding on hit": ModifierValue(value="BleedChance"),
            "to inflict bleeding": ModifierValue(value="BleedChance"),
            "to inflict bleeding on hit": ModifierValue(value="BleedChance"),
            "to bleed": ModifierValue(value="BleedChance"),
            "bleed duration": ModifierValue(value="EnemyBleedDuration"),
            "bleeding duration": ModifierValue(value="EnemyBleedDuration"),
        },

        # Exposure modifiers
        exposure={
            "to inflict fire exposure on hit": ModifierValue(value="FireExposureChance"),
            "to apply fire exposure on hit": ModifierValue(value="FireExposureChance"),
            "to inflict cold exposure on hit": ModifierValue(value="ColdExposureChance"),
            "to apply cold exposure on hit": ModifierValue(value="ColdExposureChance"),
            "to inflict lightning exposure on hit": ModifierValue(value="LightningExposureChance"),
            "to apply lightning exposure on hit": ModifierValue(value="LightningExposureChance"),
        },

        # Recovery modifiers
        recovery={
            "life recovery from flasks": ModifierValue(value="FlaskLifeRecovery"),
            "mana recovery from flasks": ModifierValue(value="FlaskManaRecovery"),
            "life and mana recovery from flasks": [
                ModifierValue(value="FlaskLifeRecovery"),
                ModifierValue(value="FlaskManaRecovery")
            ],
        },
        # Aura and buff effects category
        aura_effects={
            "aura effect": ModifierValue(value="AuraEffect"),
            "effect of non-curse auras you cast": [
                ModifierValue(value="AuraEffect",
                tag=ModifierTag(type="SkillType", skillType=SkillType.AURA))
            ],
            "effect of non-curse auras from your skills": [
                ModifierValue(value="AuraEffect",
                tag=ModifierTag(type="SkillType", skillType=SkillType.AURA))
            ],
            "effect of auras on you": ModifierValue(value="AuraEffectOnSelf"),
            "effect of arcane surge on you": ModifierValue(value="ArcaneSurgeEffect"),
            "effect of buffs on you": ModifierValue(value="BuffEffectOnSelf"),
            "effect of buffs granted by your golems": ModifierValue(value="BuffEffect"),
            "effect of offering spells": ModifierValue(
                value="BuffEffect",
                tag=ModifierTag(type="SkillName", skillNameList=["Bone Offering", "Flesh Offering", "Spirit Offering", "Blood Offering"])
            ),
            "effect of offerings": ModifierValue(
                value="BuffEffect",
                tag=ModifierTag(type="SkillName", skillNameList=["Bone Offering", "Flesh Offering", "Spirit Offering", "Blood Offering"])
            ),
            "effect of heralds on you": ModifierValue(
                value="BuffEffect",
                tag=ModifierTag(type="SkillType", skillType=SkillType.HERALD)
            ),
            "effect of herald buffs on you": ModifierValue(
                value="BuffEffect",
                tag=ModifierTag(type="SkillType", skillType=SkillType.HERALD)
            ),
            "effect of shrine buffs on you": ModifierValue(value="ShrineBuffEffect"),
            "radius of auras": ModifierValue(
                value="AreaOfEffect",
                keywordFlags=KeywordFlag.AURA
            ),
            "effect of withered": ModifierValue(value="WitherEffect"),
            "effect of withered on you": ModifierValue(value="WitherEffectOnSelf"),
        },

        # Special duration effects
        duration_effects={
            "soul gain prevention duration": ModifierValue(value="SoulGainPreventionDuration"),
            "sentinel of absolution duration": ModifierValue(value="SecondaryDuration"),
            "warcry speed": ModifierValue(value="WarcrySpeed"),
            "fire trap burning ground duration": ModifierValue(
                value="Duration",
                tag=ModifierTag(type="SkillName", skillName="Fire Trap")
            ),
            "aspect of the spider debuff duration": ModifierValue(
                value="Duration",
                tag=ModifierTag(type="SkillName", skillName="Aspect of the Spider")
            ),
        },

        # Brand modifiers
        brands={
            "activation frequency": ModifierValue(value="BrandActivationFrequency"),
            "brand activation frequency": ModifierValue(value="BrandActivationFrequency"),
            "brand attachment range": ModifierValue(value="BrandAttachmentRange"),
        },

        # Weapon-specific modifiers
        weapon_specifics={
            "bow damage": ModifierValue(value="Damage", flags=ModFlag.BOW | ModFlag.HIT),
            "damage with arrow hits": ModifierValue(value="Damage", flags=ModFlag.BOW | ModFlag.HIT),
            "wand damage": ModifierValue(value="Damage", flags=ModFlag.WAND | ModFlag.HIT),
            "wand physical damage": ModifierValue(value="PhysicalDamage", flags=ModFlag.WAND | ModFlag.HIT),
            "claw physical damage": ModifierValue(value="PhysicalDamage", flags=ModFlag.CLAW | ModFlag.HIT),
            "sword physical damage": ModifierValue(value="PhysicalDamage", flags=ModFlag.SWORD | ModFlag.HIT),
        },

        # Suppression and recoup effects
        suppression_and_recoup={
            # Suppression effects
            "to suppress spell damage": ModifierValue(value="SpellSuppressionChance"),
            "amount of suppressed spell damage prevented": ModifierValue(value="SpellSuppressionEffect"),
            # Recoup effects
            "damage taken recouped as life": ModifierValue(value="LifeRecoup"),
            "physical damage taken recouped as life": ModifierValue(value="PhysicalLifeRecoup"),
            "lightning damage taken recouped as life": ModifierValue(value="LightningLifeRecoup"),
            "cold damage taken recouped as life": ModifierValue(value="ColdLifeRecoup"),
            "fire damage taken recouped as life": ModifierValue(value="FireLifeRecoup"),
            "chaos damage taken recouped as life": ModifierValue(value="ChaosLifeRecoup"),
        },
        impale_effects={
            "to impale enemies on hit": ModifierValue(value="ImpaleChance"),
            "to impale on spell hit": ModifierValue(
                value="ImpaleChance",
                flags=ModFlag.SPELL
            ),
            "impale effect": ModifierValue(value="ImpaleEffect"),
            "effect of impales you inflict": ModifierValue(value="ImpaleEffect"),
            "effects of impale inflicted": ModifierValue(value="ImpaleEffect"),
            "effect of impales inflicted": ModifierValue(value="ImpaleEffect"),
            "impales you inflict last": ModifierValue(value="ImpaleStacksMax"),
        }
    )