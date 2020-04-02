# PyLootTable - A framework to build loot tables out of Python Code

<!-- MarkdownTOC autolink="true" -->

- [Purpose](#purpose)
- [Installation](#installation)
- [Usage](#usage)
    - [Basic Loot Table](#basic-loot-table)
    - [Advanced Concepts](#advanced-concepts)
        - [Functions, Conditions, and Predicates](#functions-conditions-and-predicates)
        - [More than One Item](#more-than-one-item)

<!-- /MarkdownTOC -->

## Purpose
The purpose of this small python programming language is to provide the framework to build Minecraft loot tables using Python. It should speed up the time it takes to build loot tables versus building them manually, as well as eliminate most errors when it comes to building JSON syntax. It was originally a personal project in which I wanted to use to build loot tables quicker using Python for modding, but has since become a bigger project.

## Installation
This small python programming language was programmed in Python 3. Ensure you have that installed. You can download Python 3 [here](https://www.python.org/downloads/). Download the `pyloottable.py` file from the repository, and import it into your python file. You are now ready to build loot tables with Python!

## Usage

### Basic Loot Table
For this usage example, we will be creating a barebones loot table. One pool, one entry, no functions, no conditions.

In order to create a loot table, you'll need a table, a pool, and an entry. You define loot tables, pools, and entries like such:
```py
from pyloottable import Table, Pool, Entry, TableTypes, EntryTypes


entry = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:dirt')

pool = Pool(1, 'dirt0', entry).pool

table = Table(TableTypes.BLOCK, pool).table
```
Now, this is fairly easy to explain. This language works bottom up. You start at the very bottom with a *Table* object. It takes in a *TableTypes* value, which has a couple different types corresponding to the different types of loot tables:

TableType     | JSON Value 
---           | ---
ADVANCEMENT   | "minecraft:advancement_reward"
BLOCK         | "minecraft:block"
CHEST         | "minecraft:chest"
ENTITY        | "minecraft:entity"
FISHING       | "minecraft:fishing"
GENERIC       | "minecraft:generic"

The *Table* object also takes in a pool which you define above. To get the actual dictionary from the object, call the `table` property on it. That should return the dictionary required for JSON parsing.

Next, you define a *Pool*. This object takes in how many rolls on the pool it should roll, a name for the pool, and an entry. In order to pass the proper dictionary to your *Table* object, call the `pool` property on it.

Next, you define a *Entry* object. This object takes in a *EntryTypes* value, depending on what type of entry you want this to be.

EntryType          | JSON Value
---                | ---
ALTERNATIVES       | "minecraft:alternatives"
DYNAMIC            | "minecraft:dynamic"
EMPTY              | "minecraft:empty"
GROUP              | "minecraft:group"
ITEM               | "minecraft:item"
LOOT_TABLE         | "minecraft:loot_table"
SEQUENCE           | "minecraft:sequence"
TAG                | "minecraft:tag"

After that, you run the `gen_entry` method, in which you pass in your various arguments required for an entry of that type. For our basic loot table example, we pass in a namespaced block/item string to which we refer to the block. 

Once the entry is created, we now should test that our output is as desired. In order to do this, we pass our table to a JSON parser, get the string, and print it out. Your code should look like such:

```py
from pyloottable import Table, Pool, Entry, TableTypes, EntryTypes
import json


entry = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:dirt')

pool = Pool(1, 'dirt0', entry).pool

table = Table(TableTypes.BLOCK, pool).table

table_json = json.dumps(table, indent=4)
print(table_json)
```

Should all go well, your code should output something like this:

```json
{
    "type": "minecraft:block",
    "pools": {
        "rolls": 1,
        "name": "dirt0",
        "entries": {
            "type": "minecraft:item",
            "name": "minecraft:dirt"
        }
    }
}
```

Finally, in order to push this dictionary, which is now your loot table, into a proper file, you'll want to replace your original `table_json` and `print` code with something like this:

```py
with open('example_json.json', 'w') as file:
    json.dump(loot_table, file, indent=4)
```

This will open a new file named after what you called it in the first parameter of the `open` function in write mode and pass the json into the file and indent it properly.

### Advanced Concepts

#### Functions, Conditions, and Predicates
In order to add a function or a condition to an entry, pool, or table, you'll first have to create a *Function* or *Condition* object that represents said function/condition, and generate the dict associated with said object. 

Some conditions require predicates to be passed in. You can initialize a *Predicate*, and pass in the tags needed through the keyword arguments. To get the proper dictionary, call the `predicate` property on it to retrieve the proper dictionary.

Please note that functions can take conditions as well.

Functions should be placed above entries, and conditions should be placed above functions. If a condition requires entries, then those entries should be placed above the condition. If a condition requires a predicate, it should be placed above what condition they are being used for.

```py
from pyloottable import Table, TableTypes, Pool, Entry, EntryTypes, Function, Functions, Condition, Conditions, Predicate
import json


predicate = Predicate(flags={'is_on_fire': True}).predicate

condition = Condition(Conditions.ENTITY_PROPERTIES).gen_condition(entity='this', predicate=predicate)

function = Function(Functions.FURNACE_SMELT).gen_function(conditions=condition)

entry = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:porkchop', functions=function)

pool = Pool(1, 'porkchop_cook_example', entry).pool

table = Table(TableTypes.ENTITY, pool).table

with open('zombie.json', 'w') as file:
    json.dump(table, file, indent=4)
```

Once generated, it should look like this:

```json
{
    "type": "minecraft:entity",
    "pools": {
        "rolls": 1,
        "name": "porkchop_cook_example",
        "entries": {
            "type": "minecraft:item",
            "name": "minecraft:porkchop",
            "functions": {
                "function": "minecraft:furnace_smelt",
                "conditions": {
                    "condition": "minecraft:entity_properties",
                    "entity": "this",
                    "predicate": {
                        "flags": {
                            "is_on_fire": true
                        }
                    }
                }
            }
        }
    }
}
```

Functions and conditions in this program include:

Function            | JSON Value
---                 | ---
APPLY_BONUS         | "minecraft:apply_bonus"
COPY_NAME           | "minecraft:copy_name"
COPY_NBT            | "minecraft:copy_nbt"
COPY_STATE          | "minecraft:copy_state"
ENCHANT_RANDOMLY    | "minecraft:enchant_randomly"
ENCHANT_WITH_LEVELS | "minecraft:enchant_with_levels"
EXPLOSION_DECAY     | "minecraft:explosion_decay"
FURNACE_SMELT       | "minecraft:furnace_smelt"
LIMIT_COUNT         | "minecraft:limit_count"
LOOTING_ENCHANT     | "minecraft:looting_enchant"
SET_ATTRIBUTES      | "minecraft:set_attributes"
SET_CONTENTS        | "minecraft:set_contents"
SET_COUNT           | "minecraft:set_count"
SET_DAMAGE          | "minecraft:set_damage"
SET_LORE            | "minecraft:set_lore"
SET_NAME            | "minecraft:set_name"
SET_NBT             | "minecraft:set_nbt"

Condition           | JSON Value
---                 | ---
ALTERNATIVE         | "minecraft:alternative"
BLOCKSTATE_PROPERTY | "minecraft:block_state_property"
DAMAGE_SOURCE       | "minecraft:damage_source_properties"
ENTITY_PROPERTIES   | "minecraft:entity_properties"
INVERTED            | "minecraft:inverted"
KILLED_BY_PLAYER    | "minecraft:killed_by_player"
LOCATION            | "minecraft:location_check"
MATCH_TOOL          | "minecraft:match_tool"
RANDOM_CHANCE       | "minecraft:random_chance"
REFERENCE           | "minecraft:reference"
SURVIVES_EXPLOSION  | "minecraft:survives_explosion"
TIME                | "minecraft:time_check"
TOOL_ENCHANTMENT    | "minecraft:tool_enchantment"
WEATHER             | "minecraft:weather_check"

#### More than One Item
In order to define more than one pool, entry, function, or condition to use, define the pools or entries you want in a list, like so:

```py
from pyloottable import Table, TableTypes, Pool, Entry, EntryTypes
import json

entry = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:dirt')
entry2 = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:grass')

entry3 = Entry(EntryTypes.ITEM).gen_entry(name='minecraft:cobblestone')
entry4 = Entry(EntryTypes.EMPTY).gen_entry()

pool = Pool(1, 'dirt0', [entry, entry2]).pool

pool2 = Pool(1, 'dirt1', [entry3, entry4]).pool

loot_table = Table(TableTypes.BLOCK, [pool, pool2]).table

with open('example_json.json', 'w') as file:
    json.dump(loot_table, file, indent=4)
```

Note that in `pool`, `pool2`, and `loot_table`, they were both passed a list of entries/pools. This is valid, and the proper way to have more than one entry, pool, function, or condition in a table. It should generate this:

```json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "name": "dirt0",
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:dirt"
                },
                {
                    "type": "minecraft:item",
                    "name": "minecraft:grass"
                }
            ]
        },
        {
            "rolls": 1,
            "name": "dirt1",
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:cobblestone"
                },
                {
                    "type": "minecraft:empty"
                }
            ]
        }
    ]
}
```