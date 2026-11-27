#!/usr/bin/env python3

"""
test_speaker.py

Hardware test for the audio output device.

Purpose:
- Verify that the speaker output device is available.
- Verify that ALSA can open the playback device.
- Verify successful playback of a test sound.

Expected Result:
- Playback device is detected.
- ALSA test sound is played successfully.
- Audio is clearly audible without distortion or noise.
"""

import subprocess
import sys


PLAYBACK_DEVICE = "hw:2,0"
TEST_FILE = "/usr/share/sounds/alsa/Front_Center.wav"


def check_playback_device():
    """
    Check whether ALSA detects playback devices.
    """

    print("Checking playback devices...")

    result = subprocess.run(
        ["aplay", "-l"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("FAIL: Unable to query playback devices.")
        return False

    print("PASS: Playback devices detected.\n")
    print(result.stdout)

    return True


def play_test_sound():
    """
    Play ALSA test sound through the selected device.
    """

    print("Playing ALSA test sound...")
    print(f"Device: {PLAYBACK_DEVICE}")

    result = subprocess.run(
        [
            "aplay",
            "-D",
            PLAYBACK_DEVICE,
            TEST_FILE,
        ]
    )

    if result.returncode == 0:
        print("PASS: ALSA playback completed successfully.")
        return True

    print(f"FAIL: Playback failed (exit code {result.returncode}).")
    return False


def verify_audio_output():
    """
    Ask the user whether the sound was audible.
    """

    print("\nManual Verification Required")
    print("Did you hear the test sound through the speaker?")
    print("Enter 'y' for yes or 'n' for no.")

    while True:
        response = input("> ").strip().lower()

        if response in ("y", "yes"):
            return True

        if response in ("n", "no"):
            return False

        print("Please enter 'y' or 'n'.")


def main():

    print("===================================")
    print(" Speaker Hardware Test")
    print("===================================")
    print()
    print("Test Objective:")
    print("- Verify playback device detection")
    print("- Verify ALSA audio playback")
    print("- Verify speaker functionality")
    print()

    device_detected = check_playback_device()

    if not device_detected:
        print("\n=== Test Summary ===")
        print("Playback device detected: FAIL")
        print("ALSA playback: NOT TESTED")
        print("Audible sound: NOT TESTED")
        print("Overall Result: FAIL")
        return

    playback_ok = play_test_sound()

    audible_sound = False

    if playback_ok:
        audible_sound = verify_audio_output()

    print("\n=== Test Summary ===")
    print(
        f"Playback device detected: {'PASS' if device_detected else 'FAIL'}"
    )
    print(
        f"ALSA playback: {'PASS' if playback_ok else 'FAIL'}"
    )
    print(
        f"Audible sound: {'PASS' if audible_sound else 'FAIL'}"
    )

    overall_pass = (
        device_detected
        and playback_ok
        and audible_sound
    )

    print(
        f"Overall Result: {'PASS' if overall_pass else 'FAIL'}"
    )
    
    sys.exit(0 if overall_pass else 1)

if __name__ == "__main__":
    main()
