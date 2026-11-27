#!/usr/bin/env python3

"""
test_mic.py

Hardware test for the USB microphone.

Purpose:
- Verify microphone detection.
- Verify audio recording.
- Optionally play back the recorded sample.
- Refer to the separate speaker test if playback fails
  or audio quality cannot be confirmed.

Expected Result:
- Microphone detected by ALSA.
- Recording succeeds.
- Playback and audio quality are reported separately.
- Playback issues do not cause the microphone test to fail.
"""

import subprocess
from pathlib import Path
import sys


OUTPUT_FILE = "mic_test.wav"
MIC_DEVICE = "plughw:CARD=Device,DEV=0"
PLAYBACK_DEVICE = "plughw:2,0"


def check_audio_device():
    print("Checking recording devices...")

    result = subprocess.run(
        ["arecord", "-l"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("FAIL: Unable to query recording devices.")
        print(result.stderr)
        return False

    print("PASS: Recording devices detected.\n")
    print(result.stdout)

    return True


def record_audio():
    print("Recording 3-second audio sample...")
    print("Format: 16 kHz, Mono, 16-bit LE")

    result = subprocess.run(
        [
            "arecord",
            "-D", MIC_DEVICE,
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "1",
            "-d", "3",
            OUTPUT_FILE,
        ]
    )

    return result.returncode == 0


def playback_audio():
    print("Playing recorded sample...")

    result = subprocess.run(
        [
            "aplay",
            "-D", PLAYBACK_DEVICE,
            OUTPUT_FILE,
        ]
    )

    return result.returncode == 0


def verify_recording():
    print("\nManual Verification Required")
    print("Was the recording understandable?")
    print("Enter 'y' or 'n'.")

    while True:
        answer = input("> ").strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False


def main():
    print("===================================")
    print(" USB Microphone Hardware Test")
    print("===================================")
    print()

    device_detected = check_audio_device()

    recording_ok = False
    playback_ok = False
    audio_quality_ok = False

    if device_detected:
        recording_ok = record_audio()

        if recording_ok and Path(OUTPUT_FILE).is_file():
            playback_ok = playback_audio()

            if playback_ok:
                audio_quality_ok = verify_recording()

                if not audio_quality_ok:
                    print(
                        "\nNOTICE: Audio quality could not be confirmed. "
                        "Please run the separate speaker test "
                        "to check audio output."
                    )
            else:
                print(
                    "\nNOTICE: Playback failed. "
                    "Please run the separate speaker test "
                    "to check audio output."
                )

    overall_pass = device_detected and recording_ok

    print("\n=== Test Summary ===")
    print(
        f"Device detected: {'PASS' if device_detected else 'FAIL'}"
    )
    print(
        f"Recording: {'PASS' if recording_ok else 'FAIL'}"
    )
    print(
        f"Playback check: {'PASS' if playback_ok else 'FAIL'}"
    )
    print(
        f"Audio quality: {'PASS' if audio_quality_ok else 'FAIL'}"
    )
    print(
        f"Overall Result: {'PASS' if overall_pass else 'FAIL'}"
    )

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    raise SystemExit(main())
