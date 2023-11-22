from pynput.keyboard import Key

INPUT_FP = 0
INPUT_MAP = {
    # in order: Left, Right, Dash, Slide, Jump, Respawn, Reset
    "L": Key.left,
    "R": Key.right,
    "D": "z",
    "S": "x",
    "J": "c",
    "K": "r",
    "RESET": Key.esc,
}
FPS = 60
