import BAC0
import pymodbus.client
from aas import aas_components
from aas.aas_components import AasCommunicator
from config import ConfigManager
from protocols.bacnet.BACnet import Device
from utils import utils


class Communicator:
    __bacnet = None
    __modbus = None
    __config_manager: ConfigManager = None
    __aas = None

    @staticmethod
    def set_config_manager(config_manager: ConfigManager):
        Communicator.__config_manager = config_manager

    @staticmethod
    def get_bacnet_communicator() -> BAC0.scripts.Base:
        if Communicator.__bacnet is None:
            Communicator.__bacnet = BAC0.connect()
        return Communicator.__bacnet

    @staticmethod
    def get_aas_communicator() -> AasCommunicator:
        if Communicator.__aas is None:
            Communicator.__aas = AasCommunicator(config_manager=Communicator.__config_manager)
        return Communicator.__aas

    @staticmethod
    def discover_bacnet():
        bacnet = Communicator.get_bacnet_communicator()
        if Communicator.__config_manager.include_mstp():
            bacnet.discover(global_broadcast=True)
        else:
            bacnet.whois()

        devices_to_browse = Communicator.filter_found_devices(Communicator.__config_manager.get_wanted_devices())
        #mapping = {dev[3]: {"aas_url": None, "objects": {}, "ip_address": dev[2],
        #                    "pull_interval": Communicator.__config_manager.get_default_timer_period()} for dev in devices_to_browse}

        basyx_version = Communicator.__config_manager.get_basyx_version()
        if basyx_version == "v1":
            aas_server = aas_components.AasServerV1(Communicator.__config_manager.getServerUrl())
        elif basyx_version == "v2":
            aas_server = aas_components.AasServerV2(Communicator.__config_manager.getServerUrl())
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")

        for device_tuple in devices_to_browse:
            device = Device(
                bacnet=bacnet,
                device_id=device_tuple[3],
                ip_address=device_tuple[2],
                device_name=device_tuple[0]
            )
            aas_components.ShellBuilder.create_shells(device, aas_server, Communicator.__config_manager)

    @staticmethod
    def filter_found_devices(wanted_devices: list):
        bacnet = Communicator.get_bacnet_communicator()
        device_ids_found = [device[3] for device in bacnet.devices]
        utils.log(f"Devices available: {str(device_ids_found)}\n", newline=True)

        if len(wanted_devices) == 0:
            return bacnet.devices

        for device_id in wanted_devices:
            if device_id not in device_ids_found:
                utils.log(f"Missing wanted device: {device_id}")

        devices_to_browse = [device for device in bacnet.devices if device[3] in wanted_devices]
        return devices_to_browse

    @staticmethod
    def get_modbus_communicator() -> pymodbus.client.ModbusSerialClient:
        """ToDo: get Port (semi-)automatically"""
        baudrate = Communicator.__config_manager.get_baudrate_modbus()
        parity = Communicator.__config_manager.get_parity_modbus()
        stopbits = Communicator.__config_manager.get_stopbits_modbus()

        if Communicator.__modbus is None:
            Communicator.__modbus = pymodbus.client.ModbusSerialClient(
                method='rtu',
                port='COM5',
                baudrate=baudrate,
                timeout=5,
                retry_on_empty=True,
                retries=3,
                debug=True,
                stopbits=stopbits,
                parity=parity)
        return Communicator.__modbus
