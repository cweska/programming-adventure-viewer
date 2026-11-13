# Python students meet in the campaign (Modules 1-2), extracted verbatim from content/modules

## Leylines Awaken (Module 1)

### Part `program-movement`

**Instructions shown to students:**

Each `def` line makes a function: a named set of steps.
The game runs `move_left()` when you press the left arrow, `move_right()` for the right arrow, and so on.
Right now each function only says `pass`, which means do nothing.
1. Replace each `pass` with a command that moves the party, like `party.move("left")`. Use the direction in the function's name.
2. Press Run.
3. When the arrow keys work, click the map and walk the party to the cabin door.

**Starter code:**

```python
def move_left():
    pass


def move_right():
    pass


def move_up():
    pass


def move_down():
    pass
```

**Finished solution:**

```python
def move_left():
    party.move("left")


def move_right():
    party.move("right")


def move_up():
    party.move("up")


def move_down():
    party.move("down")
```

**Check names:** move_left steps left; move_right steps right; move_up steps up; move_down steps down

### Part `program-dialogue-prompt`

**Instructions shown to students:**

`get_dialogue_prompt_string()` returns the line Mar'tu says.
1. Change the words inside the quotes to a question Mar'tu asks Oogrish and Gearshift. The next two lines make it lower case and then capitalize the first letter.
2. Finish `present_dialogue_option()`: store the result of `get_dialogue_prompt_string()` in a variable.
3. Pass that variable to `print_prompt()`.
4. Press Run to see the line on the game screen.

**Starter code:**

```python
def get_dialogue_prompt_string():
    dialogue_input = "Write what Mar'tu asks here"
    dialogue_input = dialogue_input.lower()
    dialogue_input = dialogue_input.capitalize()
    return dialogue_input


def present_dialogue_option():
    pass
```

**Finished solution:**

```python
def get_dialogue_prompt_string():
    dialogue_input = "WHAT DO YOU REMEMBER ABOUT THE GREENROOM?"
    dialogue_input = dialogue_input.lower()
    dialogue_input = dialogue_input.capitalize()
    return dialogue_input


def present_dialogue_option():
    dialogue = get_dialogue_prompt_string()
    print_prompt(dialogue)
```

**Check names:** Mar'tu has a line; present_dialogue_option shows the line; the line is stored in a variable

### Part `program-dialogue-options`

**Instructions shown to students:**

`get_dialogue_input()` is already finished except for its four option strings.
The game runs `dialogue_option_selected()` whenever a box is clicked, and `user.clicked()` tells you which one.
1. Change the four option strings to things Oogrish could say back. The game shows them in the four boxes.
2. Replace each `<option>` with `"option 1"`, `"option 2"`, `"option 3"`, or `"option 4"` (keep the quotes), in order.
3. Add `make_option_green()` under each `speak_dialogue` line so the clicked box turns green.
4. Press Run.

**Starter code:**

```python
def get_dialogue_input():
    option_1 = "Write option 1 here"
    option_2 = "Write option 2 here"
    option_3 = "Write option 3 here"
    option_4 = "Write option 4 here"
    print_options(
        option_1.lower().capitalize(),
        option_2.lower().capitalize(),
        option_3.lower().capitalize(),
        option_4.lower().capitalize(),
    )


def dialogue_option_selected():
    if (user.clicked() == <option>):
        speak_dialogue("option 1")
    elif (user.clicked() == <option>):
        speak_dialogue("option 2")
    elif (user.clicked() == <option>):
        speak_dialogue("option 3")
    elif (user.clicked() == <option>):
        speak_dialogue("option 4")
```

**Finished solution:**

```python
def get_dialogue_input():
    option_1 = "We will help you."
    option_2 = "What is the decay?"
    option_3 = "Tell us about the clock."
    option_4 = "We need to rest first."
    print_options(
        option_1.lower().capitalize(),
        option_2.lower().capitalize(),
        option_3.lower().capitalize(),
        option_4.lower().capitalize(),
    )


def dialogue_option_selected():
    if (user.clicked() == "option 1"):
        speak_dialogue("option 1")
        make_option_green()
    elif (user.clicked() == "option 2"):
        speak_dialogue("option 2")
        make_option_green()
    elif (user.clicked() == "option 3"):
        speak_dialogue("option 3")
        make_option_green()
    elif (user.clicked() == "option 4"):
        speak_dialogue("option 4")
        make_option_green()
```

**Check names:** four replies are written; clicking option 1 speaks it and turns it green; clicking option 2 speaks it and turns it green; clicking option 3 speaks it and turns it green; clicking option 4 speaks it and turns it green

## Friends In Low Places (Module 2)

### Part `skill-checks`

**Instructions shown to students:**

A skill check rolls a die and compares the roll to the number needed to succeed.
1. Finish `perform_roll(die_size)`: replace `return 1` with `return random.randint(1, die_size)`. That gives a random whole number from 1 to `die_size`.
2. In each check, set `required_roll` to how hard that action should be, a number from 2 to 20.
3. In each check, replace `return False` with `return roll >= required_roll`, so the check succeeds when the roll is high enough.
4. Press Run.

**Starter code:**

```python
import random


def perform_roll(die_size):
    return 1


def strength_check(roll):
    # Prying the hatch open with brute force.
    required_roll = 0
    return False


def dexterity_check(roll):
    # Sliding a metal shim in to free the latch.
    required_roll = 0
    return False


def investigation_check(roll):
    # Finding the worn spot that pops the latch when you hit it.
    required_roll = 0
    return False
```

**Finished solution:**

```python
import random


def perform_roll(die_size):
    return random.randint(1, die_size)


def strength_check(roll):
    # Prying the hatch open with brute force.
    required_roll = 12
    return roll >= required_roll


def dexterity_check(roll):
    # Sliding a metal shim in to free the latch.
    required_roll = 15
    return roll >= required_roll


def investigation_check(roll):
    # Finding the worn spot that pops the latch when you hit it.
    required_roll = 9
    return roll >= required_roll
```

**Check names:** perform_roll rolls a die; strength_check succeeds from its required roll up; dexterity_check succeeds from its required roll up; investigation_check succeeds from its required roll up

### Part `spell-book`

**Instructions shown to students:**

Finish `add_spell()`.
1. In the `spell` dictionary, replace each placeholder with the matching parameter: `mana_cost`, `required_affinity`, and `spell_function`.
2. Replace the comment with one line that stores the spell in `spell_book`, using `spell_name` as the key: `spell_book[spell_name] = spell`.
3. Press Run.
The loop at the bottom is already written: it writes Strengthen Magic into every party member's spell book.
Notice that `strengthen_magic` is passed in without parentheses. We're handing over the function itself so the game can call it later, not calling it now.

**Starter code:**

```python
def strengthen_magic(caster):
    reinforce_barrier(caster)


def add_spell(spell_book, spell_name, mana_cost, required_affinity, spell_function):
    spell = {
        "mana_cost": 0,
        "required_affinity": 0,
        "spell_function": None,
    }
    # Store the spell in spell_book, using spell_name as the key


for member in party.members:
    add_spell(member["spell_book"], "Strengthen Magic", 10, 8, strengthen_magic)
```

**Finished solution:**

```python
def strengthen_magic(caster):
    reinforce_barrier(caster)


def add_spell(spell_book, spell_name, mana_cost, required_affinity, spell_function):
    spell = {
        "mana_cost": mana_cost,
        "required_affinity": required_affinity,
        "spell_function": spell_function,
    }
    spell_book[spell_name] = spell


for member in party.members:
    add_spell(member["spell_book"], "Strengthen Magic", 10, 8, strengthen_magic)
```

**Check names:** add_spell stores a spell under its name; the stored spell has the right values; a second spell keeps the first; every party member knows Strengthen Magic

### Part `mana-bars`

**Instructions shown to students:**

`print_mana()` at the top is already finished, so leave it as it is. The comments mark each line you need to change.
`get_mana_bar(caster)` builds a text bar from two kinds of blocks: a full block `█` for each point of mana the caster has, and a light block `░` for each point they've used.
1. Replace the first 0 with `caster["mana"]`.
2. Replace the second 0 with `caster["max_mana"] - caster["mana"]`.
3. Finish `show_mana(caster)` like `present_dialogue_option()` in Module 1: store the result of `get_mana_bar(caster)` in a variable.
4. Pass the caster and that variable to `print_mana()`.
5. Press Run.
The loop at the bottom shows every party member's bar.

**Starter code:**

```python
def print_mana(caster, mana_bar):
    # This function is already finished. You don't need to change it.
    # It draws mana_bar in this caster's row of the party panel.
    party.show_mana_bar(caster, mana_bar)


def get_mana_bar(caster):
    # Change this 0 to the caster's mana: caster["mana"]
    filled = "█" * 0
    # Change this 0 to the mana they've used: caster["max_mana"] - caster["mana"]
    empty = "░" * 0
    return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])


def show_mana(caster):
    # 1. Store the result of get_mana_bar(caster) in a variable.
    # 2. Pass the caster and that variable to print_mana().
    # Replace pass with those two lines.
    pass


for member in party.members:
    show_mana(member)
```

**Finished solution:**

```python
def print_mana(caster, mana_bar):
    # This function is already finished. You don't need to change it.
    # It draws mana_bar in this caster's row of the party panel.
    party.show_mana_bar(caster, mana_bar)


def get_mana_bar(caster):
    filled = "█" * caster["mana"]
    empty = "░" * (caster["max_mana"] - caster["mana"])
    return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])


def show_mana(caster):
    mana_bar = get_mana_bar(caster)
    print_mana(caster, mana_bar)


for member in party.members:
    show_mana(member)
```

**Check names:** 3 of 5 mana; empty and full bars; show_mana draws the bar once; the bar is stored in a variable

### Part `hold-the-barrier`

**Instructions shown to students:**

Write the rest of `cast_spell(caster, spell_name)` where the comments are, using an `if`, an `elif`, and an `else`.
1. If the caster's magical affinity, `caster["abilities"]["magical_affinity"]`, is lower than `spell["required_affinity"]`, call `print_prompt()` to say they aren't skilled enough.
2. Otherwise, if `caster["mana"]` is lower than `spell["mana_cost"]`, call `print_prompt()` to say they don't have enough mana.
3. Otherwise, call `spell["spell_function"](caster)`, subtract `spell["mana_cost"]` from `caster["mana"]`, and call `show_mana(caster)` so the bar updates.
4. Press Run.
Use `<` and not `<=`, because a caster with exactly enough mana can still cast.
`spell["spell_function"](caster)` works because the dictionary is holding a function: the parentheses on the end are what call it.

**Starter code:**

```python
def cast_spell(caster, spell_name):
    if spell_name not in caster["spell_book"]:
        print_prompt(caster["character_name"] + " doesn't know " + spell_name + ".")
        return
    spell = caster["spell_book"][spell_name]

    # 1. If the caster's magical affinity is lower than the spell's required affinity:
    #        print_prompt(caster["character_name"] + " isn't skilled enough to cast " + spell_name + ".")
    # 2. Otherwise, if the caster's mana is lower than the spell's mana cost:
    #        print_prompt(caster["character_name"] + " doesn't have enough mana to cast " + spell_name + ".")
    # 3. Otherwise: call the spell's function, subtract its mana cost, and show the new mana bar.
    pass
```

**Finished solution:**

```python
def cast_spell(caster, spell_name):
    if spell_name not in caster["spell_book"]:
        print_prompt(caster["character_name"] + " doesn't know " + spell_name + ".")
        return
    spell = caster["spell_book"][spell_name]

    if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:
        print_prompt(caster["character_name"] + " isn't skilled enough to cast " + spell_name + ".")
    elif caster["mana"] < spell["mana_cost"]:
        print_prompt(caster["character_name"] + " doesn't have enough mana to cast " + spell_name + ".")
    else:
        spell["spell_function"](caster)
        caster["mana"] = caster["mana"] - spell["mana_cost"]
        show_mana(caster)
```

**Check names:** a skilled caster with enough mana casts; the mana bar updates after a cast; too little affinity does not cast; too little mana does not cast; exactly enough mana still casts; the spell's own cost is used

## Concept inventory (what a student must be comfortable reading/writing)
- `def` functions with 0-5 parameters, `pass`, `return` (returning strings, booleans, computed values)
- calling functions and methods with string args: `party.move("left")`, `print_prompt(dialogue)`
- storing a function's return value in a variable, then passing that variable to another function
- string methods chained: `.lower()`, `.capitalize()`, `.lower().capitalize()`
- string concatenation with `+`, `str()` conversion, string repetition `"█" * n`
- comparison operators `==`, `<`, `>=`; returning a comparison (`return roll >= required_roll`)
- `if` / `elif` / `else` chains (4-branch elif chains on `user.clicked() == "option 1"`)
- `import random`, `random.randint(1, die_size)`
- dictionaries: literal with 3 keys, reading `d["key"]`, nested `caster["abilities"]["magical_affinity"]`, writing `book[name] = spell`, `in` / `not in` membership on dict keys
- a dictionary value that is a function, called as `spell["spell_function"](caster)`; passing a function without parentheses as an argument
- `for member in party.members:` looping over a list of dicts
- reassigning with arithmetic: `caster["mana"] = caster["mana"] - spell["mana_cost"]`
- early `return` inside an `if`
- reading 'engine helper' functions they did not write (print_prompt, print_mana, reinforce_barrier)

