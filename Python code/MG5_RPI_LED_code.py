import serial                  # Library used for UART / serial communication
import time                    # Library used for implementing timing delays
import RPi.GPIO as GPIO        # Library used for controlling Raspberry Pi GPIO pins

GPIO.setwarnings(False)        # Ignore GPIO warnings
GPIO.setmode(GPIO.BCM)         # Use BCM GPIO numbering

GP2_LED = 26                # GP2 LED indicates GPS fix available
GP1_LED = 6                   # GP1 LED indicates no GPS fix

GPIO.setup(GP2_LED, GPIO.OUT, initial=GPIO.LOW)  # Set GPIO 26 as output and OFF
GPIO.setup(GP1_LED, GPIO.OUT, initial=GPIO.LOW)    # Set GPIO 6 as output and OFF

serial_port = serial.Serial('/dev/serial0', 115200) # Establish UART serial connection to the GNSS receiver

# /dev/serial0 refers to the primary Raspberry Pi UART interface
# 115200 baud is the default communication speed of the mosaic-G5 receiver

# If using USB serial communication instead of UART, the device may appear as:
# /dev/ttyACM0, /dev/ttyACM1, etc.
# Available serial devices can be checked using:
# dmesg | grep tty

# If permission errors occur when accessing USB serial ports, run:
# sudo chmod 666 /dev/ttyACM0

time.sleep(1)                                          # Delay for serial connection to initialise properly

serial_port.write(b'SSSSSSSSSSSSS\n')                  # Send multiple 'S' characters to place the mosaic-G5 into command mode

time.sleep(0.1)                                        # Short delay to ensure the command is processed

serial_port.write(b'sno, Stream1, COM1, GGA, sec1\n') # Enable continuous NMEA GGA message streaming once per second on COM1

time.sleep(0.1)                                        # Delay for reading incoming serial data

try:

    while True:

        nmea_data_bytes = serial_port.readline()       # Read one complete line of incoming serial data
        nmea_sentence = str(nmea_data_bytes.decode())  # Decode received byte data into a UTF-8 string
        nmea_sentence = nmea_sentence.rstrip()         # Remove newline and whitespace characters

        if (nmea_sentence.startswith('$GNGGA')):       # Check if the received NMEA sentence is a GNGGA position message

            nmea_fields = [element.strip() for element in nmea_sentence.split(',')]  # Separate NMEA fields into a list

            try:
                quality_indicator = int(nmea_fields[6])  # Get the NMEA quality indicator field
            except (ValueError, IndexError):
                continue                                 # Ignore malformed GGA messages

            if quality_indicator == 0:                   # Quality indicator value of 0 means no valid GNSS position fix

                print("No GPS Fix Available!")

                GPIO.output(GP1_LED, GPIO.HIGH)         # Turn GP1 LED ON
                GPIO.output(GP2_LED, GPIO.LOW)        # Turn GP2 LED OFF

            else:

                GPIO.output(GP1_LED, GPIO.LOW)          # Turn GP1 LED OFF
                GPIO.output(GP2_LED, GPIO.HIGH)       # Turn GP2 LED ON
               

                utc_time = float(nmea_fields[1])        # Parse UTC time field from the NMEA GGA message

                latitude = float(nmea_fields[2]) * 0.01 # Get latitude value in NMEA format
                latitude_direction = nmea_fields[3]     # Get latitude hemisphere indicator (N or S)

                longitude = float(nmea_fields[4]) * 0.01 # Get longitude value in NMEA format
                longitude_direction = nmea_fields[5]     # Get longitude hemisphere indicator (E or W)

                altitude = float(nmea_fields[9])        # Get altitude above mean sea level
                altitude_unit = nmea_fields[10]         # Get altitude unit, typically metres (M)

                print('UTC Time: ' + str(utc_time))     # Display UTC time
                print(' Latitude: ' + str(latitude) + latitude_direction)  # Display latitude
                print(' Longitude: ' + str(longitude) + longitude_direction)  # Display longitude
                print(' Height: ' + str(altitude) + altitude_unit)  # Display altitude

            time.sleep(0.1)                             # Delay before processing the next incoming message

        else:
            continue                                    # Ignore non-GGA NMEA messages and continue listening

except KeyboardInterrupt:

    print("\nProgram stopped by user.")

finally:

    GPIO.output(GP2_LED, GPIO.LOW)                   # Turn GP2 LED OFF
    GPIO.output(GP1_LED, GPIO.LOW)                     # Turn GP1 LED OFF

    GPIO.cleanup()                                     # Release GPIO resources
    serial_port.close()                                # Close serial connection

    print("GPIO cleaned up and serial port closed.")