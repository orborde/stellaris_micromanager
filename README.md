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
