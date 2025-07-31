import base64

import requests
import json
from enum import Enum
from aas.asset_interfaces_description import AssetInterfacesDescription
from config import ConfigManager
from patterns import AssetAdministrationShellBuilder, Submodel, SubmodelElementCollectionBuilder, PropertyBuilder, \
    AssetInterfaceMappingConfigurationBuilder, RelationshipsBuilder, SubmodelV2, SubmodelElementCollectionBuilderV2, \
    PropertyBuilderV2, RelationshipsBuilderV2, AssetInterfaceMappingConfigurationBuilderV2, \
    AssetAdministrationShellBuilderV2, AssetInterfaceMappingConfigurationBuilderV1
from protocols.bacnet.BACnet import Device
from utils import utils


class BasyxVersion(Enum):
    V1 = 1
    V2 = 2


class AasCommunicator:
    def __init__(self, config_manager: ConfigManager):
        ## for testing only
        if not config_manager:
            self.server = AasServerV2("http://139.6.140.150:8081/shells/")
            self.registry = None
            self.version = "v2"

        else:
            self.version = config_manager.get_basyx_version()
            if self.version == "v1":
                self.server = AasServerV1(config_manager.getServerUrl())
                self.registry = AasRegistryV1(config_manager.getRegistryUrl())
            elif self.version == "v2":
                self.server = AasServerV2(config_manager.getServerUrl())
                self.registry = AasRegistryV2(config_manager.getRegistryUrl())
            else:
                raise RuntimeError(f"{self.version} not implemented")

    def get_server_url(self):
        return self.server.get_url()

    def get_registry_url(self):
        if self.registry:
            return self.registry.get_url()
        return None

    def create_aas_bacnet(self, config_manager: ConfigManager, device: Device, submodels: list):
        self.server.create_aas_bacnet(config_manager, device, submodels)

    def get_submodels(self, semantic_id: dict):
        if self.version == "v1":
            return self.registry.get_submodels(semantic_id)
        elif self.version == "v2":
            return self.server.get_submodels(semantic_id)
        else:
            return []

    def add_aas(self, aas: dict):
        self.server.add_aas(aas)

    def add_submodel(self, aas_id: str, submodel: dict):
        self.server.add_submodel(aas_id, submodel)
        if self.registry:
            self.registry.assure_submodel_is_registered(aas_id, submodel)

    def get_submodel(self, aas_id: str, submodel_id: str) -> dict:
        return self.server.get_submodel(aas_id, submodel_id)

    def get_sm_metadata(self, submodel_id):
        if self.version == "v1":
            return None
        elif self.version == "v2":
            return self.server.get_sm_metadata(submodel_id)
        else:
            return None

    def get_aas(self, aas_id: str) -> dict:
        return self.server.get_aas(aas_id)

    def get_aas_id_for_submodel(self, submodel_id):
        if self.version == "v1":
            return None
        elif self.version == "v2":
            return self.server.get_aas_id_for_submodel(submodel_id)
        else:
            return None


class AasComponent:
    def __init__(self, url: str):
        if not url.endswith("/"):
            url += "/"
        self.url = url

    def get_url(self):
        return self.url

    @staticmethod
    def do_read(url: str) -> dict | list:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"GET failed:\r{r.status_code}\r{r.text}")
            return {}
        return json.loads(r.text)

    @staticmethod
    def put(url: str, element):
        r = requests.put(url, str(element))
        # if isinstance(element, dict) and "modelType" in element.keys():
        #    print(f"Added {element['modelType']['name']}")
        return r

    @staticmethod
    def post(url: str, element):
        headers = {'Content-type': 'application/json', "Accept": "*/*"}
        r = requests.post(url, json.dumps(element), headers=headers)
        return r

    @staticmethod
    def encode_id(id_: str):
        id_bytes = id_.encode("utf8")
        return base64.b64encode(id_bytes).decode("utf8")

    @staticmethod
    def decode_id(encoded_id: str):
        return base64.b64decode(encoded_id).decode("utf8")


class AasRegistry(AasComponent):
    def get_aas_descriptor(self, aas_id: str):
        pass

    def register_aas(self, aas_id: str):
        pass

    def register_submodel(self, aas_id: str, submodel: dict, aas_desc: dict):
        pass

    def get_submodels(self, semantic_id: dict):
        pass

    def get_submodel_urls(self, semantic_id: dict):
        pass

    def assure_submodel_is_registered(self, aas_id: str, submodel: dict):
        pass

    def assure_submodels_are_registered(self, aas_id: str, submodels: list[dict]):
        for submodel in submodels:
            self.assure_submodel_is_registered(aas_id, submodel)


class AasRegistryV1(AasRegistry):
    def get_aas_descriptor(self, aas_id: str):
        r = requests.get(self.url + aas_id)
        if r.status_code != 200:
            print(f"Unknown aas: {aas_id}")
        return json.loads(r.text)

    def register_submodel(self, aas_id: str, submodel: dict, aas_desc: dict):
        url_aas = aas_desc["endpoints"][0]["address"]
        if not url_aas.endswith("/"):
            url_aas += "/"
        id_short = submodel["idShort"]
        url_submodel = url_aas + "submodels/" + id_short.replace("/", "%2F") + "/submodel"

        submodel_desc = {
            "idShort": submodel["idShort"],
            "identification": submodel["identification"],
            "description": [],
            "semanticId": submodel["semanticId"],
            "endpoints": [{
                "type": "http",
                "address": url_submodel
            }]
        }
        url_submodel_desc = self.url + aas_id + "/submodels/" + submodel["identification"]["id"].replace(
            "/", "%2F")
        r = requests.put(url_submodel_desc, str(submodel_desc))
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)

    def get_submodels(self, semantic_id: dict):
        urls = self.get_submodel_urls(semantic_id)
        submodels = []
        for url in urls:
            submodels.append(self.do_read(url))
        return submodels, urls

    def get_submodel_urls(self, semantic_id: dict):
        full_content = self.do_read(self.url)
        urls = []
        for aas_descriptor in full_content:
            for submodel_descriptor in aas_descriptor["submodels"]:
                if submodel_descriptor["semanticId"].__eq__(semantic_id):
                    urls.append(submodel_descriptor["endpoints"][0]["address"])
        return urls

    def assure_submodel_is_registered(self, aas_id: str, submodel: dict):
        aas_id = aas_id.replace("/", "%2F")
        aas_desc = self.get_aas_descriptor(aas_id)
        is_registered = False
        for var1 in aas_desc["submodels"]:
            if var1["identification"]["id"] == submodel["identification"]["id"]:
                is_registered = True
                break
        if not is_registered:
            self.register_submodel(aas_id=aas_id, submodel=submodel, aas_desc=aas_desc)


class AasRegistryV2(AasRegistry):
    def __init__(self, url: str):
        super().__init__(url)
        self.url = self.url[:-1]

    def register_aas_(self, aas: dict, url_server: str):
        mandatory_keys = ["id"]
        optional_keys = [
            "description",
            "displayName",
            "extensions",
            "administration",
            "assetKind",
            "assetType",
            "globalAssetId",
            "idShort",
            "specificAssetIds",
        ]
        aas_descriptor = self._build_descriptor(aas, mandatory_keys, optional_keys)
        aas_id = aas['id']
        if type(aas_descriptor) == list:
            print(f"Cannot register AAS {aas_id}, missing mandatory keys:\n{aas_descriptor}")
            return False

        aas_descriptor["submodelDescriptors"] = []
        endpoint = {
            "interface": "AAS-1.0",
            "protocolInformation": {
                "href": url_server + "/" + self.encode_id(aas_id)
            }
        }
        aas_descriptor["endpoints"] = [endpoint]

        r = requests.post(self.url, json=aas_descriptor)
        if r.status_code == 201:
            print(f"Registered AAS {aas_id}")
            return True
        else:
            print(f"Could not register AAS {aas_id}:\nHTTP response code {r.status_code}\nresponse message: {r.text}")
            return False

    def _build_descriptor(
            self,
            element: dict,
            mandatory_keys: list[str],
            optional_keys: list[str]) -> dict | list:
        descriptor = {}
        missing_keys = []

        for m_key in mandatory_keys:
            if m_key in element.keys():
                descriptor[m_key] = element[m_key]
            else:
                missing_keys.append(m_key)

        if len(missing_keys) != 0:
            return missing_keys

        for o_key in optional_keys:
            if o_key in element.keys():
                descriptor[o_key] = element[o_key]
        return descriptor

    def register_submodel_(self, submodel: dict, url_server: str, aas_id: str):
        submodel_id = submodel["id"]
        if not aas_id:
            print(f"Cannot register submodel {submodel_id} due to missing AAS Id (submodel not linked to any AAS)")
            return

        mandatory_keys = ["id"]
        optional_keys = [
            "description",
            "displayName",
            "extensions",
            "administration",
            "idShort",
            "semanticId",
            "supplementalSemanticId	"
        ]

        submodel_descriptor = self._build_descriptor(submodel, mandatory_keys, optional_keys)
        if type(submodel_descriptor) == list:
            print(f" AAS {aas_id}, missing mandatory keys:\n{submodel_descriptor}")
            return False

        endpoint = {
            "interface": "SUBMODEL-1.0",
            "protocolInformation": {
                "href": url_server.replace("shells", "submodels") + "/" + self.encode_id(submodel_id)
            }
        }
        submodel_descriptor["endpoints"] = [endpoint]

        r = requests.post(self.url + f"/{self.encode_id(aas_id)}/submodel-descriptors", json=submodel_descriptor)
        if r.status_code == 201:
            print(f"Registered submodel {submodel_id} to AAS {aas_id}")
            return True
        else:
            print(
                f"Could not register submodel {submodel_id} to AAS {aas_id}:\nHTTP response code {r.status_code}\nresponse message: {r.text}")
            return False


class AasServer(AasComponent):
    def add_aas(self, aas: dict):
        pass

    def create_aas_bacnet(self, config_manager: ConfigManager, device: Device, submodels: list):
        pass

    def get_aas(self, aas_id: str) -> dict:
        pass

    def add_submodel(self, aas_id: str, submodel: dict):
        pass

    def get_submodel(self, aas_id: str, submodel_id: str):
        pass


class AasServerV1(AasServer):
    def add_aas(self, aas: dict):
        aas_id = aas["identification"]["id"]
        url_aas = self.url + aas_id.replace("/", "%2F")
        return self.put(url_aas, aas)

    def get_aas(self, aas_id: str) -> dict:
        return self.do_read(self.url + aas_id + "/aas")

    def add_submodel(self, aas_id: str, submodel: dict):
        submodel_id_short = submodel["idShort"]
        url_submodel = self.url + aas_id.replace("/", "%2F") + "/aas/submodels/" + submodel_id_short.replace("/", "%2F")
        return self.put(url_submodel, submodel)

    def get_submodel(self, aas_id: str, submodel_id: str):
        pass

    def create_aas_bacnet(self, config_manager: ConfigManager, device: Device, submodels: list):
        aas_id = config_manager.get_id_aas(device.device_name, device.device_id)["id"]
        aas_id_type = config_manager.get_id_aas(device.device_name, device.device_id)["idType"]

        asset_id = config_manager.getAssetId(device.device_name, device.device_id)
        aas_id_short = config_manager.getIdShortAAS(device.device_name, device.device_id)
        aas = AssetAdministrationShellBuilder(aas_id, aas_id_short, asset_id, idType=aas_id_type).build()
        r = self.add_aas(aas)
        if r.status_code == 200:
            utils.log(f"Published AAS '{aas_id}' for device '{device.device_id}({device.device_name})'")
        else:
            pass
        for submodel in submodels:
            r = self.add_submodel(aas_id, submodel)
            if r.status_code == 200:
                utils.log(f"Added Submodel '{submodel['idShort']}' to AAS '{aas_id}'")
            else:
                print(r.status_code)
                print(r.text)

        url_registry = config_manager.getRegistryUrl()
        registry = AasRegistryV1(url_registry)
        registry.assure_submodels_are_registered(aas_id, submodels)

        return aas


class AasServerV2(AasServer):
    def __init__(self, url: str):
        super().__init__(url)
        self.headers = {'Content-type': 'application/json', "Accept": "*/*"}

        if self.url.endswith("shells/"):
            self.url = self.url.replace("shells/", "")

    def get_aas_id_for_submodel(self, submodel_id: str):
        all_aas = self.do_read(self.url + "shells/")["result"]
        for aas in all_aas:
            aas_id = aas["id"]
            for ref in aas["submodels"]:
                for key in ref["keys"]:
                    if key["value"] == submodel_id:
                        return aas_id
        return None

    def get_sm_metadata(self, submodel_id: str):
        return self.do_read(self.url + f"submodels/{self.encode_id(submodel_id)}/$metadata")

    def get_submodels(self, semantic_id: dict):
        # all_aas = self.do_read(self.url + "shells/")["result"]
        # sm_aas_dict = {}
        # for aas in all_aas:
        #    aas_id = aas["id"]
        #    for key in aas["submodels"]["keys"]:
        #        if key["type"] == "Submodel":
        #            sm_aas_dict[key["value"]] = aas_id
        #            break
        ## dict: {sm_id: aas_id}

        submodels = self.do_read(self.url + "submodels/")["result"]
        matching_submodels = []
        for submodel in submodels:
            if "semanticId" in submodel.keys() and submodel["semanticId"].__eq__(semantic_id):
                matching_submodels.append(submodel)
        return matching_submodels

    def add_aas(self, aas: dict):
        return self.post(self.url + "shells", aas)

    def get_aas(self, aas_id: str) -> dict:
        return self.do_read(self.url + "shells/" + self.encode_id(aas_id))

    def get_submodel(self, aas_id: str, submodel_id: str):
        return self.do_read(self.url + "submodels/" + self.encode_id(submodel_id))

    def add_submodel(self, aas_id: str, submodel: dict):
        r = self.post(self.url + "submodels", submodel)
        submodel_ref = {
            "keys": {
                "type": "Submodel",
                "value": submodel["id"]
            },
            "type": "ExternalReference"
        }
        r = self.post(self.url + "shells/" + self.encode_id(aas_id) + "/submodel-refs", submodel_ref)
        return r

    def create_aas_bacnet(self, config_manager: ConfigManager, device: Device, submodels: list):
        aas_id = config_manager.get_id_aas(device.device_name, device.device_id)["id"]

        asset_id = config_manager.getAssetId(device.device_name, device.device_id)
        aas_id_short = config_manager.getIdShortAAS(device.device_name, device.device_id)
        aas = AssetAdministrationShellBuilderV2(aas_id, id_short=aas_id_short).build()

        r = self.add_aas(aas)
        if r.status_code == 201:
            utils.log(f"Published AAS '{aas_id}' for device '{device.device_id}({device.device_name})'")

        else:
            print(f"Failed to publish aas:")
            print(r.status_code)
            print(r.text)
        for submodel in submodels:
            r = self.add_submodel(aas_id, submodel)
            if r.status_code == 201:
                utils.log(f"Added Submodel '{submodel['idShort']}' to AAS '{aas_id}'")
            else:
                print(r.status_code)
                print(r.text)

        return aas


class ShellBuilder:
    @staticmethod
    def build_live_data_submodel(config_manager: ConfigManager, device: Device):
        basyx_version = config_manager.get_basyx_version()
        idLiveData = config_manager.get_id_live_data(device.device_name, device.device_id)
        if basyx_version == "v1":
            submodel_builder = Submodel(idLiveData["id"], "BACnetDatapointsInformation", idType=idLiveData["idType"])
            smc_builder = SubmodelElementCollectionBuilder
            prop_builder = PropertyBuilder
        elif basyx_version == "v2":
            submodel_builder = SubmodelV2(idLiveData["id"], "BACnetDatapointsInformation")
            smc_builder = SubmodelElementCollectionBuilderV2
            prop_builder = PropertyBuilderV2
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")
        submodel_builder.setSemanticId(config_manager.getSemanticIdLiveData())
        submodel = submodel_builder.build()

        #device.browse()
        for objectIdentifier, propList in device.get_obj_prop_map().items():
            if objectIdentifier.isnumeric():
                objectIdentifier = "proprietary_" + objectIdentifier
            object_smc = smc_builder(objectIdentifier).build()
            for prop in propList:
                object_smc["value"].append(prop_builder(id_short=str(prop)).build())

            submodel["submodelElements"].append(object_smc)

        return submodel

    @staticmethod
    def build_aimc_submodel(config_manager: ConfigManager, device: Device):

        aas_id = config_manager.get_id_aas(device.device_name, device.device_id)["id"]
        aid_id = config_manager.get_id_aid(device.device_name, device.device_id)["id"]
        device_name = device.device_name
        device_id = device.device_id
        aas_id_type = config_manager.get_id_aas(device.device_name, device.device_id)["idType"]
        aid_id_type = config_manager.get_id_aid(device.device_name, device.device_id)["idType"]
        idAIMC = config_manager.get_id_aimc(device_name, device_id)

        basyx_version = config_manager.get_basyx_version()
        if basyx_version == "v1":
            rel_builder = RelationshipsBuilder(config_manager, device)
            relations = rel_builder.getElements()
            aimc_builder = AssetInterfaceMappingConfigurationBuilderV1(
                idAIMC["id"],
                aas_id,
                aid_id,
                idAIMC["idType"],
                aas_id_type,
                aid_id_type,
                config_manager.getIdShortAIMC(device_name, device_id)
            )
        elif basyx_version == "v2":
            rel_builder = RelationshipsBuilderV2(config_manager, device)
            relations = rel_builder.getElements()

            aimc_builder = AssetInterfaceMappingConfigurationBuilderV2(
                idAIMC["id"],
                aas_id,
                aid_id,
                config_manager.getIdShortAIMC(device_name, device_id)
            )
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")

        semanticIdAimc = config_manager.getSemanticIdAIMC()
        aimc_builder.setSemanticId(semanticIdAimc)
        aimc_builder.addRelationshipElements(relations)
        return aimc_builder.build()

    @staticmethod
    def build_aid_submodel(device: Device, config_manager: ConfigManager):
        idAidSM = config_manager.get_id_aid(device.device_name, device.device_id)
        idShortAid = config_manager.getIdShortAID(device.device_name, device.device_id)

        basyx_version = config_manager.get_basyx_version()
        if basyx_version == "v1":
            submodelBuilder = Submodel(idAidSM["id"], idShortAid, idType=idAidSM["idType"])
            smc_builder = SubmodelElementCollectionBuilder
            prop_builder = PropertyBuilder
        elif basyx_version == "v2":
            submodelBuilder = SubmodelV2(idAidSM["id"], idShortAid)
            smc_builder = SubmodelElementCollectionBuilderV2
            prop_builder = PropertyBuilderV2

        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")
        submodelBuilder.setSemanticId(config_manager.getSemanticIdAID())
        submodel = submodelBuilder.build()

        endpointMetadata = smc_builder("EndpointMetadata").build()
        interfaceMetadata = smc_builder("InterfaceMetadata").build()
        aid_properties = smc_builder("Properties").build()
        operations = smc_builder("Operations").build()
        events = smc_builder("Events").build()

        #objectPropMap = {}
        object_counter = 0

        object_list = device.get_object_list()
        nr_objects = len(object_list)
        for object_identifier, property_list in device.get_obj_prop_map().items():
            #utils.log(f"Objects browsed: {str(object_counter)}/{str(nr_objects)}", end="\r")

            #objectIdentifier = str(object_[0]) + "_" + str(object_[1])
            if object_identifier[0].isdigit():
                var3 = smc_builder("proprietary_" + object_identifier).build()
            else:
                var3 = smc_builder(object_identifier).build()

            var3["value"].append(prop_builder(id_short="bacnet:ObjectType", value=object_identifier.split("_")[0]).build())
            var3["value"].append(prop_builder(id_short="bacnet:InstanceNumber", value=str(object_identifier.split("_")[1])).build())
            var3["value"].append(
                prop_builder(id_short="bacnet:service", value=str(device.services_supported)).build())
            var3["value"].append(smc_builder(id_short="dataMapping").build())

            #property_list = device.get_properties(object_[0], object_[1])
            #objectPropMap[objectIdentifier] = property_list
            var3["value"].append(prop_builder(id_short="bacnet:PropertyList", value=str(property_list)).build())

            aid_properties["value"].append(var3)

            object_counter += 1

            if object_counter == nr_objects:
                utils.log(f"Objects browsed: {str(object_counter)}/{str(nr_objects)}", end="\n")

        interfaceMetadata["value"].append(aid_properties)
        interfaceMetadata["value"].append(operations)
        interfaceMetadata["value"].append(events)

        endpointMetadata["value"].append(
            prop_builder(id_short="base", value=f"bacnet:{device.ip_address}").build())
        endpointMetadata["value"].append(prop_builder(id_short="contentType").build())
        endpointMetadata["value"].append(smc_builder(id_short="securityDefinition").build())
        endpointMetadata["value"].append(
            smc_builder(id_short="alternativeEndpointMetadata").build())

        BACnetInterface = smc_builder("BACnetInterface").build()
        BACnetInterface["value"].append(endpointMetadata)
        BACnetInterface["value"].append(interfaceMetadata)

        submodel["submodelElements"].append(BACnetInterface)

        return submodel#, objectPropMap

    @staticmethod
    def create_shells(device: Device, aas_server: AasServer, config_manager: ConfigManager):
        # mapping: dict):
        device.browse()

        config_manager.update_all_ids(device.device_name, device.device_id)
        aas_identification = config_manager.get_id_aas(device.device_name, device.device_id)
        aas_id = aas_identification["id"]

        id_short_live_data = config_manager.getIdShortLiveData(device.device_id, device.device_name).replace('/', '%2F')

        url_server = aas_server.get_url()
        # mapping[device.device_id] = {}

        submodels = []
        #aid, objectPropMap = ShellBuilder.build_aid_submodel(device, config_manager)
        aid = ShellBuilder.build_aid_submodel(device, config_manager)

        ### Mapping build

        aid_submodel = AssetInterfacesDescription(aid, aas_id)
        basyx_version = config_manager.get_basyx_version()
        if basyx_version == "v1":
            url = url_server + f"{aas_id.replace('/', '%2F')}/aas/submodels/{config_manager.getIdShortAID(device.device_name, device.device_id)}/submodel/"
        elif basyx_version == "v2":
            if url_server.endswith("/"):
                url_server = url_server[:-1]
            url = url_server + f"{AasComponent.encode_id(aid_submodel.get_id())}"
        else:
            raise RuntimeError(f"Basyx version {basyx_version} not implemented")

        aid_submodel.set_url(url)

        ###

        # mapping[device.device_id]["objects"] = objectPropMap
        submodels.append(aid)

        liveData = ShellBuilder.build_live_data_submodel(config_manager, device)
        submodels.append(liveData)

        aimc = ShellBuilder.build_aimc_submodel(config_manager, device)
        submodels.append(aimc)

        aas_server.create_aas_bacnet(config_manager, device, submodels)
