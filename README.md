# strata-tastools

A simple TAS script for [Strata](https://leomca.itch.io/strata) that I made in 20 minutes.
(Also, join our [discord](https://discord.gg/vJhYA9FbAw))

Scripts are formatted like so:

```tas
# this is a comment
[duration],[button1],[button2],etc.

# press jump for 10f
10,J

# overlapping inputs
5,D
5,D,S
15,S

# repeating inputs
Repeat,5
1,R,D
15,R,S
1,R,J
10,R
EndRepeat
# will repeat the inputs between repeat and endrepeat 5 times (case insensitive)

# 0 frame inputs will be ignored
0,R
```

## How to run

1. Clone the project
2. `cd` into project root
3. Change config (in [config.py](config.py)) to your liking (see config section)
4. `python main.py`
5. When `Ready` appears, tab into the game (I know, very sophisticated)
6. Enjoy

## Config

- `Input_Filepath` - Filepath of input file to run. Or just use `0` and pipe the input into stdin like I do.
- `Input_Map` - In-game controls go here.
- `FPS` - Framerate to run at. Keep this at 144.
