Stellaris involves a lot of micromanagement that's pretty mechanical. This repo is a pile of awful hacks to make a computer deal with it.

The closest thing Stellaris has to a general-purpose API is its savegame format, so that's what this tooling ingests.

# How do I run it?

## One-off
```
ed check.py  # Edit the script to point TARGET_COUNTRIES at the player-controlled countries you want to analyze
go build sav2json.go
./sav2json -infile autosave_2241.04.01.sav > gamestate.json
./check.py gamestate.json
```

`sav2json` uses an ANTLR-generated parser to convert to a _regrettable_ JSON format. `check.py` ingests said JSON to analyze the game state for some tedious-to-keep-track-of problems and prints out any that need addressing.

## Monitoring while you play

```
ed check.py  # Edit the script to point TARGET_COUNTRIES at the player-controlled countries you want to analyze
go build sav2json.go
nice -n19 ./autosave_poller.py $STELLARIS_SAVE_FOLDER/mpinterstellarorchorde2_1013776793/ 1
```

This script watches the savegame directory for new autosaves, and reruns the toolchain when it sees one.

Set Stellaris to autosave monthly. It doesn't matter whether "Save to Cloud" is enabled; this only affects the save game folder path you need to point the poller at.

# Feature ideas

* Detect research agreement participants researching the same technology simultaneously ✔️
* Agreement checks️
  * Artisan troupe
    * Patron deal ✔
    * Festival of Worlds ✔
    * Monuments
      * All purchased
      * All exhibited
  * Curator order ✔️
* Scientist misallocation
* Underdeveloped claimed systems
* Election influence budget
  * When is your next election?
  * More importantly: are you on track to have enough influence?
  * How much influence can you safely spend?
* Advanced job allocation
  * Detect pointless job usages
  * Resource stockpile full
  * Too many bureaucrats
* Corporate empires
  * Branch office candidates
  * Commercial pact prospects
* Can you analyze
  * the market?
    * Overselling from autobuys
    * Autobuys that are NOPping because you're resource-capped
  * Diplomacy
    * prospective commercial pacts?
    * prospective trade deals?
    * prospective research agreements? (mostly care about coarse relative tech and acceptancy)
* Allied economic analysis (by agreement, of course!)
* Leader pool monitoring
  * Spark of Genius
  * Scientist specialties
* Planet administrivia
  * Machine assembly plants not built
  * Available capital upgrade
  * (if enabled) distribute luxury goods reminders?
  * Optimal planet designation
* Colonization targets in your space
* (if you can figure out how to _write_ the save format) Modify save to have an optimal setup
  * Meticulous scientists
  * Scientists with the optimal specialties for the "make research faster" techs
