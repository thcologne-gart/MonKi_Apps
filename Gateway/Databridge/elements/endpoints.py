import datetime
import json
import pymodbus.client
import Enums
from elements.Parser import BACnetParser
import BAC0
import requests
from elements.mongodb import MongoDB


class Endpoint:
    def __init__(self):
        pass

    def read_value(self):
        pass

    def write_value(self, value: str):
        pass

    def set_trigger(self, datasinks: list):
        pass

class TimerEndpoint(Endpoint):
    def __init__(self, period: int, fixed_rate: bool = True, delay: int = 0):
        super().__init__()
        self._period = period
        self._fixed_rate = fixed_rate
        self._delay = delay


class AasEndpoint(Endpoint):
    def __init__(self, submodel_endpoint: str, id_short_path: str, basyx_version: str):
        super().__init__()
        self._submodel_endpoint = submodel_endpoint
        self._id_short_path = id_short_path
        self._basyx_version = basyx_version.lower()
        self.headers = {'Content-type': 'application/json', "Accept": "*/*"}

        if not submodel_endpoint.endswith("/"):
            submodel_endpoint += "/"

        if self._basyx_version == "v1":
            id_short_path = id_short_path.replace(".", "/")
            self._url = submodel_endpoint + "submodelElements/" + id_short_path
            self._url_end = "/value"
            self.method = requests.put
            self.success_code = 200
        elif self._basyx_version == "v2":
            id_short_path = id_short_path.replace("/", ".")
            self._url = submodel_endpoint + "submodel-elements/" + id_short_path
            self._url_end = "/$value"
            self.method = requests.patch
            self.success_code = 204
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")

    def __repr__(self):
        return f"aas_endpoint: {self._url}"

    def read_value(self):
        r = requests.get(self._url + self._url_end)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
            return ""
        return json.loads(r.text)

    def write_value(self, value):
        """ToDo: specify Exceptions for except"""

        if self._basyx_version == "v2" and not isinstance(value, str):
            try:
                value = json.dumps(value)
            except:
                value = json.dumps(str(value))

        try:
            try:
                return self._do_write(value)
            except TypeError:
                return self._do_write(str(value))
        except Exception as e:
            print(f"Failed to write to AAS-Server: {e.__class__.__name__}: {e}\nURL: {self._url + self._url_end}\nvalue: {value}")
            return False

    def _do_write(self, value):
        r = self.method(self._url + self._url_end, json=value, headers=self.headers)
        if r.status_code != self.success_code:
            print(r.status_code)
            print(r.text)
            print(self._url + self._url_end)
            print(value)
            return False
        #else:
        #    print(r.status_code)
        return True

class ModbusEndpoint(Endpoint):
    def __init__(self,
                 modbus_client: pymodbus.client.ModbusSerialClient,
                 device_id: int,
                 register_address: int,
                 nr_register: int,
                 type_: str
                 ):
        super().__init__()
        self.modbus_client = modbus_client
        self.device_id = device_id
        self.register_address = register_address
        self.nr_register = nr_register
        self.type = type_
        match type_:
            case "coil":
                self.func_read = self.modbus_client.read_coils
            case "discrete_input":
                self.func_read = self.modbus_client.read_discrete_inputs
            case "input_register":
                self.func_read = self.modbus_client.read_input_registers
            case "holding_register":
                self.func_read = self.modbus_client.read_holding_registers

    def __repr__(self):
        return f"modbus_endpoint: device {self.device_id}, reg {self.register_address}({self.nr_register} registers)"

    def write_value(self, value: str):
        print(f"Modbus writing not implemented yet")

    def read_value(self):
        try:
            return self.func_read(address=self.register_address, count=self.nr_register, slave=self.device_id).registers
        except:
            return None

class BacnetEndpoint(Endpoint):
    def __init__(self,
                 bacnet: BAC0.scripts.Base,
                 device_id: int,
                 ip_address: str,
                 object_type: str,
                 instance_nr: int,
                 property_id: int
                 ):
        super().__init__()
        self.bacnet = bacnet
        self.device_id = device_id
        self.ip_address = ip_address
        self.object_type = object_type
        self.instance_nr = instance_nr
        self.property_id = property_id
        self.linked_datasinks = None

    def __repr__(self):
        return f"bacnet_endpoint: device: {self.device_id}({self.ip_address}), object: {self.object_type}_{self.instance_nr}, property: {self.property_id}"

    def read_value(self):
        #if isinstance(self.property_id, int) and propertyNameForId[self.property_id] in double_mapped_props:
        #    print(f"{self.object_type}_{self.instance_nr}: {propertyNameForId[self.property_id]}")
        #if isinstance(self.property_id, str) and self.property_id in double_mapped_props:
        #    print(f"{self.object_type}_{self.instance_nr}: {self.property_id}")
        try:
            value = self.bacnet.read(f"{self.ip_address} {self.object_type} {self.instance_nr} {self.property_id}")
            return BACnetParser.parse(value)
        except BAC0.core.io.IOExceptions.NoResponseFromController:
            return None
        except BAC0.core.io.IOExceptions.UnknownObjectError:
            print("UnknownObjectError happened. This should not happen...")
            return None

    def write_value(self, value: str):
        self.bacnet.write(f"{self.ip_address} {self.object_type} {self.instance_nr} {self.property_id} {value} - 8")

    def _cov_callback(self, elements: dict):
        value = elements['properties']['presentValue']
        for endpoint in self.linked_datasinks:
            endpoint.write_value(value)

    def set_trigger(self, datasinks: list[Endpoint]):
        self.linked_datasinks = datasinks
        self.bacnet.cov(
            address=self.ip_address,
            objectID=(self.object_type, self.instance_nr),
            callback=self._cov_callback,
            confirmed=False
        )


class MongoDbEndpoint(Endpoint):
    def __init__(self,
                 mongo_db: MongoDB,
                 database_name: str,
                 collection_name: str
                 ):
        super().__init__()
        self._mongo_db = mongo_db
        self.database_name = database_name
        self.collection_name = collection_name


class MongoDbTimeSeriesEndpoint(MongoDbEndpoint):
    def __init__(self,
                 mongo_db: MongoDB,
                 database_name: str,
                 collection_name: str,
                 submodel_name: str,
                 id_short_path: str
                 ):
        super().__init__(mongo_db,
                         database_name,
                         collection_name)
        self.submodel_name = submodel_name
        self.short_id_path = id_short_path

    def write_value(self, value):
        if not self._mongo_db.contains_collection(self.database_name, self.collection_name):
            self._mongo_db.create_time_series_database_collection(self.database_name, self.collection_name)
        col = self._mongo_db.get_collection(self.database_name, self.collection_name)
        self._mongo_db.insert_time_series_value(
            collection=col,
            submodel_name=self.submodel_name,
            id_short_path=self.short_id_path,
            datetime=datetime.datetime.now(),
            value=value
        )


class Element:
    def __init__(self):
        pass


class RouteElement(Element):
    def __init__(self, datasource: str, datasinks: list[str], trigger: Enums.TriggerType, timer_name: str = None):
        super().__init__()
        self.datasource = datasource
        self.datasinks = datasinks
        self.trigger = trigger
        self.timer_name = timer_name

