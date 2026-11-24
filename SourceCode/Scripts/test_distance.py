#!/usr/bin/env python3

import time
import board
import busio
import adafruit_vl53l0x

# Measurement interval in seconds
READ_INTERVAL = 0.5


def main():
	print("Initializing VL53L0X...")

	try:
		# Initialize I2C bus
		# SDA = GPIO2 Pin 3
		# SCL = GPIO3 Pin 5
		i2c = busio.I2C(board.SCL, board.SDA)

		# Initialize sensor (default I2C address: 0x29)
		sensor = adafruit_vl53l0x.VL53L0X(i2c)

		print("VL53L0X detected.")
		print("Starting distance measurement...(Ctrl+C to stop)\n")

		while True:
			try:
				# Read distance in millimeters
				distance_mm = sensor.range

				# Convert to centimeters
				distance_cm = distance_mm / 10.0

				# Timestamp for troubleshooting
				timestamp = time.strftime("%H:%M:%S")

				print(
					f"[{timestamp}]"
					f"RAW={distance_mm:4d} mm | "
					f"{distance_cm:5.1f} cm"
				)
			except OSError as e:
				print(f"[I2C ERROR] {e}")

			except RuntimeError as e:
				print(f"[SENSOR ERROR] {e}")

			time.sleep(READ_INTERVAL)

	except KeyboardInterrupt:
		print("\nMeasurement stopped.")
	
	except Exception as e:
		print(f"Initialization failed: {e}")

if __name__=="__main__":
	main()

