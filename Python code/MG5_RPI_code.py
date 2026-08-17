import serial   # Library used for UART / serial communication
import time     # Library used for implementing timing delays

serial_port = serial.Serial('/dev/serial0', 115200) #Establish UART serial connection to the GNSS receiver

# /dev/serial0 refers to the primary Raspberry Pi UART interface
# 115200 baud is the default communication speed of the mosaic-G5 receiver

# If using USB serial communication instead of UART, the device may appear as:
# /dev/ttyACM0, /dev/ttyACM1, etc.
# Available serial devices can be checked using:
# dmesg | grep tty

# If permission errors occur when accessing USB serial ports, run:
# sudo chmod 666 /dev/ttyACM0

time.sleep(1)                                          # delay for serial connection time to be initialise properly

serial_port.write(b'SSSSSSSSSSSSS\n')                  # Send multiple 'S' characters to place the mosaic-G5 into command mode

time.sleep(0.1)                                        # Short delay to ensure the command is processed

# Enable continuous NMEA GGA message streaming once per second on COM1
# For USB communication, replace COM1 with USB1 or USB2
serial_port.write(b'sno, Stream1, COM1, GGA, sec1\n')

time.sleep(0.1)                                         # delay for reading incoming serial data

while True:

   
    nmea_data_bytes = serial_port.readline()            # Read one complete line of incoming serial data from the receiver  
    nmea_sentence = str(nmea_data_bytes.decode())       # Decode received byte data into a UTF-8 string   
    nmea_sentence = nmea_sentence.rstrip()              # Remove newline and whitespace characters

    # Check if the received NMEA sentence is a GNGGA position message
    if (nmea_sentence.startswith('$GNGGA')):

        nmea_fields = [element.strip() for element in nmea_sentence.split(',')]  #separated NMEA fields with a comma into a list
        quality_indicator = int(nmea_fields[6])            #Get the NMEA quality indicator field

        # Quality indicator value of 0 means no valid GNSS position fix
        if quality_indicator==0:

            print("No GPS Fix Available!")

        else:

            utc_time = float(nmea_fields[1])             # Parse UTC time field from the NMEA GGA message
            
            latitude = float(nmea_fields[2])*0.01        # Get latitude value in NMEA format
            latitude_direction = nmea_fields[3]          # Get latitude hemisphere indicator (N or S)
            
            longitude = float(nmea_fields[4])*0.01       # Get longitude value in NMEA format
            longitude_direction = nmea_fields[5]         # Get longitude hemisphere indicator (E or W)

            altitude = float(nmea_fields[9])             # Get altitude above mean sea level            
            altitude_unit = nmea_fields[10]              # Get altitude unit, typically metres (M)

            # Display parsed GNSS positioning information
            print('UTC Time: ' + str(utc_time))
            print(' Latitude: ' + str(latitude) + latitude_direction)
            print(' Longitude: ' + str(longitude) + longitude_direction)
            print(' Height: ' + str(altitude) + altitude_unit)  
                    
        time.sleep(0.1)                                  # Delay before processing the next incoming message

    else:
        continue                                         # Ignore non-GGA NMEA messages and continue listening

serial_port.close()                                      # Close serial connection when the program terminates
