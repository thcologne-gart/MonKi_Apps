import json
import os
import time

from utils import utils

class ConfigManagerStatic:
    DEFAULT_ID_TYPE = "IRI"
    DEFAULT_TIMER_PERIOD = 60
    MIN_TIMER_PERIOD = 5
    DEFAULT_DO_SCAN = False
    DEFAULT_MONGODB_DATABASE_NR = 10001
    DEFAULT_MONGODB_URL = "mongodb://localhost:27017/"
    DEFAULT_INCLUDE_MSTP = False
    DEFAULT_MONGODB_DATABASE_NAME = "TimeSeries-$mongoDbDatabaseNr$"
    DEFAULT_ID_SHORT_MEASUREMENTS = "Measurements"
    # DEFAULT_CONFIG_PATH = "config"
    DEFAULT_BASYX_VERSION = "v1"

    __CONTENT = None
    __PATH = None

    @staticmethod
    def init(path_config_file: str = None):
        ConfigManagerStatic.__CONTENT, ConfigManagerStatic.__PATH = ConfigManagerStatic.__load_config_file(path_config_file)

    @staticmethod
    def __load_config_file(path_config_file):
        if path_config_file is None:
            file_name = os.path.basename(__file__)
            path_config_file = __file__.replace(file_name, "config.json")
        else:
            path_config_file = path_config_file.replace("\\", "/")
            if not path_config_file.endswith("config.json"):
                if path_config_file.endswith("/"):
                    path_config_file = path_config_file + "config.json"
                else:
                    path_config_file = path_config_file + "/config.json"

        if not os.path.isfile(path_config_file):
            raise FileNotFoundError(f"No 'config.json'-file found in {path_config_file.replace('/config.json', '')}")

        f = open(path_config_file)
        #self._mod_time = os.path.getmtime(path_config_file)
        return json.loads(f.read()), path_config_file

    @staticmethod
    def get_basyx_version():
        if "basyxVersion" in ConfigManagerStatic.__CONTENT.keys():
            return ConfigManagerStatic.__CONTENT['basyxVersion']
        return ConfigManagerStatic.DEFAULT_BASYX_VERSION

    @staticmethod
    def get_server_url():
        if "serverUrl" in ConfigManagerStatic.__CONTENT.keys():
            if ConfigManagerStatic.get_basyx_version() == "v2":
                url = ConfigManagerStatic.__CONTENT['serverUrl']
                if not url.endswith("/"):
                    url += "/"
                return url.replace("shells/", "")
            return ConfigManagerStatic.__CONTENT['serverUrl']

        raise RuntimeError("No serverUrl defined in config-file")

class ConfigManager:
    DEFAULT_ID_TYPE = "IRI"
    DEFAULT_TIMER_PERIOD = 60
    MIN_TIMER_PERIOD = 5
    DEFAULT_DO_SCAN = False
    DEFAULT_MONGODB_DATABASE_NR = 10001
    DEFAULT_MONGODB_URL = "mongodb://localhost:27017/"
    DEFAULT_INCLUDE_MSTP = False
    DEFAULT_MONGODB_DATABASE_NAME = "TimeSeries-$mongoDbDatabaseNr$"
    DEFAULT_ID_SHORT_MEASUREMENTS = "Measurements"
    #DEFAULT_CONFIG_PATH = "config"
    DEFAULT_BASYX_VERSION = "v1"

    def __init__(self, path_config_file: str = None):
        self.jsonConfig, self.path_config_file = self.__load_config_file(path_config_file)

        self.live_data_id_short = None
        self.aas_id_short = None
        self.aid_id_short = None
        self.aimc_id_short = None

        self.aas_identification = None
        self.aid_identification = None
        self.aimc_identification = None
        self.live_data_identification = None

    def __load_config_file(self, path_config_file):
        if path_config_file is None:
            file_name = os.path.basename(__file__)
            path_config_file = __file__.replace(file_name, "config.json")
        else:
            path_config_file = path_config_file.replace("\\", "/")
            if not path_config_file.endswith("config.json"):
                if path_config_file.endswith("/"):
                    path_config_file = path_config_file + "config.json"
                else:
                    path_config_file = path_config_file + "/config.json"

        if not os.path.isfile(path_config_file):
            raise FileNotFoundError(f"No 'config.json'-file found in {path_config_file.replace('/config.json', '')}")

        f = open(path_config_file)
        self._mod_time = os.path.getmtime(path_config_file)
        return json.loads(f.read()), path_config_file

    def reload_config_file(self):
        time_stamp_old = self._mod_time
        self.jsonConfig, self.path_config_file = self.__load_config_file(self.path_config_file)
        return time_stamp_old, self._mod_time

    def get_basyx_version(self):
        if "basyxVersion" in self.jsonConfig.keys():
            return self.jsonConfig['basyxVersion']
        return self.DEFAULT_BASYX_VERSION

    def scan_wanted(self):
        if "doScan" in self.jsonConfig.keys():
            return self.jsonConfig['doScan']
        return self.DEFAULT_DO_SCAN

    def get_wanted_devices(self):
        devices = []
        if "devices" in self.jsonConfig.keys():
            var1 = self.jsonConfig["devices"]
            for device_id in var1:
                try:
                    devices.append(int(device_id))
                except ValueError:
                    print(f"Provided DeviceId '{device_id}' is invalid and therefor ignored.")
        return devices

    def get_timer_period(self):
        if "defaultTimerPeriod" in self.jsonConfig.keys():
            return self.jsonConfig["defaultTimerPeriod"]
        return self.DEFAULT_TIMER_PERIOD

    def getServerUrl(self):
        if "serverUrl" in self.jsonConfig.keys():
            return self.jsonConfig['serverUrl']
        raise RuntimeError("No serverUrl defined in config-file")

    def getRegistryUrl(self):
        if "registryUrl" in self.jsonConfig.keys():
            return self.jsonConfig['registryUrl']
        raise RuntimeError("No registryUrl defined in config-file")
    def __getSemanticId(self, name):
        basyx_version = self.get_basyx_version()
        if name not in self.jsonConfig.keys():
            print(f"No {name} defined in config-file. Defaulting to: empty semantic id.")
            return {"keys": []} if basyx_version == "v1" else {"type": "ExternalReference", "keys": []}

        var1 = self.jsonConfig[name]
        if basyx_version == "v1":
            mandatory_keys = ["idType", "value", "local", "type"]
            if "keys" in var1.keys():
                var1 = var1["keys"]
            var1 = self.checkForMandatoryKeys(mandatory_keys, var1, name)
            return {"keys": [var1]}
        elif basyx_version == "v2":
            mandatory_keys = ["value", "type"]
            if "keys" in var1.keys():
                var1 = var1["keys"]
            var1 = self.checkForMandatoryKeys(mandatory_keys, var1, name)
            return {"type": "ExternalReference", "keys": [var1]}
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")



    def checkForMandatoryKeys(self, mandatoryKeys: list, dictToCheck: dict, dictName: str):
        missingKeys = []
        for key in mandatoryKeys:
            if key not in dictToCheck.keys():
                missingKeys.append(key)

        dict_keys = list(dictToCheck.keys())
        for key in dict_keys:
            if key not in mandatoryKeys:
                dictToCheck.pop(key)
        if len(missingKeys) != 0:
            raise KeyError(f"{dictName} missing mandatory keys: {str(missingKeys)}")
        return dictToCheck

    def getSemanticIdAID(self):
        return self.__getSemanticId("semanticIdAid")

    def getSemanticIdAIMC(self):
        return self.__getSemanticId("semanticIdAimc")

    def getSemanticIdLiveData(self):
        return self.__getSemanticId("semanticIdLiveData")


    def get_id_aas(self, deviceName, deviceId):
        if self.aas_identification is None:
            self.update_id_aas(deviceName, deviceId)
        return self.aas_identification

    def get_id_aid(self, deviceName, deviceId):
        if self.aid_identification is None:
            self.update_id_aid(deviceName, deviceId)
        return self.aid_identification

    def get_id_aimc(self, deviceName, deviceId):
        if self.aimc_identification is None:
            self.update_id_aimc(deviceName, deviceId)
        return self.aimc_identification

    def get_id_live_data(self, deviceName, deviceId):
        if self.live_data_identification is None:
            self.update_id_live_data(deviceName, deviceId)
        return self.live_data_identification

    def update_all_ids(self, deviceName, deviceId):
        self.update_id_aas(deviceName, deviceId)
        time.sleep(0.3)
        self.update_id_aid(deviceName, deviceId)
        time.sleep(0.3)
        self.update_id_aimc(deviceName, deviceId)
        time.sleep(0.3)
        self.update_id_live_data(deviceName, deviceId)

    def update_id_aas(self, deviceName, deviceId):
        self.aas_identification = self.__create_id("schemeIdAas", deviceName, deviceId)

    def update_id_aid(self, deviceName, deviceId):
        self.aid_identification = self.__create_id("schemeIdAid", deviceName, deviceId)

    def update_id_aimc(self, deviceName, deviceId):
        self.aimc_identification = self.__create_id("schemeIdAimc", deviceName, deviceId)

    def update_id_live_data(self, deviceName, deviceId):
        self.live_data_identification = self.__create_id("schemeIdLiveData", deviceName, deviceId)

    def __create_id(self, name, deviceName, deviceId):
        DEFAULT_ID = f"{name}-$timestamp$"
        if name in self.jsonConfig.keys():
            var3 = self.jsonConfig[name]
        else:
            var3 = {'id': f'{name}-$timestamp$', 'idType': self.DEFAULT_ID_TYPE}
            utils.log(f"No {name} defined in config-file. Defaulting to: '{str(var3)}'")

        if type(var3) == str:
            return {"id": utils.applySchemeId(var3, deviceName, deviceId), "idType": self.DEFAULT_ID_TYPE}
        elif type(var3) == dict:
            for key in var3.keys():
                if key != "id" and key != "idType" and key != "idShort":
                    utils.log(f"Ignoring unknown key '{key}' in {name}")

            var7 = {}
            if "id" in var3.keys():
                var7["id"] = utils.applySchemeId(var3["id"], deviceName, deviceId)
            else:
                var7["id"] = utils.applySchemeId(DEFAULT_ID, deviceName, deviceId)
                utils.log(f"No id defined for {name}. Defaulting to: '{var7['id']}'")
            if "idType" in var3.keys():
                var7["idType"] = var3["idType"]
            else:
                var7["idType"] = self.DEFAULT_ID_TYPE
                utils.log(f"No idType defined for {name}. Defaulting to: '{var7['idType']}'")
            return var7

    def getAssetId(self, deviceName, deviceId):
        default = f"bacnet_device_{deviceId}_{deviceName}"
        if "assetId" in self.jsonConfig.keys():
            assetId = self.jsonConfig["assetId"]
            if type(assetId) == str:
                return assetId.replace("$deviceName$", deviceName).replace("$deviceId$", str(deviceId))
            utils.log(f"Value of key assetId should be String, is {str(type(assetId))}. Defaulting assetId to: '{default}'")
            return default

    def getIdShortAAS(self, deviceName, deviceId):
        var11 = self.__getIdShort("schemeIdAas", deviceName, deviceId)
        return var11#.replace("$deviceName$", deviceName).replace("$deviceId$", str(deviceId))
    def getIdShortAID(self, deviceName, deviceId):
        return self.__getIdShort("schemeIdAid", deviceName, deviceId)
    def getIdShortAIMC(self, deviceName, deviceId):
        return self.__getIdShort("schemeIdAimc", deviceName, deviceId)
    def getIdShortLiveData(self, deviceName, deviceId):
        return self.__getIdShort("schemeIdLiveData", deviceName, deviceId)

    def __getIdShort(self, name, deviceName, deviceId):
        defaults = {
            "schemeIdAas": "$deviceName$($deviceId$)",
            "schemeIdAid": "AssetInterfacesDescription",
            "schemeIdAimc": "AssetInterfaceMappingConfiguration",
            "schemeIdLiveData": "BACnetDatapointsInformation"
        }
        if name in self.jsonConfig.keys():
            var9 = self.jsonConfig[name]
            if type(var9) == dict:
                if "idShort" in var9.keys():
                    return utils.applySchemeId(var9["idShort"], deviceName, deviceId)
                else:
                    utils.log(f"No idShort defined for {name} in config-file. Defaulting to: '{defaults[name]}'")
                    return utils.applySchemeId(defaults[name], deviceName, deviceId)
            else:
                utils.log(f"Value of key {name} should be JSON-object, is {str(type(var9))}. Defaulting idShort to: '{defaults[name]}'")
                return utils.applySchemeId(defaults[name], deviceName, deviceId)
        else:
            utils.log(f"No {name} defined in config-file. Defaulting idShort to: '{defaults[name]}'")
            return utils.applySchemeId(defaults[name], deviceName, deviceId)

    """
    NEW
    """

    def get_trigger_options(self):
        if "triggerOptions" in self.jsonConfig.keys():
            return self.jsonConfig["triggerOptions"]
        return {}

    def get_default_timer_period(self) -> int:
        if "defaultTimerPeriod" in self.jsonConfig.keys():
            return self.jsonConfig["defaultTimerPeriod"]
        return self.DEFAULT_TIMER_PERIOD

    def include_mstp(self):
        if "includeMSTP" in self.jsonConfig.keys():
            return self.jsonConfig["includeMSTP"]
        return ConfigManager.DEFAULT_INCLUDE_MSTP

    def get_mongo_db_url(self):
        if "mongoDbUrl" in self.jsonConfig.keys():
            return self.jsonConfig["mongoDbUrl"]
        return ConfigManager.DEFAULT_MONGODB_URL

    def get_mongo_db_database_nr(self):
        if "mongoDbDatabaseNr" in self.jsonConfig.keys():
            return self.jsonConfig["mongoDbDatabaseNr"]
        return ConfigManager.DEFAULT_MONGODB_DATABASE_NR

    def get_mongo_db_database_name(self):
        db_nr = self.get_mongo_db_database_nr()
        if "mongoDbDatabaseName" in self.jsonConfig.keys():
            return self.jsonConfig["mongoDbDatabaseName"].replace("$mongoDbDatabaseNr$", str(db_nr))
        return ConfigManager.DEFAULT_MONGODB_DATABASE_NAME.replace("$mongoDbDatabaseNr$", str(db_nr))

    def get_id_short_measurements(self):
        if "idShortMeasurements" in self.jsonConfig.keys():
            return self.jsonConfig["idShortMeasurements"]
        return ConfigManager.DEFAULT_ID_SHORT_MEASUREMENTS

    def get_baudrate_modbus(self):
        if "modbusBaudrate" in self.jsonConfig.keys():
            return self.jsonConfig["modbusBaudrate"]
        return 38400

    def get_parity_modbus(self):
        if "modbusParity" in self.jsonConfig.keys():
            return self.jsonConfig["modbusParity"]
        return "N"

    def get_stopbits_modbus(self):
        if "modbusStopbits" in self.jsonConfig.keys():
            return self.jsonConfig["modbusStopbits"]
        return 2


