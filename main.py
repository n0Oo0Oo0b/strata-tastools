import time

from pynput import keyboard

from config import INPUT_FP, INPUT_MAP, FPS


KC = keyboard.Controller()


def main():
    # Read input
    inputs = []
    with open(INPUT_FP) as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                continue
            duration, *keys = line.split(",")
            keys = {INPUT_MAP[key.strip()] for key in keys}
            inputs.append((int(duration), keys))
    inputs.append((0, set()))  # Release all keys at the end

    # Execute
    current_frame = 0
    current_keys = set()
    print("Ready")
    time.sleep(2)  # Delay to switch windows
    start_time = time.time()
    for duration, keys in inputs:
        # Release old keys
        for key in current_keys - keys:
            KC.release(key)
        # Press new keys
        for key in keys - current_keys:
            KC.press(key)
        # Wait until current block ends
        current_frame += duration
        target_time = start_time + current_frame / FPS
        while time.time() < target_time:
            time.sleep(0.001)
        current_keys = keys
    print("Done")


if __name__ == '__main__':
    main()
