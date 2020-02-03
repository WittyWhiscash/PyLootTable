from enum import Enum
import json


# Enum to determine what type of loot table this is.
class LootTableTypes(Enum):
    ADVANCEMENT = "minecraft:advancement_reward"
    BLOCK = "minecraft:block"
    CHEST = "minecraft:chest"
    ENTITY = "minecraft:entity"
    FISHING = "minecraft:fishing"
    GENERIC = "minecraft:generic"


# Enum to determine conditions.
class LootTableConditions(Enum):
    ALTERNATIVE = "minecraft:alternative"
    BLOCKSTATE_PROPERTY = "minecraft:block_state_property"
    DAMAGE_SOURCE = "minecraft:damage_source_properties"
    ENTITY_PROPERTIES = "minecraft:entity_properties"
    INVERTED = "minecraft:inverted"
    KILLED_BY_PLAYER = "minecraft:killed_by_player"
    LOCATION = "minecraft:location_check"
    MATCH_TOOL = "minecraft:match_tool"
    RANDOM_CHANCE = "minecraft:random_chance"
    REFERENCE = "minecraft:reference"
    SURVIVES_EXPLOSION = "minecraft:survives_explosion"
    TIME = "minecraft:time_check"
    TOOL_ENCHANTMENT = "minecraft:tool_enchantment"
    WEATHER = "minecraft:weather_check"


# Enum to determine functions.
class LootTableFunctions(Enum):
    APPLY_BONUS = "minecraft:apply_bonus"
    COPY_NAME = "minecraft:copy_name"
    COPY_NBT = "minecraft:copy_nbt"
    COPY_STATE = "minecraft:copy_state"
    ENCHANT_RANDOMLY = "minecraft:enchant_randomly"
    ENCHANT_WITH_LEVELS = "minecraft:enchant_with_levels"
    EXPLOSION_DECAY = "minecraft:explosion_decay"
    FURNACE_SMELT = "minecraft:furnace_smelt"
    LIMIT_COUNT = "minecraft:limit_count"
    LOOTING_ENCHANT = "minecraft:looting_enchant"
    SET_ATTRIBUTES = "minecraft:set_attributes"
    SET_CONTENTS = "minecraft:set_contents"
    SET_COUNT = "minecraft:set_count"
    SET_DAMAGE = "minecraft:set_damage"
    SET_LORE = "minecraft:set_lore"
    SET_NAME = "minecraft:set_name"
    SET_NBT = "minecraft:set_nbt"


class LootTableEntryTypes(Enum):
    ALTERNATIVES = "minecraft:alternatives"
    DYNAMIC = "minecraft:dynamic"
    EMPTY = "minecraft:empty"
    GROUP = "minecraft:group"
    ITEM = "minecraft:item"
    LOOT_TABLE = "minecraft:loot_table"
    SEQUENCE = "minecraft:sequence"
    TAG = "minecraft:tag"

# Represents a loot table itself.
class LootTable():

    # Pass in a LootTableType for the loot table class to parse on init.
    # As well, pass in the pools, conditions, and functions used for this table.
    def __init__(self, table_type, pools, **kwargs):
        self.table = {'type': table_type.value, 'pools': pools}
        if 'functions' in kwargs:
            self.table['functions'] = kwargs.get('functions')
        if 'conditions' in kwargs:
            self.table['conditions']: kwargs.get('conditions')


# Represents a loot table condition.
class LootTableCondition():

    # Grab a LootTableConditions entry to gauge what kwargs to pass on to the gen function
    def __init__(self, condition_type):
        self.condition_type = condition_type

    # Grab the kwargs required as described below and generate the dict.
    def gen_condition(self, **kwargs):
        condition = self.condition_type.value
        # 1 Required Arg: A list of conditions to do an alternative against.
        if condition == LootTableConditions.ALTERNATIVE.value:
            return {'condition': LootTableConditions.ALTERNATIVE.value, 'terms': kwargs['terms']}
        # 3 Required Args: A namespaced block string, a property to test against, and the value of that property.
        if condition == LootTableConditions.BLOCKSTATE_PROPERTY.value:
            return {'condition': LootTableConditions.BLOCKSTATE_PROPERTY.value, 'block': kwargs['block'], 'property': {kwargs['property']: kwargs['value']}}
        # 1 Required Arg: A damage source predicate to compare against.
        if condition == LootTableConditions.DAMAGE_SOURCE.value:
            return {'condition': LootTableConditions.DAMAGE_SOURCE.value, 'predicate': kwargs['predicate']}
        # 2 Required Args: An entity variable to check the entity to which this will be applied, and an entity predicate to provide properties to check for.
        if condition == LootTableConditions.ENTITY_PROPERTIES.value:
            return {'condition': LootTableConditions.ENTITY_PROPERTIES.value, 'entity': kwargs['entity'], 'predicate': kwargs['predicate']}
        # 1 Required Arg: A condition to match and invert against.
        if condition == LootTableConditions.INVERTED.value:
            return {'condition': LootTableConditions.INVERTED.value, 'term': kwargs['term']}
        # 1 Optional Arg: Pass inverse if the killer won't be available.
        if condition == LootTableConditions.KILLED_BY_PLAYER.value:
            kbp_dict = {'condition': LootTableConditions.KILLED_BY_PLAYER.value}
            if 'inverse' in kwargs:
                kbp_dict['inverse'] = kwargs.get('inverse')
            return kbp_dict
        # 1 Required Arg, 3 Optional Args: A location predicate to match against the location of the loot table.
        # OPTIONAL: An offset for the X, Y, and Z position.
        if condition == LootTableConditions.LOCATION.value:
            location_dict = {'condition': LootTableConditions.LOCATION.value, 'predicate': kwargs['predicate']}
            if 'offsetX' in kwargs:
                location_dict['offsetX'] = kwargs.get('offsetX')
            if 'offsetY' in kwargs:
                location_dict['offsetY'] = kwargs.get('offsetY')
            if 'offsetZ' in kwargs:
                location_dict['offsetZ'] = kwargs.get('offsetZ')
            return location_dict
        # 1 Required Arg: An item predicate to match against the tool.
        if condition == LootTableConditions.MATCH_TOOL.value:
            return {'condition': LootTableConditions.MATCH_TOOL.value, 'predicate': kwargs['predicate']}
        # 1 Required Arg: A float to define the chance of it happening between 0.0 and 1.0
        if condition == LootTableConditions.RANDOM_CHANCE.value:
            return {'condition': LootTableConditions.RANDOM_CHANCE.value, 'chance': kwargs['chance']}
        # 1 Required Arg: A condition to reference against.
        if condition == LootTableConditions.REFERENCE.value:
            return {'condition': LootTableConditions.REFERENCE.value, 'name': kwargs['name']}
        # No Required Args
        if condition == LootTableConditions.SURVIVES_EXPLOSION.value:
            return {'condition': LootTableConditions.SURVIVES_EXPLOSION.value}
        # 2 Optional Args
        # OPTIONAL: Pick a time value, or a min and max time value in a dict
        # OPTIONAL: Choose a modulo'd time period.
        if condition == LootTableConditions.TIME.value:
            time_dict = {'condition': LootTableConditions.TIME.value}
            if 'value' in kwargs:
                time_dict['value'] = kwargs.get('value')
            if 'period' in kwargs:
                time_dict['period'] = kwargs.get('period')
            return time_dict
        # 1 Required Arg: An enchantments list which contains enchantment entries.
        if condition == LootTableConditions.TOOL_ENCHANTMENT.value:
            return {'condition': LootTableConditions.TOOL_ENCHANTMENT.value, 'enchantments': kwargs['enchantments']}
        # 2 Optional Args
        # OPTIONAL: Determine whether it is raining or not.
        # OPTIONAL: Determine if it is thundering or not.
        if condition == LootTableConditions.WEATHER.value:
            weather_dict = {'condition': LootTableConditions.WEATHER.value}
            if 'raining' in kwargs:
                weather_dict['raining'] = kwargs.get('raining')
            if 'thundering' in kwargs:
                weather_dict['thundering'] = kwargs.get('thundering')
            return weather_dict
        else:
            return {}


# Represents a loot table function.
class LootTableFunction():

    # Grab a LootTableFunctions entry to gauge what kwargs to pass on to the gen function
    def __init__(self, function_type):
        self.function_type = function_type

    # Grab the kwargs required as described below and generate the dict.
    def gen_function(self, **kwargs):
        function = self.function_type.value
        dictionary = {}
        # Takes different args based on the formula key.
        # If formula is equal to 'uniform_bonus_count', takes in a bonusMultiplier parameter.
        # Else, formula should be set to 'binomial_with_bonus_count', takes in an extra parameter and a probability parameter.
        if function == LootTableFunctions.APPLY_BONUS.value:
            if kwargs['formula'] == 'uniform_bonus_count':
                dictionary = {'function': LootTableFunctions.APPLY_BONUS.value, 'formula': kwargs['formula'], 'parameters': {'bonusMultiplier': kwargs['bonusMultiplier']}}
            else:
                dictionary = {'function': LootTableFunctions.APPLY_BONUS.value, 'formula': kwargs['formula'], 'parameters': {'extra': kwargs['extra'], 'probability': kwargs['probability']}}
        # No Required Args
        if function == LootTableFunctions.COPY_NAME.value:
            dictionary = {'function': LootTableFunctions.COPY_NAME.value, 'source': 'block_entity'}
        # 2 Required Args: The source of the nbt, and a list of operations (dict) each with a source, target, and an operation. 
        if function == LootTableFunctions.COPY_NBT.value:
            dictionary = {'function': LootTableFunctions.COPY_NBT.value, 'source': kwargs['source'], 'ops': kwargs['ops']}
        # 2 Required Args: The namespaced block ID of the block to match, and the property to copy.
        if function == LootTableFunctions.COPY_STATE.value:
            dictionary = {'function': LootTableFunctions.COPY_STATE.value, 'block': kwargs['block'], 'properties': kwargs['properties']}
        # 1 Optional Arg:
        # OPTIONAL: A list of enchantments to choose from.
        if function == LootTableFunctions.ENCHANT_RANDOMLY.value:
            dictionary = {'function': LootTableFunctions.ENCHANT_RANDOMLY.value}
            if 'enchantments' in kwargs:
                dictionary['enchantments'] = kwargs.get('enchantments')
        # 1 Required Arg and 1 Optional Arg: An exact enchantment level, or a dict with a min and max amount of levels to use.
        # OPTIONAL: Whether treasure enchantments are allowed on this item.
        if function == LootTableFunctions.ENCHANT_WITH_LEVELS.value:
            dictionary = {'function': LootTableFunctions.ENCHANT_WITH_LEVELS.value, 'levels': kwargs['levels']}
            if 'treasure' in kwargs:
                dictionary['treasure'] = kwargs.get('treasure')
        # No Required Args
        if function == LootTableFunctions.EXPLOSION_DECAY.value:
            dictionary = {'function': LootTableFunctions.EXPLOSION_DECAY.value}
        # No Required Args
        if function == LootTableFunctions.FURNACE_SMELT.value:
            dictionary = {'function': LootTableFunctions.FURNACE_SMELT.value}
        # 1 Required Arg: An exact value to limit, or a dict with a min and max value to limit.
        if function == LootTableFunctions.LIMIT_COUNT.value:
            dictionary = {'function': LootTableFunctions.LIMIT_COUNT.value, 'limit': kwargs['limit']}
        # 1 Required Arg and 1 Optional Arg: An exact value for additional items, or a dict with a min and max value to add to the count.
        # OPTIONAL: Specify the limit in the stack after the looting calculation. If nothing is defined, limit is set to 0.
        if function == LootTableFunctions.LOOTING_ENCHANT.value:
            dictionary = {'function': LootTableFunctions.LOOTING_ENCHANT.value, 'count': kwargs['count']}
            if 'limit' in kwargs:
                dictionary['limit'] = kwargs.get('limit')
            else:
                dictionary['limit'] = 0
        # 1 Required Arg: A list of dicts to represent attribute modifiers. Refer to wiki on loot tables for the structure.
        if function == LootTableFunctions.SET_ATTRIBUTES.value:
            dictionary = {'function': LootTableFunctions.SET_ATTRIBUTES.value, 'modifiers': kwargs['modifiers']}
        # 1 Required Arg: A list of LootTableEntries to use as the contents of the container.
        if function == LootTableFunctions.SET_CONTENTS.value:
            dictionary = {'function': LootTableFunctions.SET_CONTENTS.value, 'entries': kwargs['entries']}
        # 1 Required Arg: An exact value to set the count size, or a dict with a min and max count size.
        if function == LootTableFunctions.SET_COUNT.value:
            dictionary = {'function': LootTableFunctions.SET_COUNT.value, 'count': kwargs['count']}
        # 1 Required Arg: An exact value to set the damage, or a dict with a min and max damage.
        if function == LootTableFunctions.SET_DAMAGE.value:
            dictionary = {'function': LootTableFunctions.SET_DAMAGE.value, 'damage': kwargs['damage']}
        # 1 Required Arg and 2 Optional Args: A list of JSON text components.
        # OPTIONAL: Specify an entity to act as a source for @s in the JSON text.
        # OPTIONAL: A bool on whether it replaces all existing lines of lore or not.
        if function == LootTableFunctions.SET_LORE.value:
            dictionary = {'function': LootTableFunctions.SET_LORE.value, 'lore': kwargs['lore']}
            if 'entity' in kwargs:
                dictionary['entity'] = kwargs.get('entity')
            if 'replace' in kwargs:
                dictionary['replace'] = kwargs.get('replace')
        # 1 Required Arg and 1 Optional Arg: A name to use, being either a simple name, or a JSON text component.
        # OPTIONAL: Specify an entity to act as a source for @s in the JSON text.
        if function == LootTableFunctions.SET_NAME.value:
            dictionary = {'function': LootTableFunctions.SET_NAME.value, 'name': kwargs['name']}
            if 'entity' in kwargs:
                dictionary['entity'] = kwargs.get('entity')
        # 1 Required Arg: A tag string to add.
        if function == LootTableFunctions.SET_NBT.value:
            dictionary = {'function': LootTableFunctions.SET_NBT.value, 'tag': kwargs['tag']}
        if 'conditions' in kwargs:
            dictionary['conditions'] = kwargs.get('conditions')
        return dictionary


# Represents an item entry within a loot table
class LootTableEntry():

    # Pass in a namespace string to parse the proper entry you need.
    def __init__(self, entry_type):
        self.entry_type = entry_type

    # Grabs the kwargs passed to it and generates an entry based on the type.
    def gen_entry(self, **kwargs):
        entry_type = self.entry_type.value
        # 1 Required Arg: A list of entries to select one of.
        if entry_type == LootTableEntryTypes.ALTERNATIVES.value:
            return {'type': LootTableEntryTypes.ALTERNATIVES.value, 'children': kwargs['children']}
        # 1 Required Arg: Either "contents" for a block entity's contents, or "self" for getting banner/player head data.
        if entry_type == LootTableEntryTypes.DYNAMIC.value:
            return {'type': LootTableEntryTypes.DYNAMIC.value, 'name': kwargs['name']}
        # No Args: Generates an empty entry.
        if entry_type == LootTableEntryTypes.EMPTY.value:
            return {'type': LootTableEntryTypes.EMPTY.value}
        # 1 Required Arg: A list of entries to group together.
        if entry_type == LootTableEntryTypes.GROUP.value:
            return {'type': LootTableEntryTypes.GROUP.value, 'children': kwargs['children']}
        # 1 Required Arg, 2 Optional Args: A namespaced block/item name
        # OPTIONAL: A list of functions to apply to the block/item
        # OPTIONAL: A list of conditions to apply to the block/item
        if entry_type == LootTableEntryTypes.ITEM.value:
            item_dict = {'type': LootTableEntryTypes.ITEM.value, 'name': kwargs['name']}
            if 'functions' in kwargs:
                item_dict['functions'] = kwargs.get('functions')
            if 'conditions' in kwargs:
                item_dict['conditions'] = kwargs.get('conditions')
            return item_dict
        # 1 Required Arg: A namespaced directory that points to the loot table you want to use.
        if entry_type == LootTableEntryTypes.LOOT_TABLE.value:
            return {'type': LootTableEntryTypes.LOOT_TABLE.value, 'name': kwargs['name']}
        # 1 Required Arg: A list of entries, in order, that you want to sequence.
        if entry_type == LootTableEntryTypes.SEQUENCE.value:
            return {'type': LootTableEntryTypes.SEQUENCE.value, 'children': kwargs['children']}
        # 1 Required Arg, 1 Optional Arg: The name of the tag you want to use 
        # OPTIONAL: A boolean value on whether you want to expand it or not.
        if entry_type == LootTableEntryTypes.TAG.value:
            tag_dict = {'type': LootTableEntryTypes.TAG.value, 'name': kwargs['name']}
            if 'expand' in kwargs:
                tag_dict['expand'] = kwargs.get('expand')
            return tag_dict
        else:
            return {}


class LootTablePredicate():

    def __init__(self, **kwargs):
        self.predicate = dict(kwargs)

class LootTablePool():

    def __init__(self, rolls, pool_name, entries, **kwargs):
        self.pool = {'rolls': rolls, 'name': pool_name, 'entries': entries}
        if 'functions' in kwargs:
            self.pool['functions'] = kwargs.get('functions')
        if 'conditions' in kwargs:
            self.pool['conditions'] = kwargs.get('conditions')
