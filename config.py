from pynput.keyboard import Key

INPUT_FILEPATH = ''
INPUT_MAP = {
    'L': 'a',  # Left
    'R': 'd',  # Right
    'D': 'i',  # Dash
    'S': 's',  # Slide
    'J': Key.space,  # Jump
    'K': 'r',  # Respawn
    'RESET': Key.esc,  # Reset
}
FPS = 144  # 144 Recommended
