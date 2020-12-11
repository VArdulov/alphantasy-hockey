# Notebooks

## Creating a League

This file has a notebook that will create a synthetic hockey league with
fake hockey players and then assigns a large subset of the player.

These files generate a number of output CSV files, one will be a set of
schedules for 5 seasons that tell you the date that different teams play
one another. The other is a list of players that tells you their average
expected performance.

**To-do**:
1. Come up with a way to simulate trading between teams and add/drop behavior
   1. trading
   2. signing
   3. drafting (create a new set of players to add for each following season)

2. Develop a method to change the underlying statistics (degrade or improved players).
   1. This may require constructing age and trying to "simulate" related improvement/etc


## Simulating the Season

This file outlines the code necessary to simulate a single game and generate
a bunch of game_reports that are also saved as CSV files in the simulated-data.
The game reports are stored as dataframes that list every player involved and the
number of points/hits/blocks each player scored or gamestarts/

The `simulate_a_game` and `game_day_performance` functions will probably
be refactored to live in the alphantasy sub-module instead.

**To-Do**:
1. Come up with a way to mimic/simulate goalie swaps in the game to generate
the stats for goalies that might not have started but maybe came into the game

## Future Work:

**To-Do** *(most likely in a separate notebook)*:
1. Generate some plots about the progression of the season for players
2. Generate end of season standings and summary reports
3. See if you can compute individual player advance stats (like WAR) and others
4. Design the "fantasy" league now that can track and reward and simulates the head-to-head match ups on a weekly basis