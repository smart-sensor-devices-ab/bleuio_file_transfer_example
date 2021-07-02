import serial
import time

your_com_port = "COM6"  # Change this to the com port your dongle is connected to.
file_name = "result.png"  # Change this to match the file type you are recieving

connecting_to_dongle = True
trying_to_connect = False

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

file_data = ""
file_transfer_done = False
connected = "0"
line = ""
while 1 and console.is_open.__bool__() or not file_transfer_done:
    console.write(str.encode("AT+DUAL"))
    console.write("\r".encode())
    print("Putting dongle in Dual role.")
    time.sleep(0.1)
    console.write(str.encode("AT+ADVSTART"))
    console.write("\r".encode())
    time.sleep(0.1)
    print("Starting advertising and awaiting connection from other dongle...")
    while connected == "0":
        dongle_output2 = console.read(console.in_waiting)
        time.sleep(2)
        if not dongle_output2.isspace():
            if dongle_output2.decode().__contains__("\r\nCONNECTED."):
                connected = "1"
                print("Connected!")
            if dongle_output2.decode().__contains__("\r\nDISCONNECTED."):
                connected = "0"
                print("Disconnected!")
            dongle_output2 = " "
    while connected == "1" or not file_transfer_done:
        time.sleep(0.2)
        dongle_output3 = console.read(console.in_waiting)
        if not dongle_output3.isspace():
            if dongle_output3.__contains__(str.encode("\r\nDISCONNECTED.")):
                print("Disconnected!")
                connected = "0"
            elif dongle_output3.__contains__(str.encode("[DONE]")):
                file_transfer_done = True
                print("File transfer complete!\r\n")
                fo = open(file_name, "wb")
                hex = bytes.fromhex(file_data)
                fo.write(hex)
                fo.close()
                print("Exiting script...")
                exit()
            elif dongle_output3.__contains__(str.encode("[Received]:")):
                line = dongle_output3.decode()
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                line = line.replace("[Received]:", "")
                line = line.replace(" ", "")
                file_data += line
                print(line)
            dongle_output3 = ""
        msg = ""