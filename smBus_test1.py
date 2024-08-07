from smbus2 import SMBus

# open i2c bus and read one byte from address 0x40, offset 0
bus = SMBus(1) # i2cdetect -r -y 1 shows 0x40 is good... 

b = bus.read_byte_data(0x40,0)
print(b)

bus.close()

