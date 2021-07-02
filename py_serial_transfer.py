import serial
import time

target_dongle_mac_address = (
    "[0]40:48:FD:E5:2D:AF"  # Change this to the peripheral's mac address.
)
your_com_port = "COM25"  # Change this to the com port your dongle is connected to.

connecting_to_dongle = True
trying_to_connect = False
file_name = "test.txt"

print("Connecting to dongle...")
# Trying to connect to dongle until connected. Make sure the port and baudrate is the same as your dongle.
# You can check in the device manager to see what port then right-click and choose properties then the Port Settings
# tab to see the other settings
while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0,
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

print("Connected to Dongle.")

connected = "0"
while 1 and console.is_open.__bool__():
    console.write(str.encode("AT+DUAL"))
    console.write("\r".encode())
    time.sleep(0.1)
    print("Putting dongle in Dual role and trying to connect to other dongle.")
    while connected == "0":
        time.sleep(0.5)
        if not trying_to_connect:
            console.write(str.encode("AT+GAPCONNECT="))
            console.write(str.encode(target_dongle_mac_address))
            console.write("\r".encode())
            trying_to_connect = True
        dongle_output2 = console.read(console.in_waiting)
        time.sleep(2)
        print("Trying to connect to Peripheral...")
        if not dongle_output2.isspace():
            if dongle_output2.decode().__contains__("\r\nCONNECTED."):
                connected = "1"
                print("Connected!")
                time.sleep(10)
            if dongle_output2.decode().__contains__("\r\nDISCONNECTED."):
                connected = "0"
                print("Disconnected!")
                trying_to_connect = False
            dongle_output2 = " "
    while connected == "1":
        dongle_output3 = console.read(console.in_waiting)
        want_to_exit = input(
            "Press Enter to start sending file or 'exit' to quit script.\n\r>> "
        )
        want_to_exit = want_to_exit.upper()
        if "EXIT" in want_to_exit:
            print("Exiting script...")
            exit()
        hex_to_send = ""
        fo2 = open(file_name, "rb")
        print("Sending file. Please wait...")
        while (byte := fo2.read(1)) :
            hex_to_send += byte.hex().upper()
            if len(hex_to_send) >= 200:
                # my_dongle.at_spssend(hex_to_send)
                console.write(str.encode("AT+SPSSEND=" + hex_to_send + "\r"))
                time.sleep(0.2)
                hex_to_send = ""
        if len(hex_to_send) != 0:
            # my_dongle.at_spssend(hex_to_send)
            console.write(str.encode("AT+SPSSEND=" + hex_to_send + "\r"))
            time.sleep(0.2)
        fo2.close()
        console.write(str.encode("AT+SPSSEND=[DONE]\r"))
        print("File transfer complete!\r\n")
        print("Exiting script...")
        exit()
