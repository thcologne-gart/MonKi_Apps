import json
import requests

from config import ConfigManagerStatic


class AssetInterfaceDescription:
    def __init__(self, dict_: dict):
        self._content = dict_

    def __str__(self):
        return str(self._content)

    def get_id_short(self):
        return self._content["idShort"]

    def get_base(self):
        for sme in self._content["value"]:
            if sme["idShort"] == "EndpointMetadata":
                for elem in sme["value"]:
                    if elem["idShort"] == "base":
                        return elem["value"]


    def get_properties(self):
        for sme in self._content["value"]:
            if sme["idShort"] == "InterfaceMetadata":
                for elem in sme["value"]:
                    if elem["idShort"] == "Properties":
                        return elem["value"]

    def get_events(self):
        pass

    def get_operations(self):
        pass


class AssetInterfaceDescriptionV2(AssetInterfaceDescription):
    pass


class AssetInterfacesDescription:
    def __init__(self, dict_: dict, aas_id: str = None):
        self._asset_interface_descriptions = {}
        for aid in dict_["submodelElements"]:
            self.add_aid(AssetInterfaceDescription(aid))

        self._aas_id = aas_id

        if "identification" in dict_.keys():
            self._id = dict_["identification"]["id"]
        elif "id" in dict_.keys():
            self._id = dict_["id"]
        elif "idShort" in dict_.keys():
            self._id = dict_["idShort"]
        else:
            self._id = None

        self._url = None #if ConfigManagerStatic.get_basyx_version() == "v1" else ConfigManagerStatic.get_server_url() + f"submodels/{AasComponent.encode_id(self._id)}"


    def set_url(self, url: str):
        self._url = url

    def get_url(self):
        return self._url

    def get_id(self):
        return self._id

    def get_aid(self, id_short_aid) -> AssetInterfaceDescription:
        return self._asset_interface_descriptions[id_short_aid] if id_short_aid in self._asset_interface_descriptions.keys() else None

    def get_aas_id(self):
        if self._aas_id:
            return self._aas_id
        next_is_id = False
        if self._url:
            for part in self._url.split("/"):
                if next_is_id:
                    return part.replace("%2F", "/")
                if part == "shells":
                    next_is_id = True
        return None

    def get_aids(self):
        return self._asset_interface_descriptions

    def add_aid(self, aid: AssetInterfaceDescription):
        self._asset_interface_descriptions[aid.get_id_short()] = aid


class AssetInterfacesDescriptionV2(AssetInterfacesDescription):
    pass
