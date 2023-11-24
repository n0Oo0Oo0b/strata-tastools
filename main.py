import logging
import time
from pathlib import Path
from typing import Iterator

from colorlog import ColoredFormatter
from pynput import keyboard
from win32gui import GetWindowText, GetForegroundWindow

from config import INPUT_FILEPATH, INPUT_MAP, FPS

INPUT_MAP = {i.lower(): INPUT_MAP[i] for i in list(INPUT_MAP)}  # Converts keys to lowercase for case insensitivity

KeyType = str | keyboard.Key
InputKeyframeType = tuple[int, set[KeyType]]

#  Initializes colored logs (pure logging is only red ;-;)
LOG_FORMAT = '  %(log_color)s%(levelname)-7s%(reset)s | %(log_color)s%(message)s%(reset)s'
logging.root.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setFormatter(ColoredFormatter(LOG_FORMAT))
logging.root.addHandler(stream)


def try_int(num: str, fail_message: str) -> int:
    try:
        return int(num)

    except ValueError:
        logging.error(fail_message)
        raise


def parse_inputs(input_names: list[str], lineno: int) -> set[KeyType]:
    result = set()

    for name in input_names:
        if not name:
            continue

        key = INPUT_MAP.get(name)
        if key is None:
            logging.error(f"Invalid input name on line {lineno}: {name}")
            raise ValueError(f"Invalid input name: {name}")
        result.add(key)

    return result


def parse_lines(lines: Iterator[str]) -> list[InputKeyframeType]:
    result = []
    repeating_count: int = 0  # 0 for not repeating, [repeat count] for repeating
    current_repeat: list[InputKeyframeType] = []

    for lineno, line in enumerate(lines, 1):
        parts = [part.strip() for part in line.split(",")]

        match parts:
            case ():  # empty line
                continue

            case first, *_ if first.startswith("#"):
                continue

            case "REPEAT", count_str:
                if repeating_count:
                    logging.error("Nested repeats are not supported")
                    raise ValueError("Nested repeats are not supported")
                repeating_count = try_int(count_str, "Repeat count must be an integer")
                current_repeat = []

            case "ENDREPEAT", :
                result += current_repeat * repeating_count
                repeating_count = 0

            case duration_str, *input_names:
                duration = try_int(duration_str, "Duration must be an integer")
                inputs = parse_inputs(input_names, lineno)
                if not repeating_count:
                    result.append((duration, inputs))
                else:
                    current_repeat.append((duration, inputs))

    if repeating_count:
        logging.error("Unfinished REPEAT")
        raise ValueError("Unfinished REPEAT")

    return result


def read_inputs(fp: str | Path) -> list[InputKeyframeType]:
    path = Path(fp)
    if path.suffix != ".tas":
        logging.warning("File extension is not .tas")

    try:
        inputs = parse_lines(path.open())
    except (OSError, IOError) as e:
        logging.error(f"Error while reading input file: {e}")
        raise

    return inputs


def execute_inputs(inputs: list[InputKeyframeType]) -> None:
    # Execute
    logging.info('Ready')
    current_keys = set()
    total_duration = 0

    while GetWindowText(GetForegroundWindow()) != 'Strata':
        ...  # Waiting for you to switch to Strata
    time.sleep(0.2)

    start_time = time.time()
    controller = keyboard.Controller()
    for line, (duration, keys) in enumerate(inputs):
        if GetWindowText(GetForegroundWindow()) != 'Strata':
            logging.warning('Tabbed out of Strata, ending execution')
            break

        # Release old keys
        for key in current_keys - keys:
            controller.release(key)

        # Press new keys
        for key in keys - current_keys:
            controller.press(key)

        # Display offset
        current_time = total_duration / FPS
        actual_time = time.time() - start_time
        logging.info(f'Input offset: {current_time - actual_time:.4f}s (line {line + 1})')

        # Wait until current keyframe ends
        total_duration += duration
        end_time = start_time + total_duration / FPS

        while time.time() < end_time:
            time.sleep(0.001)

        current_keys = keys

    for key in INPUT_MAP.values():
        controller.release(key)

    logging.info('Finished')


def main() -> None:
    inputs = read_inputs(INPUT_FILEPATH)
    execute_inputs(inputs)


if __name__ == '__main__':
    main()
