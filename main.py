import os
from pathlib import Path
import time
import logging

from pynput import keyboard
from win32gui import GetWindowText, GetForegroundWindow

from config import INPUT_FILEPATH, INPUT_MAP, FPS

KC = keyboard.Controller()

os.system('')  # for console colors

Input_Map = {k.lower(): v for k, v in INPUT_MAP.items()}  # Converts all keys to lowercase

LOG_FORMAT = "[%(asctime)s %(levelname)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logging.info("Logger initialized")


def read_inputs(fp: str | Path):
    path = Path(fp)
    if path.suffix != ".tas":
        logging.warning("File extension is not .tas")

    try:
        path.open()
    except (OSError, IOError) as e:
        logging.error(f"Error while reading input file: {e}")
        raise

    inputs = []
    repeat = False
    repeat_count = 1
    repeating_block = []

    with path.open() as file:
        for line in file:
            line = line.strip()

            if line == '' or line.startswith('#') or line.startswith('0,'):
                continue

            if line.lower().startswith('repeat'):
                repeat = True
                repeat_count = int(line.lower().removeprefix('repeat '))
                continue
            elif line.lower().startswith('endrepeat'):
                for _ in range(repeat_count - 1):
                    for i in repeating_block:
                        inputs.append(i)
                repeat = False
                repeat_count = 1
                repeating_block = []
                continue

            duration, *keys = line.split(',')

            try:
                keys = {INPUT_MAP[key.strip().lower()] for key in keys}
            except:
                logging.error(f'Incorrect keybind used in inputs {keys}')
                os.system('pause>nul')
                quit()

            if repeat:
                repeating_block.append((int(duration), keys))

            inputs.append((int(duration), keys))

    if repeat:
        logging.error('No EndRepeat after Repeat.')
        os.system('pause>nul')
        quit()

    return inputs


def main():
    inputs = read_inputs(INPUT_FILEPATH)

    # Execute
    current_keys = set()

    logging.info('Ready')

    while GetWindowText(GetForegroundWindow()) != 'Strata':
        ...  # Waiting for you to switch to Strata
    time.sleep(0.2)

    for duration, keys in inputs:
        if GetWindowText(GetForegroundWindow()) != 'Strata':
            logging.warning('Tabbed out of Strata.')
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
        logging.info(f'Input offset: {abs(duration - Time_Taken):.4f}s')

    for key in current_keys:
        KC.release(key)

    logging.info('Finished')


if __name__ == '__main__':
    main()
