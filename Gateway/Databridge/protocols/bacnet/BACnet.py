import datetime
import time
import BAC0
import threading
from utils import utils
import requests
from config import ConfigManager
from utils import utils, propertyNameForId, protocolServices


class Route:
    def __init__(self, datasource: dict, datasink: dict, pull_interval: int):
        self._datasource = datasource
        self._datasink = datasink
        self._pull_interval = pull_interval

    def get_target_url(self):
        submodel_endpoint = self._datasink["submodelEndpoint"]
        id_short_path = self._datasink["idShortPath"]
        return submodel_endpoint + id_short_path if submodel_endpoint.endswith("/") else submodel_endpoint + "/" + id_short_path


class Device:
    def __init__(self, bacnet, device_id: int, ip_address: str, device_name: str = None):
        self.bacnet = bacnet
        self.objects_and_properties = None
        self.do_pull = False
        self.pull_interval = ConfigManager.DEFAULT_TIMER_PERIOD
        self.device_id = device_id
        self.ip_address = ip_address
        self.device_name = device_name
        self._lock = threading.Lock()
        self.objects = None
        self.aas_url = None
        self.services_supported = None
        self.object_list = None

    def write_to_aas(self, url: str, value: str):
        r = requests.put(url, str(value).replace(" ", ""), headers={"Content-Type": "text/plain; charset=UTF-8"})

#        if r.status_code != 200:
 #           utils.log(r.status_code)
  #          utils.log(r.text)
   #         utils.log(f"Url: {url}")
    #        utils.log(f"Value: {value}")

    def get_services_supported(self):
        if self.services_supported is None:
            try:
                services_supported = self.bacnet.read(f"{self.ip_address} device {self.device_id} protocolServicesSupported")
                self.services_supported = [protocolServices[i] for i in range(len(services_supported)) if services_supported[i] == 1]
            except BAC0.core.io.IOExceptions.UnknownPropertyError:
                self.services_supported = []
        return self.services_supported

    def get_object_list(self):
        if self.object_list is None:
            try:
                self.object_list = self.bacnet.read(f"{self.ip_address} device {self.device_id} objectList")
            except BAC0.core.io.IOExceptions.UnknownPropertyError:
                self.object_list = []
        return self.object_list

    def set_pull_interval(self, interval: int):
        self.pull_interval = interval


    def set_aas_url(self, aas_url: str):
        if aas_url.endswith("/"):
            self.aas_url = aas_url
        else:
            self.aas_url = aas_url + "/"

    def get_properties(self, object_type: str, object_id: int | str):
        obj_identifier = f"{object_type}_{object_id}"
        if not self.objects_and_properties:
            self.browse()
        if obj_identifier in self.objects_and_properties.keys():
            return self.objects_and_properties[obj_identifier]
        return []

    def browse(self):
        utils.log(f"Starting to browse device {self.device_id}({self.device_name})", newline=True)
        object_list = self.get_object_list()
        utils.log(f"Found {len(object_list)} objects")
        self.objects_and_properties = {}
        object_counter = 0
        for obj in object_list:
            utils.log(f"Objects browsed: {object_counter}/{len(object_list)}", end="\r")
            prop_list = self._get_objects_properties(obj[0], obj[1])
            self.objects_and_properties[f"{obj[0]}_{obj[1]}"] = prop_list
            object_counter += 1

    def get_obj_prop_map(self) -> dict[str, list]:
        if not self.objects_and_properties:
            self.browse()
        return self.objects_and_properties

    def _get_objects_properties(self, object_type: str, object_nr: int):
        counter = 0
        try:
            property_list = self.bacnet.read(f'{self.ip_address} {object_type} {object_nr} propertyList')

        except BAC0.core.io.IOExceptions.UnknownPropertyError:
            try:
                property_list = []
                property_tuples = self.bacnet.readMultiple(f'{self.ip_address} {object_type} {object_nr} all',
                                                     show_property_name=True)
                for propertyTuple in property_tuples:
                    try:
                        property_list.append(str(propertyTuple[1]))
                    except:
                        continue
                if len(property_list) < 2:
                    property_list = self._try_all_properties(object_type, object_nr)
            except (KeyError, BAC0.core.io.IOExceptions.SegmentationNotSupported):
                property_list = self._try_all_properties(object_type, object_nr)

        counter += 1
        return property_list

    def _try_all_properties(self, object_type: str, object_nr: int):
        property_list = []
        for prop_id, prop_name in propertyNameForId.items():
            try:
                self.bacnet.read(f'{self.ip_address} {object_type} {object_nr} {prop_id}')
                property_list.append(prop_name)
            except BAC0.core.io.IOExceptions.UnknownPropertyError:
                continue
            except BAC0.core.io.IOExceptions.NoResponseFromController as e:
                utils.log(f"Property {prop_name} cannot be read: ")
                utils.log(e)
        return property_list

    def pull(self):
        for obj, prop_list in self.objects.items():
            if "_" in obj:
                obj_type = obj.split("_")[0]
                obj_instance = obj.split("_")[1]
                for prop in prop_list:
                    try:
                        value = self.bacnet.read(f"{self.ip_address} {obj_type} {obj_instance} {prop}")
                        value = str(value).replace(":", "%3a").replace(" ", "%20").replace("(", "%28").replace(")", "%29").replace("'", "%27").replace(",", "%32").replace("/", "%35").replace("=", "%3D").replace(";", "%3B")
                        #print(f"{self.device_id}: prop: {prop} -> value: {value}")
                        target_url = f"{self.aas_url}{obj}/{prop}/value"
                        self.write_to_aas(target_url, str(value))
                        #if "stopWhenFull" in target_url or "stopWhenFull" in prop:
                        #    print(target_url)
                        #    print(value)
                        #    print(f"Object: {obj}\nProperty: {prop}")
                    except BAC0.core.io.IOExceptions.NoResponseFromController:
                        continue
            else:
                print(f"object without underscore: {obj}")

        #print(f"{self.device_id}: I pulled data")

    def set_objects(self, objects: dict):
        self.objects = objects


    def check_mandatory_fields(self):
        if self.objects is None:
            raise RuntimeError(f"No objects provided for device {self.device_id}. Blank start not implemented yet")
        if self.aas_url is None:
            raise RuntimeError(f"No aas url provided for device {self.device_id}. No target for pulled data")

    def start_pulling(self):
        self.check_mandatory_fields()
        self._lock.acquire()
        self.do_pull = True
        self._lock.release()
        utils.log(f"{self.device_id}: Starting to pull")
        while True:
            t1 = datetime.datetime.now()
            self.pull()
            t2 = datetime.datetime.now()
            pull_duration = (t2-t1).total_seconds()
            utils.log(f"{self.device_id}: Pull successful. Took {str(pull_duration)} s")
            if pull_duration < self.pull_interval:
                time.sleep(self.pull_interval - pull_duration)

            self._lock.acquire()
            if not self.do_pull:
                self._lock.release()
                break
            self._lock.release()
        utils.log(f"{self.device_id}: Stopped pulling")

    def stop_pulling(self):
        self._lock.acquire()
        self.do_pull = False
        self._lock.release()


class DeviceHandler:
    def __init__(self, bacnet, devices_to_handle: dict):
        self.bacnet = bacnet
        self.devices = {}
        self.threads = {}
        for device_id, device_dict in devices_to_handle.items():
            self.devices[device_id] = Device(self.bacnet, device_id, device_dict["ip_address"], None)

    def start_device_neu(self, device: Device):
        if device.do_pull:
            utils.log(f"Device {device.device_id} is already pulling")
        else:
            device.start_pulling()
    def start_device(self, device_id: int):
        if device_id in self.devices.keys():
            self.threads[device_id] = threading.Thread(target=self.devices[device_id].start_pulling)
            self.threads[device_id].start()
        else:
            utils.log(f"Unknown device id {device_id}")

    def set_device_objects(self, device_id: int, objects: dict):
        if device_id in self.devices.keys():
            self.devices[device_id].set_objects(objects)
        else:
            utils.log(f"Unknown device id {device_id}")

    def set_device_interval(self, device_id: int, interval: int):
        if device_id in self.devices.keys():
            self.devices[device_id].set_pull_interval(interval)
        else:
            utils.log(f"Unknown device id {device_id}")

    def set_device_aas_url(self, device_id: int, aas_url: str):
        if device_id in self.devices.keys():
            self.devices[device_id].set_aas_url(aas_url)
        else:
            utils.log(f"Unknown device id {device_id}")
    def set_device_objects_multiple(self, devices: dict):
        for key, value in devices.items():
            self.set_device_objects(key, value["objects"])
            if "aas_url" in value.keys():
                self.set_device_aas_url(key, value["aas_url"])


    def stop_device(self, device_id: int):
        if device_id in self.threads.keys():
            self.devices[device_id].stop_pulling()
            utils.log(f"Device {device_id} stopped")
        else:
            utils.log(f"Device {device_id} not pulling")

    def start(self):
        for device_id in self.devices.keys():
            self.start_device(device_id)

    def stop(self):
        for device_id in self.threads.keys():
            if self.threads[device_id].is_alive():
                self.stop_device(device_id)

