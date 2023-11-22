import os
import time
from datetime import datetime
from typing import Literal

from pynput import keyboard
from win32gui import GetWindowText, GetForegroundWindow

from config import Input_Filepath, Input_Map, FPS

KC = keyboard.Controller()

os.system('')  # for console colors

Input_Map = {k.lower(): v for k, v in Input_Map.items()}  # Converts all keys to lowercase


def Pretty_Print(Text, Method: Literal['Default', 'Error']):
    for Line in Text.splitlines():
        Time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')

        r = 134
        g = 180
        b = 43

        if Method == 'Error':
            r = 175
            g = 6
            b = 6

        Color = f'\033[38;2;{r};{g};{b}m'

        Reset = '\033[0m'

        print(f'[{Color}{Time}{Reset}] {Line}')


def Read_Inputs():
    inputs = []

    try:
        open(Input_Filepath)
    except:
        Pretty_Print('Incorrect file path.', 'Error')
        os.system('pause>nul')
        quit()

    if Input_Filepath[-4:] != '.tas':
        Pretty_Print('File extension must be .tas', 'Error')
        os.system('pause>nul')
        quit()

    Repeat = False
    Repeat_Count = 1
    Repeating = []

    with open(Input_Filepath) as file:
        for line in file:
            line = line.strip()

            if line == '' or line.startswith('#') or line.startswith('0,'):
                continue

            if line.lower().startswith('repeat'):
                Repeat = True
                Repeat_Count = int(line.lower().removeprefix('repeat '))
                continue
            elif line.lower().startswith('endrepeat'):
                for _ in range(Repeat_Count - 1):
                    for i in Repeating:
                        inputs.append(i)
                Repeat = False
                Repeat_Count = 1
                Repeating = []
                continue

            duration, *keys = line.split(',')

            try:
                keys = {Input_Map[key.strip().lower()] for key in keys}
            except:
                Pretty_Print(f'Incorrect keybind used in inputs {keys}', 'Error')
                os.system('pause>nul')
                quit()

            if Repeat:
                Repeating.append((int(duration), keys))

            inputs.append((int(duration), keys))

    if Repeat is True:
        Pretty_Print('No EndRepeat after Repeat.', 'Error')
        os.system('pause>nul')
        quit()

    return inputs


def main():
    inputs = Read_Inputs()

    # Execute
    current_keys = set()

    Pretty_Print('Ready', 'Default')

    while GetWindowText(GetForegroundWindow()) != 'Strata':
        ...  # Waiting for you to switch to Strata
    time.sleep(0.2)

    for duration, keys in inputs:
        if GetWindowText(GetForegroundWindow()) != 'Strata':
            Pretty_Print('Tabbed out of Strata.', 'Error')
            os.system('pause>nul')
            quit()

        start_time = time.time()

        # Release old keys
        for key in current_keys - keys:
            KC.release(key)

        # Press new keys
        for key in keys - current_keys:
            KC.press(key)

        # Wait until current block ends
        target_time = start_time + duration / FPS

        while time.time() < target_time:
            time.sleep(0.001)

        current_keys = keys

        end_time = time.time()

        Time_Taken = (end_time - start_time) * FPS
        Pretty_Print(f'Input offset: {abs(duration - Time_Taken):.4f}s', 'Default')

    for key in current_keys:
        KC.release(key)

    Pretty_Print('Finished', 'Default')


if __name__ == '__main__':
    main()
