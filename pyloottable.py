from enum import Enum
import json


# Enum to determine what type of loot table this is.
class TableTypes(Enum):
    ADVANCEMENT = "minecraft:advancement_reward"
    BLOCK = "minecraft:block"
    CHEST = "minecraft:chest"
    ENTITY = "minecraft:entity"
    FISHING = "minecraft:fishing"
    GENERIC = "minecraft:generic"


# Enum to determine conditions.
class Conditions(Enum):
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
class Functions(Enum):
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


class EntryTypes(Enum):
    ALTERNATIVES = "minecraft:alternatives"
    DYNAMIC = "minecraft:dynamic"
    EMPTY = "minecraft:empty"
    GROUP = "minecraft:group"
    ITEM = "minecraft:item"
    LOOT_TABLE = "minecraft:loot_table"
    SEQUENCE = "minecraft:sequence"
    TAG = "minecraft:tag"

# Represents a loot table itself.
class Table():

    # Pass in a LootTableType for the loot table class to parse on init.
    # As well, pass in the pools, conditions, and functions used for this table.
    def __init__(self, table_type, pools, **kwargs):
        self.table = {'type': table_type.value, 'pools': pools}
        if 'functions' in kwargs:
            self.table['functions'] = kwargs.get('functions')
        if 'conditions' in kwargs:
            self.table['conditions']: kwargs.get('conditions')


# Represents a loot table condition.
class Condition():

    # Grab a LootTableConditions entry to gauge what kwargs to pass on to the gen function
    def __init__(self, condition_type):
        self.condition_type = condition_type

    # Grab the kwargs required as described below and generate the dict.
    def gen_condition(self, **kwargs):
        condition = self.condition_type.value
        # 1 Required Arg: A list of conditions to do an alternative against.
        if condition == Conditions.ALTERNATIVE.value:
            return {'condition': Conditions.ALTERNATIVE.value, 'terms': kwargs['terms']}
        # 3 Required Args: A namespaced block string, a property to test against, and the value of that property.
        if condition == Conditions.BLOCKSTATE_PROPERTY.value:
            return {'condition': Conditions.BLOCKSTATE_PROPERTY.value, 'block': kwargs['block'], 'property': {kwargs['property']: kwargs['value']}}
        # 1 Required Arg: A damage source predicate to compare against.
        if condition == Conditions.DAMAGE_SOURCE.value:
            return {'condition': Conditions.DAMAGE_SOURCE.value, 'predicate': kwargs['predicate']}
        # 2 Required Args: An entity variable to check the entity to which this will be applied, and an entity predicate to provide properties to check for.
        if condition == Conditions.ENTITY_PROPERTIES.value:
            return {'condition': Conditions.ENTITY_PROPERTIES.value, 'entity': kwargs['entity'], 'predicate': kwargs['predicate']}
        # 1 Required Arg: A condition to match and invert against.
        if condition == Conditions.INVERTED.value:
            return {'condition': Conditions.INVERTED.value, 'term': kwargs['term']}
        # 1 Optional Arg: Pass inverse if the killer won't be available.
        if condition == Conditions.KILLED_BY_PLAYER.value:
            dictionary = {'condition': Conditions.KILLED_BY_PLAYER.value}
            if 'inverse' in kwargs:
                dictionary['inverse'] = kwargs.get('inverse')
            return dictionary
        # 1 Required Arg, 3 Optional Args: A location predicate to match against the location of the loot table.
        # OPTIONAL: An offset for the X, Y, and Z position.
        if condition == Conditions.LOCATION.value:
            dictionary = {'condition': Conditions.LOCATION.value, 'predicate': kwargs['predicate']}
            if 'offsetX' in kwargs:
                dictionary['offsetX'] = kwargs.get('offsetX')
            if 'offsetY' in kwargs:
                dictionary['offsetY'] = kwargs.get('offsetY')
            if 'offsetZ' in kwargs:
                dictionary['offsetZ'] = kwargs.get('offsetZ')
            return dictionary
        # 1 Required Arg: An item predicate to match against the tool.
        if condition == Conditions.MATCH_TOOL.value:
            return {'condition': Conditions.MATCH_TOOL.value, 'predicate': kwargs['predicate']}
        # 1 Required Arg: A float to define the chance of it happening between 0.0 and 1.0
        if condition == Conditions.RANDOM_CHANCE.value:
            return {'condition': Conditions.RANDOM_CHANCE.value, 'chance': kwargs['chance']}
        # 1 Required Arg: A condition to reference against.
        if condition == Conditions.REFERENCE.value:
            return {'condition': Conditions.REFERENCE.value, 'name': kwargs['name']}
        # No Required Args
        if condition == Conditions.SURVIVES_EXPLOSION.value:
            return {'condition': Conditions.SURVIVES_EXPLOSION.value}
        # 2 Optional Args
        # OPTIONAL: Pick a time value, or a min and max time value in a dict
        # OPTIONAL: Choose a modulo'd time period.
        if condition == Conditions.TIME.value:
            dictionary = {'condition': Conditions.TIME.value}
            if 'value' in kwargs:
                dictionary['value'] = kwargs.get('value')
            if 'period' in kwargs:
                dictionary['period'] = kwargs.get('period')
            return dictionary
        # 1 Required Arg: An enchantments list which contains enchantment entries.
        if condition == Conditions.TOOL_ENCHANTMENT.value:
            return {'condition': Conditions.TOOL_ENCHANTMENT.value, 'enchantments': kwargs['enchantments']}
        # 2 Optional Args
        # OPTIONAL: Determine whether it is raining or not.
        # OPTIONAL: Determine if it is thundering or not.
        if condition == Conditions.WEATHER.value:
            dictionary = {'condition': Conditions.WEATHER.value}
            if 'raining' in kwargs:
                dictionary['raining'] = kwargs.get('raining')
            if 'thundering' in kwargs:
                dictionary['thundering'] = kwargs.get('thundering')
            return dictionary
        else:
            return {}


# Represents a loot table function.
class Function():

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
        if function == Functions.APPLY_BONUS.value:
            if kwargs['formula'] == 'uniform_bonus_count':
                dictionary = {'function': Functions.APPLY_BONUS.value, 'formula': kwargs['formula'], 'parameters': {'bonusMultiplier': kwargs['bonusMultiplier']}}
            else:
                dictionary = {'function': Functions.APPLY_BONUS.value, 'formula': kwargs['formula'], 'parameters': {'extra': kwargs['extra'], 'probability': kwargs['probability']}}
        # No Required Args
        if function == Functions.COPY_NAME.value:
            dictionary = {'function': Functions.COPY_NAME.value, 'source': 'block_entity'}
        # 2 Required Args: The source of the nbt, and a list of operations (dict) each with a source, target, and an operation. 
        if function == Functions.COPY_NBT.value:
            dictionary = {'function': Functions.COPY_NBT.value, 'source': kwargs['source'], 'ops': kwargs['ops']}
        # 2 Required Args: The namespaced block ID of the block to match, and the property to copy.
        if function == Functions.COPY_STATE.value:
            dictionary = {'function': Functions.COPY_STATE.value, 'block': kwargs['block'], 'properties': kwargs['properties']}
        # 1 Optional Arg:
        # OPTIONAL: A list of enchantments to choose from.
        if function == Functions.ENCHANT_RANDOMLY.value:
            dictionary = {'function': Functions.ENCHANT_RANDOMLY.value}
            if 'enchantments' in kwargs:
                dictionary['enchantments'] = kwargs.get('enchantments')
        # 1 Required Arg and 1 Optional Arg: An exact enchantment level, or a dict with a min and max amount of levels to use.
        # OPTIONAL: Whether treasure enchantments are allowed on this item.
        if function == Functions.ENCHANT_WITH_LEVELS.value:
            dictionary = {'function': Functions.ENCHANT_WITH_LEVELS.value, 'levels': kwargs['levels']}
            if 'treasure' in kwargs:
                dictionary['treasure'] = kwargs.get('treasure')
        # No Required Args
        if function == Functions.EXPLOSION_DECAY.value:
            dictionary = {'function': Functions.EXPLOSION_DECAY.value}
        # No Required Args
        if function == Functions.FURNACE_SMELT.value:
            dictionary = {'function': Functions.FURNACE_SMELT.value}
        # 1 Required Arg: An exact value to limit, or a dict with a min and max value to limit.
        if function == Functions.LIMIT_COUNT.value:
            dictionary = {'function': Functions.LIMIT_COUNT.value, 'limit': kwargs['limit']}
        # 1 Required Arg and 1 Optional Arg: An exact value for additional items, or a dict with a min and max value to add to the count.
        # OPTIONAL: Specify the limit in the stack after the looting calculation. If nothing is defined, limit is set to 0.
        if function == Functions.LOOTING_ENCHANT.value:
            dictionary = {'function': Functions.LOOTING_ENCHANT.value, 'count': kwargs['count']}
            if 'limit' in kwargs:
                dictionary['limit'] = kwargs.get('limit')
            else:
                dictionary['limit'] = 0
        # 1 Required Arg: A list of dicts to represent attribute modifiers. Refer to wiki on loot tables for the structure.
        if function == Functions.SET_ATTRIBUTES.value:
            dictionary = {'function': Functions.SET_ATTRIBUTES.value, 'modifiers': kwargs['modifiers']}
        # 1 Required Arg: A list of LootTableEntries to use as the contents of the container.
        if function == Functions.SET_CONTENTS.value:
            dictionary = {'function': Functions.SET_CONTENTS.value, 'entries': kwargs['entries']}
        # 1 Required Arg: An exact value to set the count size, or a dict with a min and max count size.
        if function == Functions.SET_COUNT.value:
            dictionary = {'function': Functions.SET_COUNT.value, 'count': kwargs['count']}
        # 1 Required Arg: An exact value to set the damage, or a dict with a min and max damage.
        if function == Functions.SET_DAMAGE.value:
            dictionary = {'function': Functions.SET_DAMAGE.value, 'damage': kwargs['damage']}
        # 1 Required Arg and 2 Optional Args: A list of JSON text components.
        # OPTIONAL: Specify an entity to act as a source for @s in the JSON text.
        # OPTIONAL: A bool on whether it replaces all existing lines of lore or not.
        if function == Functions.SET_LORE.value:
            dictionary = {'function': Functions.SET_LORE.value, 'lore': kwargs['lore']}
            if 'entity' in kwargs:
                dictionary['entity'] = kwargs.get('entity')
            if 'replace' in kwargs:
                dictionary['replace'] = kwargs.get('replace')
        # 1 Required Arg and 1 Optional Arg: A name to use, being either a simple name, or a JSON text component.
        # OPTIONAL: Specify an entity to act as a source for @s in the JSON text.
        if function == Functions.SET_NAME.value:
            dictionary = {'function': Functions.SET_NAME.value, 'name': kwargs['name']}
            if 'entity' in kwargs:
                dictionary['entity'] = kwargs.get('entity')
        # 1 Required Arg: A tag string to add.
        if function == Functions.SET_NBT.value:
            dictionary = {'function': Functions.SET_NBT.value, 'tag': kwargs['tag']}
        if 'conditions' in kwargs:
            dictionary['conditions'] = kwargs.get('conditions')
        return dictionary


# Represents an item entry within a loot table
class Entry():

    # Pass in a namespace string to parse the proper entry you need.
    def __init__(self, entry_type):
        self.entry_type = entry_type

    # Grabs the kwargs passed to it and generates an entry based on the type.
    def gen_entry(self, **kwargs):
        entry_type = self.entry_type.value
        # 1 Required Arg: A list of entries to select one of.
        if entry_type == EntryTypes.ALTERNATIVES.value:
            return {'type': EntryTypes.ALTERNATIVES.value, 'children': kwargs['children']}
        # 1 Required Arg: Either "contents" for a block entity's contents, or "self" for getting banner/player head data.
        if entry_type == EntryTypes.DYNAMIC.value:
            return {'type': EntryTypes.DYNAMIC.value, 'name': kwargs['name']}
        # No Args: Generates an empty entry.
        if entry_type == EntryTypes.EMPTY.value:
            return {'type': EntryTypes.EMPTY.value}
        # 1 Required Arg: A list of entries to group together.
        if entry_type == EntryTypes.GROUP.value:
            return {'type': EntryTypes.GROUP.value, 'children': kwargs['children']}
        # 1 Required Arg, 2 Optional Args: A namespaced block/item name
        # OPTIONAL: A list of functions to apply to the block/item
        # OPTIONAL: A list of conditions to apply to the block/item
        if entry_type == EntryTypes.ITEM.value:
            dictionary = {'type': EntryTypes.ITEM.value, 'name': kwargs['name']}
            if 'functions' in kwargs:
                dictionary['functions'] = kwargs.get('functions')
            if 'conditions' in kwargs:
                dictionary['conditions'] = kwargs.get('conditions')
            return dictionary
        # 1 Required Arg: A namespaced directory that points to the loot table you want to use.
        if entry_type == EntryTypes.LOOT_TABLE.value:
            return {'type': EntryTypes.LOOT_TABLE.value, 'name': kwargs['name']}
        # 1 Required Arg: A list of entries, in order, that you want to sequence.
        if entry_type == EntryTypes.SEQUENCE.value:
            return {'type': EntryTypes.SEQUENCE.value, 'children': kwargs['children']}
        # 1 Required Arg, 1 Optional Arg: The name of the tag you want to use 
        # OPTIONAL: A boolean value on whether you want to expand it or not.
        if entry_type == EntryTypes.TAG.value:
            dictionary = {'type': EntryTypes.TAG.value, 'name': kwargs['name']}
            if 'expand' in kwargs:
                dictionary['expand'] = kwargs.get('expand')
            return dictionary
        else:
            return {}


class Predicate():

    def __init__(self, **kwargs):
        self.predicate = dict(kwargs)

class Pool():

    def __init__(self, rolls, pool_name, entries, **kwargs):
        self.pool = {'rolls': rolls, 'name': pool_name, 'entries': entries}
        if 'functions' in kwargs:
            self.pool['functions'] = kwargs.get('functions')
        if 'conditions' in kwargs:
            self.pool['conditions'] = kwargs.get('conditions')
