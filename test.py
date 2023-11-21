import serial

serial_port = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)


while True:
    data = serial_port.read()
    dist_reading = data.decode("utf-8")
    dist_int = 0
    while data != "\r".encode():
        data = serial_port.read()
        # print(data)
        dist_reading += data.decode("utf-8")
        # print(data.decode("utf-8"))
                        

    # dist_reading = dist_reading[:-1]
    dist_int = int(dist_reading)
    print(dist_int)