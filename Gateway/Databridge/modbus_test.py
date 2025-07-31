from pymodbus.client import ModbusSerialClient as ModbusClient
import pymodbus
import logging

import elements.Parser as Parser
pymodbus.pymodbus_apply_logging_config(logging.DEBUG)

client = ModbusClient(method='rtu', port='COM5', baudrate=38400, timeout=5, retry_on_empty=True, retries=3, debug=True, stopbits=2)

client.connect()
rr = client.read_input_registers(100, 3, slave=3)
#Address is register address e.g 30222,
#and count is number of registers to read,
#so it will read values of register 30222 to 30232
#unit is slave address, for 1 device leave it 1

#data=read.registers[int(2)] #reading register 30223
print(rr.registers) #printing value read in above line

abc = Parser.ModbusParser.parse(rr.registers, "int")
print(abc)

