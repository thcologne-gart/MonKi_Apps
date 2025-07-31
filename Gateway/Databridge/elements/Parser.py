import datetime
from enum import Enum
from typing import Type

import requests
import BAC0
from bacpypes.basetypes import *

datatypes = [
    "BOOL",
    "BYTE",
    "DATE",
    "DINT",
    "DWORD",
    "INT",
    "LINT",
    "LREAL",
    "LWORD",
    "REAL",
    "SINT",
    "STRING",
    "TIME",
    "TIME_OF_DAY",
    "UDINT",
    "UINT",
    "ULINT",
    "USINT",
    "WORD",
    "WSTRING"
]
datatypes_grouped = {
    "bool": ["BOOL"],
    "int": ["DINT", "LINT", "INT", "SINT"],
    "uint": ["UDINT", "UINT", "USINT", "ULINT"],
    "float": ["REAL", "LREAL"],
    "datetime": ["TIME_OF_DAY", "TIME", "DATE"],
    "str": ["WSTRING", "STRING"],
    "enum": ["DWORD", "WORD", "LWORD"],
    "byte": ["BYTE"]
}


class BACnetParser:
    @staticmethod
    def parse(object_to_parse):
        if isinstance(object_to_parse, list):
            new_list = []
            for obj in object_to_parse:
                new_list.append(BACnetParser.parse(obj))
            return new_list
        elif isinstance(object_to_parse, (TimeStamp, DateTime)):
            return BACnetParser._parse_timestamp(object_to_parse)
        elif isinstance(object_to_parse, (Date, Time)):
            return BACnetParser._parse_atomic(object_to_parse)

        elif issubclass(object_to_parse.__class__, (Choice, Sequence)):
            return BACnetParser._replace_bytearrays(object_to_parse.dict_contents())

        #elif issubclass(object_to_parse.__class__, (Choice, Sequence)):
        #    return object_to_parse.dict_contents()
        else:
            return object_to_parse

    @staticmethod
    def _replace_bytearrays(obj: dict):
        new_dict = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                new_dict.__setitem__(key, BACnetParser._replace_bytearrays(value))
            elif isinstance(value, bytearray):
                hex_string = ""
                for b in value:
                    hex_value = str(hex(b)).replace("0x", "")
                    hex_string += hex_value + ":" if len(hex_value) == 2 else "0" + hex_value + ":"
                hex_string = hex_string[:-1]
                new_dict.__setitem__(key, hex_string)
            else:
                new_dict.__setitem__(key, value)
        return new_dict

    @staticmethod
    def _parse_atomic(timestamp: Date | Time):
        name = timestamp.__class__.__name__.lower()
        if name == "time":
            return BACnetParser._parse_time({name: timestamp.value})
        elif name == "date":
            return BACnetParser._parse_date({name: timestamp.value})

    @staticmethod
    def _parse_timestamp(timestamp: Choice):
        dict_contents = timestamp.dict_contents()
        if "dateTime" in dict_contents.keys():
            return BACnetParser._parse_datetime(dict_contents)
        elif "time" in dict_contents.keys():
            return BACnetParser._parse_time(dict_contents)
        elif "sequenceNumber" in dict_contents.keys():
            return BACnetParser._parse_sequence_number(dict_contents)

    @staticmethod
    def _parse_datetime(dict_: dict):
        date_dict = {"date": dict_["dateTime"]["date"]}
        time_dict = {"time": dict_["dateTime"]["time"]}
        date = BACnetParser._parse_date(date_dict)
        time = BACnetParser._parse_time(time_dict)
        if time is None:
            return date
        return datetime.datetime.combine(date, time)

    @staticmethod
    def _parse_time(dict_: dict):
        tuple_ = dict_.__getitem__("time")
        try:
            time = datetime.time(hour=tuple_[0], minute=tuple_[1], second=tuple_[2], microsecond=tuple_[3])
        except ValueError:
            time = None
        return time

    @staticmethod
    def _parse_date(dict_: dict):
        tuple_ = dict_.__getitem__("date")
        try:
            date = datetime.date(year=tuple_[0], month=tuple_[1], day=tuple_[2])
        except ValueError:
            date = None
        return date

    @staticmethod
    def _parse_sequence_number(dict_: dict):
        return int(dict_.__getitem__("sequenceNumber"))

    @staticmethod
    def _parse_cov_subscription(cov_subscription: COVSubscription):
        return cov_subscription.dict_contents()

def test_bacnet_parser():
    bacnet = BAC0.connect()
    time_stamp = bacnet.read("139.6.140.136 device 13 lastRestoreTime")
    #time_stamp = bacnet.read("139.6.140.136 device 13 timeOfDeviceRestart")
    #time_stamp = TimeStamp(sequenceNumber=17)
    date_time = bacnet.read("139.6.140.136 trendLog 2001 startTime")
    cov_subs_list = bacnet.read("139.6.140.136 device 13 activeCovSubscriptions")
    recip_list = bacnet.read("139.6.140.136 notificationClass 1 recipientList")
    deviceObjectPropertyReference = bacnet.read("139.6.140.136 trendLog 2001 logDeviceObjectProperty")

    BACnetParser.parse(deviceObjectPropertyReference)

#test_bacnet_parser()

#test_dict = {'recipient': {'recipient': {'address': {'networkNumber': 0, 'macAddress': bytearray(b'\x8b\x06\x8c\x0e\xba\xc0')}}, 'processIdentifier': 1}, 'monitoredPropertyReference': {'objectIdentifier': ('multiStateValue', 2058), 'propertyIdentifier': 'presentValue'}, 'issueConfirmedNotifications': True, 'timeRemaining': 0}
#dict_neu = BACnetParser._replace_bytearrays(test_dict)
#print(test_dict)
#print(dict_neu)
#
class ModbusParser:
    @staticmethod
    def parse(reg_values: list[int], type_: str):
        match type_:
            case "bool":
                return bool(reg_values[0])
            case "int":
                # offset = 65535 ** len(reg_values) / 2
                # print(offset)
                # if len(reg_values) % 2:
                #    offset += 0.5
                min_value = -32768
                bitstring = ModbusParser.int_to_bitstring(reg_values)
                uint_value = ModbusParser.bitstring_to_uint(bitstring)
                return int(uint_value + min_value)
            case "uint":
                bitstring = ModbusParser.int_to_bitstring(reg_values)
                return ModbusParser.bitstring_to_uint(bitstring)
            case "str":
                bitstring = ModbusParser.int_to_bitstring(reg_values)
                print(bitstring)
                return ModbusParser.bitstring_to_str(bitstring)
            case "byte":
                return ModbusParser.int_to_bitstring(reg_values[0], bits_per_byte=8)

    @staticmethod
    def bitstring_to_str(bitstring: str, bits_per_char: int = 8):
        string = ""
        while len(bitstring) >= bits_per_char:
            substring = bitstring[:bits_per_char]
            bitstring = bitstring[bits_per_char:]
            value = ModbusParser.bitstring_to_uint(substring)
            string += chr(value)
        if len(bitstring) > 0:
            value = ModbusParser.bitstring_to_uint(bitstring)
            string += chr(value)
        if string.endswith("\0"):
            string = string[:-1]
        return string

    @staticmethod
    def int_to_bitstring(value: int | list[int], bits_per_byte: int = 16) -> str:
        max_value = 2 ** bits_per_byte - 1
        bitstring = ""
        if isinstance(value, int):
            value = [value]
        for i in value:
            if i > max_value:
                raise ValueError(f"Given value {i} cannot be mapped to {bits_per_byte} bits (max value {max_value})")
            bits = bin(i).replace("0b", "")[::-1]
            while len(bits) < bits_per_byte:
                bits += "0"
            bitstring += bits
        return bitstring

    @staticmethod
    def bitstring_to_uint(bitstring: str, base: int = 2):
        value = 0
        for i in range(len(bitstring)):
            value += int(bitstring[i]) * base ** i
        return value


class Protocol(Enum):
    AAS = 0
    BACNET = 1
    MODBUS = 2


class Parser:
    @staticmethod
    def parse(obj_to_parse: object, target_protocol: Protocol):
        match target_protocol.name:
            case "AAS":
                Parser.parse_to_aas(obj_to_parse)
            case "BACNET":
                print("BACNET not implemented yet")
            case "MODBUS":
                print("MODBUS not implemented yet")
            case _:
                print(f"unknown protocol: {target_protocol}")

    @staticmethod
    def parse_to_aas(obj_to_parse: object):
        if isinstance(obj_to_parse, list):
            print("I am a list")


# Parser.parse(["Hallo"], Protocol.AAS)

def read(read_str: str) -> PriorityArray:
    bacnet = BAC0.connect()
    # bacnet.whois()
    return bacnet.read(read_str)


# test()

# bitstring = ""
# string = "Hallo"
# for c in string:
#    bitstring += ModbusParser.int_to_bitstring(ord(c), bits_per_byte=8)
# bitstring += "00000000"
# abc = ModbusParser.bitstring_to_str(bitstring)
# print(abc)
# ModbusParser.parse([254**2], "str")

# abc = ModbusParser.int_to_bitstring(65535)
# print(abc)
