import json
import os
import platform
import time

from aas import aas_components
import elements.mongodb
from aas.aas_components import AasComponent
from aas.asset_interfaces_description import AssetInterfacesDescription
from config import ConfigManager, ConfigManagerStatic
from elements.endpoints import BacnetEndpoint, AasEndpoint, TimerEndpoint, MongoDbTimeSeriesEndpoint, RouteElement, ModbusEndpoint
from mapper import Mapper
from utils import propertyNameForId
from protocols.communicator import Communicator



class File:
    def __init__(self, file_name: str, path: str):
        self._file_name = file_name
        self._path = path
        self._full_path = self._normalize_name()
        self._content = {}

    def save(self):
        pass

    def _normalize_name(self):
        if self._path is None:
            return self._file_name
        return os.path.join(self._path, self._file_name)

    @staticmethod
    def str_to_list(string: str, separator: str = ","):
        _list = []
        if string.startswith("["):
            string = string[1:]
        if string.endswith("]"):
            string = string[:-1]
        elements = string.split(separator)
        decimal_separator = "," if separator == "." else "."

        for element in elements:
            while element.startswith(" "):
                element = element[1:]
            if element.startswith("'"):
                _list.append(element.replace("'", ""))
            elif element.startswith("\""):
                _list.append(element.replace("\"", ""))
            else:
                try:
                    if decimal_separator in element:
                        _list.append(float(element))
                    else:
                        _list.append(int(element))
                except ValueError:
                    _list.append(element)
        return _list

    def contains(self, unique_id: str):
        pass


class ConsumerFile(File):
    def __init__(self, file_name: str, path: str):
        super().__init__(file_name, path)

    def contains(self, unique_id: str):
        return unique_id in self._content.keys()

    def open(self):
        self._content = {}
        if os.path.isfile(self._full_path):
            with open(self._full_path) as f:
                content = json.load(f)
            for element in content:
                self._content[element["uniqueId"]] = element

    def get_endpoints(self):
        pass

    def remove_element(self, unique_id):
        if not self.contains(unique_id):
            print(f"Element {unique_id} does not exist")
            return False
        self._content.pop(unique_id)
        return True

    def add_element(self, element: dict):
        if type(element) != dict:
            print("Only elements of type dict allowed")
            return False

        unique_id = element["uniqueId"]
        if self.contains(unique_id):
            self.remove_element(unique_id)
        self._content[unique_id] = element
        return True

    def save(self):
        with open(self._full_path, "w") as outfile:
            json.dump(list(self._content.values()), outfile, indent=4)

class BacnetConsumerFile(ConsumerFile):
    name = "bacnetconsumer.json"
    def __init__(self, path: str = None):
        super().__init__(self.name, path)
        self._bacnet = Communicator.get_bacnet_communicator()


    @staticmethod
    def _identify_device_id(properties: list):
        for prop in properties:
            if prop["idShort"].startswith("device_"):
                for var5 in prop["value"]:
                    if var5["idShort"] == "bacnet:InstanceNumber":
                        return int(var5["value"])

    @staticmethod
    def base_to_ip(base: str):
        if ":" in base:
            if base.count(":") == 1:
                return base.split(":")[1]
            # Could be an address including the port or MS/TP address like 3:8
            elif base.count(":") == 2:
                temp = base.split(":")
                return temp[1] + ":" + temp[2]

    def get_endpoints(self):
        endpoints_ = {}
        for elem in self._content.values():
            endpoints_[elem["uniqueId"]] = BacnetEndpoint(
                    bacnet=self._bacnet,
                    device_id=elem["deviceId"],
                    ip_address=elem["ipAddress"],
                    object_type=elem["objectType"],
                    instance_nr=elem["instanceNr"],
                    property_id=elem["propertyId"]
                )
        return endpoints_


    def add_bacnet_consumer(self,
                            unique_id: str,
                            ip_address: str,
                            device_id: int,
                            object_type: str,
                            instance_nr: int,
                            property_id: int):
        consumer = {
            "uniqueId": unique_id,
            "ipAddress": ip_address,
            "deviceId": device_id,
            "objectType": object_type,
            "instanceNr": instance_nr,
            "propertyId": property_id
        }
        self.add_element(consumer)

    @staticmethod
    def _all_initialized(to_check: list):
        for var3 in to_check:
            if var3 is None:
                return False
        return True

    def discover_registry(self, config_manager: ConfigManager):
        aas_communicator = Communicator.get_aas_communicator()
        submodels, submodel_urls = aas_communicator.get_submodels(config_manager.getSemanticIdAID())
        if len(submodels) == 0:
            for file_kind in FileHandler.MANDATORY_FILES:
                if file_kind == self.__class__:
                    self.open()
                    self.save()
                else:
                    file = file_kind(self._path)
                    file.open()
                    file.save()
        else:
            """ToDo: remove index_sm"""
            index_sm = 0
            for submodel in submodels:
                aid_submodel = AssetInterfacesDescription(submodel)
                if ConfigManagerStatic.get_basyx_version() == "v1":
                    aid_submodel.set_url(submodel_urls[index_sm])
                elif ConfigManagerStatic.get_basyx_version() == "v2":
                    aid_submodel.set_url(ConfigManagerStatic.get_server_url() + f"submodels/{AasComponent.encode_id(aid_submodel.get_id())}")

                index_sm += 1
                self.build_from_aid(aid_submodel, config_manager)

    def _get_url_livedata_sm(self, aid_submodel, id_short_livedata_submodel):
        if ConfigManagerStatic.get_basyx_version() == "v1":
            return aid_submodel.get_url().replace("AssetInterfacesDescription", id_short_livedata_submodel)
        elif ConfigManagerStatic.get_basyx_version() == "v2":
            communicator = Communicator.get_aas_communicator()
            aas_id = communicator.get_aas_id_for_submodel(aid_submodel.get_id())
            aas = communicator.get_aas(aas_id)

            for sm in aas["submodels"]:
                for key in sm["keys"]:
                    if key["type"] == "Submodel":
                        try:
                            sm_id = key["value"]
                            if communicator.get_sm_metadata(sm_id)["idShort"] == id_short_livedata_submodel:
                                return aid_submodel.get_url().replace(
                                    AasComponent.encode_id(aid_submodel.get_id()),
                                    AasComponent.encode_id(sm_id)
                                )
                        except:
                            continue
        return None

    def build_from_aid(self, aid_submodel: AssetInterfacesDescription, config_manager: ConfigManager):
        aid = aid_submodel.get_aid("BACnetInterface")
        aas_server_file = AasServerFile(self._path)
        timer_consumer_file = TimerConsumerFile(self._path)
        routes_file = RoutesFile(self._path)
        mongo_file = MongoTimeSeriesConsumerFile(self._path)

        self.open()
        aas_server_file.open()
        timer_consumer_file.open()
        routes_file.open()
        mongo_file.open()

        properties = aid.get_properties()
        device_id = self._identify_device_id(properties)
        ip_address = self.base_to_ip(aid.get_base())
        aas_id = aid_submodel.get_aas_id()
        trigger_options = config_manager.get_trigger_options()

        """ToDo: remove None"""
        id_short_livedata_submodel = config_manager.getIdShortLiveData(None, device_id)

        url_livedata_submodel = self._get_url_livedata_sm(aid_submodel, id_short_livedata_submodel)

        for prop in properties:
            object_type = None
            instance_nr = None
            property_list = None
            for var1 in prop["value"]:
                if var1["idShort"] == "bacnet:ObjectType":
                    """ToDo: validate object type"""
                    object_type = var1["value"]
                elif var1["idShort"] == "bacnet:InstanceNumber":
                    instance_nr = int(var1["value"])
                elif var1["idShort"] == "bacnet:service":
                    pass
                elif var1["idShort"] == "bacnet:PropertyList":
                    var3 = var1["value"]
                    property_list = var3 if type(var3) == list else self.str_to_list(var3)
            if not self._all_initialized([object_type, instance_nr, property_list]):
                """ToDo: Log"""
                continue

            basyx_version = config_manager.get_basyx_version()
            unique_id_raw_bacnet = f"bacnet/{device_id}/{object_type}_{instance_nr}/"

            mongo_db_database_name = config_manager.get_mongo_db_database_name()
            if aas_id:
                unique_id_raw_aas = f"{aas_id.replace('/', '%2F')}/{id_short_livedata_submodel}/{object_type}_{instance_nr}/"
                unique_id_raw_mongo = f"mongo/{mongo_db_database_name}/{aas_id.replace('/', '%2F')}/"
            else:
                unique_id_raw_aas = f"{id_short_livedata_submodel}/{object_type}_{instance_nr}/"
                unique_id_raw_mongo = f"mongo/{mongo_db_database_name}/{aid_submodel.get_id()}/"


            for bacnet_prop in property_list:
                if isinstance(bacnet_prop, int) and bacnet_prop in propertyNameForId.keys():
                    bacnet_prop = propertyNameForId[bacnet_prop]
                else:
                    bacnet_prop = str(bacnet_prop)
                unique_id = unique_id_raw_bacnet + bacnet_prop
                self.add_bacnet_consumer(
                    unique_id=unique_id,
                    ip_address=ip_address,
                    device_id=device_id,
                    object_type=object_type,
                    instance_nr=instance_nr,
                    property_id=bacnet_prop
                )

                ### AAS Part
                unique_id_aas = unique_id_raw_aas + bacnet_prop
                id_short_path = f"{object_type}_{instance_nr}/{bacnet_prop}"
                aas_server_file.add_aas_consumer(
                    unique_id=unique_id_aas,
                    submodel_endpoint=url_livedata_submodel,
                    id_short_path=id_short_path,
                    basyx_version=basyx_version
                )
                ### Timer Part

                """ToDo: add function for trigger options"""
                if bacnet_prop in trigger_options.keys():
                    unique_id_timer = timer_consumer_file.add_timer(trigger_options[bacnet_prop])
                else:
                    unique_id_timer = timer_consumer_file.add_timer(config_manager.get_default_timer_period())

                ### Routes Part
                routes_file.add_timer_route(
                    datasource=unique_id,
                    datasink=unique_id_aas,
                    timer_name=unique_id_timer
                )

                ### MongoDB Part
                id_short_measurements = config_manager.get_id_short_measurements()
                unique_id_mongo = unique_id_raw_mongo + f"{id_short_measurements}/{id_short_path}"
                mongo_file.add_mongo_db_consumer(
                    unique_id=unique_id_mongo,
                    url=config_manager.get_mongo_db_url(),
                    database_name=config_manager.get_mongo_db_database_name(),
                    collection_name=aas_id,
                    id_short_submodel=id_short_measurements,
                    id_short_path=id_short_path
                )

        self.save()
        aas_server_file.save()
        routes_file.save()
        timer_consumer_file.save()
        mongo_file.save()


class ModbusConsumerFile(ConsumerFile):
    name = "modbusconsumer.json"

    def __init__(self, path: str = None):
        super().__init__(self.name, path)
        self._modbus_client = Communicator.get_modbus_communicator()

    def get_endpoints(self):
        endpoints_ = {}
        for elem in self._content.values():
            endpoints_[elem["uniqueId"]] = ModbusEndpoint(
                    modbus_client=self._modbus_client,
                    device_id=elem["device_id"],
                    register_address=elem["register_address"],
                    nr_register=elem["nr_register"],
                    type_=elem["type"]
                )
        return endpoints_

    def add_modbus_consumer(self,
                         unique_id: str,
                         device_id: int,
                         register_address: int,
                         nr_register: int,
                         type_: str
                         ):
        consumer = {
            "uniqueId": unique_id,
            "device_id": device_id,
            "register_address": register_address,
            "nr_register": nr_register,
            "type": type_
        }
        self.add_element(consumer)


class AasServerFile(ConsumerFile):
    name = "aasserver.json"
    def __init__(self, path: str = None):
        super().__init__(self.name, path)

    def add_aas_consumer(self,
                         unique_id: str,
                         submodel_endpoint: str,
                         id_short_path: str,
                         basyx_version: str
                         ):
        consumer = {
            "uniqueId": unique_id,
            "submodelEndpoint": submodel_endpoint,
            "idShortPath": id_short_path,
            "basyxVersion": basyx_version
        }
        self.add_element(consumer)

    def get_endpoints(self):
        endpoints_ = {}
        for elem in self._content.values():
            endpoints_[elem["uniqueId"]] = AasEndpoint(
                    submodel_endpoint=elem["submodelEndpoint"],
                    id_short_path=elem["idShortPath"],
                    basyx_version=elem["basyxVersion"]
                )
        return endpoints_


class MongoTimeSeriesConsumerFile(ConsumerFile):
    name = "mongotimeseriesconsumer.json"
    def __init__(self, path: str = None):
        super().__init__(self.name, path)

    def get_endpoints(self) -> dict[str, MongoDbTimeSeriesEndpoint]:
        endpoints_ = {}
        for elem in self._content.values():
            endpoints_[elem["uniqueId"]] = MongoDbTimeSeriesEndpoint(
                    mongo_db=elements.mongodb.MongoDBHandler.get_mongo_db(elem["url"]),
                    database_name=elem["databaseName"],
                    collection_name=elem["collectionName"],
                    submodel_name=elem["idShortSubmodel"],
                    id_short_path=elem["idShortPath"],
               )
        return endpoints_

    def add_mongo_db_consumer(self,
                              unique_id: str,
                              url: str,
                              database_name: str,
                              collection_name: str,
                              id_short_submodel: str,
                              id_short_path: str):
        consumer = {
            "uniqueId": unique_id,
            "url": url,
            "databaseName": database_name,
            "collectionName": collection_name,
            "idShortSubmodel": id_short_submodel,
            "idShortPath":id_short_path
        }
        self.add_element(consumer)


class TimerConsumerFile(ConsumerFile):
    name = "timerconsumer.json"
    def __init__(self, path: str = None):
        super().__init__(self.name, path)
        self._name_to_period_map = {}
        self._period_to_name_map = {}


    def open(self):
        super().open()
        self._name_to_period_map = {timer_name: timer["period"] for timer_name, timer in self._content.items()}
        self._period_to_name_map = {timer["period"]: timer_name for timer_name, timer in self._content.items()}

    def get_period(self, timer_name):
        if timer_name in self._name_to_period_map.keys():
            return self._name_to_period_map[timer_name]
        else:
            return None

    def get_endpoints(self):
        endpoints_ = []
        for elem in self._content.values():
            endpoints_[elem["uniqueId"]] = TimerEndpoint(
                    period=elem["period"]
                )
        return endpoints_

    def add_timer(self,
                  period: int,
                  fixed_rate: bool = True,
                  delay: int = 0
                  ):
        if period not in self._period_to_name_map.keys():
            unique_id = f"timer_{str(len(self._period_to_name_map)+1)}"
            consumer = {
                "uniqueId": unique_id,
                "period": period,
                "fixedRate": fixed_rate,
                "delay": delay
            }
            self._period_to_name_map[period] = unique_id
            self.add_element(consumer)
        return self._period_to_name_map[period]


class RoutesFile(File):
    name = "routes.json"
    def __init__(self, path: str = None):
        super().__init__(self.name, path)

    def open(self):
        self._content = {}
        if os.path.isfile(self._full_path):
            with open(self._full_path) as f:
                content = json.load(f)
            for route in content:
                self._content[route["datasource"]] = route

    def save(self):
        with open(self._full_path, "w") as outfile:
            json.dump(list(self._content.values()), outfile, indent=4)

    def contains(self, unique_id_datasource: str):
        return unique_id_datasource in self._content.keys()

    def add_datasink(self, unique_id_datasource: str, unique_id_datasink):
        if not self.contains(unique_id_datasource):
            print(f"Datasource {unique_id_datasource} does not exist")
        else:
            #if unique_id_datasink in self._content[unique_id_datasource]["datasinks"]:
            #    print(f"Datasink {unique_id_datasink} already routed from datasource {unique_id_datasource}")
            #else:
            self._content[unique_id_datasource]["datasinks"].append(unique_id_datasink)

    def add_element(self, element: dict):
        if type(element) != dict:
            print("Only elements of type dict allowed")
            return False

        datasource = element["datasource"]
        if self.contains(datasource):
            for var7 in element["datasinks"]:
                self.add_datasink(datasource, var7)
        else:
            self._content[datasource] = element
        return True

    def add_timer_route(self,
                        datasource: str,
                        timer_name: str,
                        datasink: str):
        route = {
            "datasource": datasource,
            "trigger": "timer",
            "triggerData": {
                "timerName": timer_name
            },
            "datasinks": [
                datasink
            ]
        }
        self.add_element(route)

    def get_routes(self) -> list[RouteElement]:
        routes_ = []
        for elem in self._content.values():
            trigger = elem["trigger"]
            timer_name = None
            if "triggerData" in elem.keys():
                trigger_data = elem["triggerData"]
                if "timerName" in trigger_data.keys():
                    timer_name = trigger_data["timerName"]
            routes_.append(
                RouteElement(
                    datasource=elem["datasource"],
                    datasinks=elem["datasinks"],
                    timer_name=timer_name,
                    trigger=trigger
                )
            )
        return routes_


class FileHandler:
    NAME_ARCHIVE_DIR = "archive"
    MANDATORY_FILES = [
        AasServerFile,
        TimerConsumerFile,
        RoutesFile,
        MongoTimeSeriesConsumerFile,
        BacnetConsumerFile
    ]

    def __init__(self, path: str = None):
        self._path = "" if path is None else path
        self._file_names = None
        self._files = None
        self._routes_file = None
        self._timer_file = None
        self.is_initialized = False

    def assure_archive_exists(self):
        path_archive = os.path.join(self._path, self.NAME_ARCHIVE_DIR)
        if not os.path.isdir(path_archive):
            os.mkdir(path_archive)

    def move_files_to_archive(self):
        self.assure_archive_exists()
        for file_type in self.MANDATORY_FILES:
            if os.path.isfile(os.path.join(self._path, file_type.name)):
                old_path = os.path.join(self._path, file_type.name)
                new_path = self._avoid_name_duplicate(os.path.join(self._path, self.NAME_ARCHIVE_DIR, file_type.name))
                os.replace(old_path, new_path)
                #current_time = time.time()
                #os.utime(new_path, (self._get_creation_date(new_path), current_time))
            self._file_names = []
            self.is_initialized = False

    @staticmethod
    def _get_creation_date(path_to_file):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

    def _avoid_name_duplicate(self, file_path, iteration: int = 0):
        if os.path.isfile(file_path):
            if iteration == 0:
                path_parts = file_path.split(os.sep)
                file_name_parts = path_parts[-1].split(".")
                new_file_name = ".".join(file_name_parts[:-1])
                new_file_name += "(1)." + file_name_parts[-1]
                new_file_path = os.sep.join(path_parts[:-1]) + os.sep + new_file_name
            else:
                new_file_path = file_path.replace(f"({iteration})", f"({iteration + 1})")
            return self._avoid_name_duplicate(new_file_path, iteration + 1)
        return file_path

    def get_routes_file(self):
        return self._routes_file

    def get_path(self):
        return self._path

    def save_files(self):
        for endpoint_file in self._files:
            endpoint_file.save()

    def get_file_names(self):
        return [f for f in os.listdir(self._path) if os.path.isfile(os.path.join(self._path, f))]

    def initialize(self):
        if not self._file_names:
            self._file_names = self.get_file_names()
            self._check_for_routes_file(self._file_names)
        self.load_files()
        self.is_initialized = True

    def load_files(self):
        self._files = []
        for file in self._file_names:
            endpoint_file = self._get_endpoint_file(file)
            endpoint_file.open()
            if endpoint_file is not None:
                if file == "routes.json":
                    self._routes_file = endpoint_file
                elif file == "timerconsumer.json":
                    self._timer_file = endpoint_file
                else:
                    self._files.append(endpoint_file)

    def _get_endpoint_file(self, file_name: str):
        match file_name:
            case "routes.json":
                return RoutesFile(self._path)
            case "aasserver.json":
                return AasServerFile(self._path)
            case "bacnetconsumer.json":
                return BacnetConsumerFile(self._path)
            case "timerconsumer.json":
                return TimerConsumerFile(self._path)
            case "mongotimeseriesconsumer.json":
                return MongoTimeSeriesConsumerFile(self._path)
            case "modbusconsumer.json":
                return ModbusConsumerFile(self._path)

            case _:
                print(f"Unknown file: {file_name}")
                return None

    def _check_for_routes_file(self, file_names: list):
        for file_name in file_names:
            if file_name == "routes.json":
                return
        raise RuntimeError(f"No routes.json file found in {self._path}")

    def build_mapping(self):
        endpoints_ = {}
        for consumer_file in self._files:
            for unique_id, endpoint in consumer_file.get_endpoints().items():
                endpoints_[unique_id] = endpoint

        mapper = Mapper()
        for route in self._routes_file.get_routes():
            group_name = None
            if isinstance(endpoints_[route.datasource], BacnetEndpoint):
                group_name = str(endpoints_[route.datasource].device_id)
            if route.trigger == "timer":
                pull_interval = self._timer_file.get_period(route.timer_name)

                sinks = [endpoints_[s] for s in route.datasinks]
                mapper.add_mapping(
                    source=endpoints_[route.datasource],
                    sinks=sinks,
                    pull_interval=pull_interval,
                    group=group_name
                )
            elif route.trigger == "event":
                sinks = [endpoints_[s] for s in route.datasinks]
                mapper.add_triggered_mapping(
                    source=endpoints_[route.datasource],
                    sinks=sinks,
                    group=group_name
                )
        return mapper

