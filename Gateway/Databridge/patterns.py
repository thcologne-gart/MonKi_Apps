import copy

from protocols.bacnet.BACnet import Device
from config import ConfigManager




class RelationshipsBuilder:
    def __init__(self, config_manager: ConfigManager, device: Device):
        self.elements = []
        aas_id = config_manager.get_id_aas(device.device_name, device.device_id)["id"]
        aid_id = config_manager.get_id_aid(device.device_name, device.device_id)["id"]
        live_data_id = config_manager.get_id_live_data(device.device_name, device.device_id)["id"]
        object_list = device.get_object_list()
        aas_id_type = config_manager.get_id_aas(device.device_name, device.device_id)["idType"]
        aid_id_type = config_manager.get_id_aid(device.device_name, device.device_id)["idType"]
        live_data_id_type = config_manager.get_id_live_data(device.device_name, device.device_id)["idType"]


        self.prepareElements(
            aas_id,
            aid_id,
            live_data_id,
            aas_id_type,
            aid_id_type,
            live_data_id_type
        )
        for obj in object_list:
            object_identifier = f"{obj[0]}_{obj[1]}"
            self.addElement(
                f"SourceSinkRelation_{len(self.elements)}",
                object_identifier
            )

    def addElement(self,
                   idShort: str,
                   objectIdentifier: str):
        first, second = self.buildFirstAndSecond(objectIdentifier)
        self.elements.append({
            "idShort": idShort,
            "modelType": {
                "name": "RelationshipElement"
            },
            "first": first,
            "second": second
        })

    def buildFirstAndSecond(self, objectIdentifier):
        if objectIdentifier[0].isdigit():
            objectIdentifier = "proprietary_" + objectIdentifier
        var1 = {"type": "SubmodelElementCollection",
                "idType": "IdShort",
                "value": objectIdentifier,
                "local": True}
        first = copy.deepcopy(self.first)
        second = copy.deepcopy(self.second)
        first["keys"].append(var1)
        second["keys"].append(var1)
        return first, second

    def getElements(self):
        return self.elements

    def prepareElements(self,
                        idAAS: str,
                        idAID: str,
                        idLiveDataSubmodel: str,
                        idTypeAAS: str = "IRI",
                        idTypeAID: str = "IRI",
                        idTypeLiveDataSubmodel: str = "IRI"):
        self.first = {
            "keys": [
                {
                    "type": "AssetAdministrationShell",
                    "idType": idTypeAAS,
                    "value": idAAS,
                    "local": True
                },
                {
                    "type": "Submodel",
                    "idType": idTypeAID,
                    "value": idAID,
                    "local": True
                },
                {
                    "type": "SubmodelElementCollection",
                    "idType": "IdShort",
                    "value": "BACnetInterface",
                    "local": True
                },
                {
                    "type": "SubmodelElementCollection",
                    "idType": "IdShort",
                    "value": "InterfaceMetadata",
                    "local": True
                },
                {
                    "type": "SubmodelElementCollection",
                    "idType": "IdShort",
                    "value": "Properties",
                    "local": True
                }
            ]
        }
        self.second = {
            "keys": [
                {
                    "type": "AssetAdministrationShell",
                    "idType": idTypeAAS,
                    "value": idAAS,
                    "local": True
                },
                {
                    "type": "Submodel",
                    "idType": idTypeLiveDataSubmodel,
                    "value": idLiveDataSubmodel,
                    "local": True
                }
            ]
        }

class RelationshipsBuilderV2(RelationshipsBuilder):
    def addElement(self,
                   idShort: str,
                   objectIdentifier: str):
        first, second = self.buildFirstAndSecond(objectIdentifier)
        self.elements.append({
            "idShort": idShort,
            "modelType": "RelationshipElement",
            "first": first,
            "second": second
        })

    def buildFirstAndSecond(self, objectIdentifier):
        if objectIdentifier[0].isdigit():
            objectIdentifier = "proprietary_" + objectIdentifier
        var1 = {"type": "SubmodelElementCollection",
                "value": objectIdentifier}
        first = copy.deepcopy(self.first)
        second = copy.deepcopy(self.second)
        first["keys"].append(var1)
        second["keys"].append(var1)
        return first, second

    def prepareElements(self,
                        idAAS: str,
                        idAID: str,
                        idLiveDataSubmodel: str,
                        idTypeAAS: str = "IRI",
                        idTypeAID: str = "IRI",
                        idTypeLiveDataSubmodel: str = "IRI"):
        self.first = {
            "keys": [
                {
                    "type": "AssetAdministrationShell",
                    "value": idAAS,
                },
                {
                    "type": "Submodel",
                    "value": idAID,
                },
                {
                    "type": "SubmodelElementCollection",
                    "value": "BACnetInterface",
                },
                {
                    "type": "SubmodelElementCollection",
                    "value": "InterfaceMetadata",
                },
                {
                    "type": "SubmodelElementCollection",
                    "value": "Properties",
                }
            ]
        }
        self.second = {
            "keys": [
                {
                    "type": "AssetAdministrationShell",
                    "value": idAAS,
                },
                {
                    "type": "Submodel",
                    "value": idLiveDataSubmodel,
                }
            ]
        }

class AssetInterfaceMappingConfigurationBuilder:
    def __init__(self):
        self.asset_interface_mapping_configuration = {}


    def build(self):
        return self.asset_interface_mapping_configuration

class AssetInterfaceMappingConfigurationBuilderV1(AssetInterfaceMappingConfigurationBuilder):
    def __init__(self, id: str, idAAS: str, idAID: str, idType: str = "IRI", idTypeAAS: str = "IRI",
                 idTypeAID: str = "IRI", idShort: str = "AssetInterfaceMappingConfiguration"):
        super().__init__()
        self.asset_interface_mapping_configuration = {"idShort": idShort,
                                                      "modelType": {
                                                          "name": "Submodel"
                                                      },
                                                      "identification": {
                                                          "id": id,
                                                          "idType": idType
                                                      },
                                                      "semanticId": {"keys": []},
                                                      "submodelElements": [
                                                          {
                                                              "idShort": "Configurations",
                                                              "modelType": {
                                                                  "name": "SubmodelElementCollection"
                                                              },
                                                              "value": [
                                                                  {
                                                                      "idShort": "BacnetMappingConfiguration",
                                                                      "modelType": {
                                                                          "name": "SubmodelElementCollection"
                                                                      },
                                                                      "value": [
                                                                          {
                                                                              "idShort": "ConnectionDescription",
                                                                              "modelType": {
                                                                                  "name": "SubmodelElementCollection"
                                                                              },
                                                                              "value": [
                                                                                  {
                                                                                      "idShort": "Connection",
                                                                                      "modelType": {
                                                                                          "name": "ReferenceElement"
                                                                                      },
                                                                                      "value": {
                                                                                          "keys": [
                                                                                              {
                                                                                                  "type": "AssetAdministrationShell",
                                                                                                  "idType": idTypeAAS,
                                                                                                  "value": idAAS,
                                                                                                  "local": True
                                                                                              },
                                                                                              {
                                                                                                  "type": "Submodel",
                                                                                                  "idType": idTypeAID,
                                                                                                  "value": idAID,
                                                                                                  "local": True
                                                                                              },
                                                                                              {
                                                                                                  "type": "SubmodelElementCollection",
                                                                                                  "idType": "IdShort",
                                                                                                  "value": "BACnetInterface",
                                                                                                  "local": True
                                                                                              }
                                                                                          ]
                                                                                      }
                                                                                  },
                                                                                  {
                                                                                      "idShort": "Security",
                                                                                      "modelType": {
                                                                                          "name": "SubmodelElementCollection"
                                                                                      },
                                                                                      "ordered": False,
                                                                                      "value": []
                                                                                  },
                                                                                  {
                                                                                      "idShort": "ConnectionParameters",
                                                                                      "modelType": {
                                                                                          "name": "SubmodelElementCollection"
                                                                                      },
                                                                                      "ordered": False,
                                                                                      "value": []
                                                                                  }
                                                                              ],
                                                                              "ordered": True
                                                                          },
                                                                          {
                                                                              "idShort": "Mappings",
                                                                              "modelType": {
                                                                                  "name": "SubmodelElementCollection"
                                                                              },
                                                                              "value": [],
                                                                              "ordered": True
                                                                          }
                                                                      ],
                                                                      "ordered": True
                                                                  }
                                                              ],
                                                              "ordered": True
                                                          }
                                                      ],
                                                      "parent": {
                                                          "keys": [
                                                              {
                                                                  "type": "AssetAdministrationShell",
                                                                  "local": False,
                                                                  "value": idAAS,
                                                                  "idType": idTypeAAS
                                                              }
                                                          ]
                                                      }
                                                      }

    def setSemanticId(self, semanticId: dict):
        if "keys" in semanticId.keys():
            self.asset_interface_mapping_configuration["semanticId"] = semanticId
        else:
            self.asset_interface_mapping_configuration["semanticId"]["keys"] = []
            self.asset_interface_mapping_configuration["semanticId"]["keys"].append(semanticId)

    def addRelationshipElement(self, relationshipElement):
        self.addRelationshipElements([relationshipElement])

    def addRelationshipElements(self, relationshipElements: list):
        for smc in self.asset_interface_mapping_configuration["submodelElements"][0]["value"][0]["value"]:
            if smc["idShort"] == "Mappings":
                for relationshipElement in relationshipElements:
                    smc["value"].append(relationshipElement)
                break


class AssetInterfaceMappingConfigurationBuilderV2(AssetInterfaceMappingConfigurationBuilder):
    def __init__(
            self,
            id_: str,
            id_aas: str,
            id_aid: str,
            id_short: str = "AssetInterfaceMappingConfiguration"
    ):
        super().__init__()
        self.asset_interface_mapping_configuration = {"idShort": id_short,
                                                      "modelType": "Submodel",
                                                      "id": id_,
                                                      "semanticId": {"type": "ExternalReference", "keys": []},
                                                      "submodelElements": [
                                                          {
                                                              "idShort": "Configurations",
                                                              "modelType": "SubmodelElementCollection",
                                                              "value": [
                                                                  {
                                                                      "idShort": "BacnetMappingConfiguration",
                                                                      "modelType": "SubmodelElementCollection",
                                                                      "value": [
                                                                          {
                                                                              "idShort": "ConnectionDescription",
                                                                              "modelType": "SubmodelElementCollection",
                                                                              "value": [
                                                                                  {
                                                                                      "idShort": "Connection",
                                                                                      "modelType": "ReferenceElement",
                                                                                      "value": {
                                                                                          "keys": [
                                                                                              {
                                                                                                  "type": "AssetAdministrationShell",
                                                                                                  "value": id_aas,
                                                                                              },
                                                                                              {
                                                                                                  "type": "Submodel",
                                                                                                  "value": id_aid,
                                                                                              },
                                                                                              {
                                                                                                  "type": "SubmodelElementCollection",
                                                                                                  "value": "BACnetInterface",
                                                                                              }
                                                                                          ]
                                                                                      }
                                                                                  },
                                                                                  {
                                                                                      "idShort": "Security",
                                                                                      "modelType": "SubmodelElementCollection",
                                                                                      "value": []
                                                                                  },
                                                                                  {
                                                                                      "idShort": "ConnectionParameters",
                                                                                      "modelType": "SubmodelElementCollection",
                                                                                      "value": []
                                                                                  }
                                                                              ],
                                                                          },
                                                                          {
                                                                              "idShort": "Mappings",
                                                                              "modelType": "SubmodelElementCollection",
                                                                              "value": [],
                                                                          }
                                                                      ],
                                                                  }
                                                              ],
                                                          }
                                                      ]}

    def setSemanticId(self, semanticId: dict):
        if "keys" in semanticId.keys():
            self.asset_interface_mapping_configuration["semanticId"] = semanticId
        else:
            self.asset_interface_mapping_configuration["semanticId"]["keys"] = []
            self.asset_interface_mapping_configuration["semanticId"]["keys"].append(semanticId)

    def addRelationshipElement(self, relationshipElement):
        self.addRelationshipElements([relationshipElement])

    def addRelationshipElements(self, relationshipElements: list):
        for smc in self.asset_interface_mapping_configuration["submodelElements"][0]["value"][0]["value"]:
            if smc["idShort"] == "Mappings":
                for relationshipElement in relationshipElements:
                    smc["value"].append(relationshipElement)
                break


class AssetAdministrationShellBuilder:
    def __init__(self, id: str, idShort: str, assetId: str, submodels: list = [], idType: str = "Custom"):
        self.aas = {
            "modelType": {
                "name": "AssetAdministrationShell"
            },
            "idShort": idShort,
            "identification": {
                "idType": idType,
                "id": id
            },
            "dataSpecification": [

            ],
            "embeddedDataSpecifications": [

            ],
            "submodels": submodels,
            "asset": {
                "keys": [
                    {
                        "type": "Asset",
                        "local": True,
                        "value": assetId,
                        "idType": "Custom"
                    }
                ],
                "modelType": {
                    "name": "Asset"
                },
                "dataSpecification": [

                ],
                "embeddedDataSpecifications": [

                ],
                "idShort": "",
                "identification": {
                    "idType": "IRDI",
                    "id": assetId
                },
                "kind": "Instance"
            },
            "views": [

            ],
            "conceptDictionary": [

            ],
            "category": "CONSTANT",
            "assetRef": {
                "keys": []
            }
        }

    def addSubmodel(self, submodel: dict):
        self.aas["submodels"].append(submodel)

    def addSubmodels(self, submodels: list):
        for submodel in submodels:
            self.addSubmodel(submodel)

    def build(self):
        return self.aas


class SubmodelV2:
    def __init__(self, submodel_id: str, id_short: str = None):
        self.submodel = {
            "modelType": "Submodel",
            "id": submodel_id,
            "submodelElements": []
        }
        self.submodel_id = submodel_id
        if id_short:
            self.submodel.__setitem__("idShort", id_short)

    def setSemanticId(self, semanticId: dict):
        if "keys" in semanticId.keys():
            self.submodel["semanticId"] = semanticId
        else:
            if semanticId not in self.submodel.keys():
                self.submodel["semanticId"] = {"type": "ExternalReference"}
            self.submodel["semanticId"]["keys"] = [semanticId]

    def build(self):
        return self.submodel

class Submodel:
    def __init__(self, id: str, idShort: str, idType: str = "Custom", kind: str = "Instance"):
        self.submodel = {
            "semanticId": {"keys": []},
            "identification": {"idType": idType, "id": id},
            "idShort": idShort,
            "kind": kind,
            "dataSpecification": [],
            "qualifiers": [],
            "modelType": {"name": "Submodel"},
            "embeddedDataSpecifications": [],
            "submodelElements": []
        }

    def addSubmodelElement(self, submodelElement: dict):
        self.submodel["submodelElements"].append(submodelElement)

    def addSubmodelElements(self, submodelElements: list):
        for submodelElement in submodelElements:
            self.addSubmodelElement(submodelElement)

    def setSemanticId(self, semanticId: dict):
        if "keys" in semanticId.keys():
            self.submodel["semanticId"] = semanticId
        else:
            self.submodel["semanticId"]["keys"] = []
            self.submodel["semanticId"]["keys"].append(semanticId)

    def build(self):
        return self.submodel

class AssetAdministrationShellBuilderV2:
    def __init__(self, aas_id: str, asset_kind: str = "Instance", id_short: str = None):
        self.aas = {
            "modelType": "AssetAdministrationShell",
            "assetInformation": {"assetKind": asset_kind},
            "id": aas_id,
        }
        if id_short:
            self.aas.__setitem__("idShort", id_short)

    def addSubmodel(self, submodel: SubmodelV2, type_: str = "ExternalReference"):
        if "submodels" not in self.aas.keys():
            self.aas["submodels"] = []
        submodel_ref = {
            "keys": {
                "type": "Submodel",
                "value": submodel.submodel_id
            },
            "type": type_
        }
        self.aas["submodels"].append(submodel_ref)

    def addSubmodels(self, submodels: list[SubmodelV2]):
        for submodel in submodels:
            self.addSubmodel(submodel)

    def build(self):
        return self.aas


class SubmodelElementCollectionBuilderV2:
    def __init__(self, id_short: str, kind: str = "Instance"):
        self.submodel_element_collection = {
            "kind": kind,
            "modelType": "SubmodelElementCollection",
            "idShort": id_short,
            "value": []
        }

    def build(self):
        return self.submodel_element_collection

class SubmodelElementCollectionBuilder:
    def __init__(self, id_short: str, kind: str = "Instance", ordered: bool = False, allow_duplicates: bool = False):
        self.submodel_element_collection = {
            "ordered": ordered,
            "parent": {"keys": []},
            "semanticId": {"keys": []},
            "idShort": id_short,
            "kind": kind,
            "qualifiers": [],
            "modelType": {"name": "SubmodelElementCollection"},
            "value": [],
            "allowDuplicates": allow_duplicates
        }

    def addElement(self, element: dict):
        self.submodel_element_collection["value"].append(element)

    def build(self):
        return self.submodel_element_collection


class PropertyBuilderV2:
    def __init__(self, id_short: str, value=None):
        self.property = {
            "modelType": "Property",
            "idShort": id_short,
            "value": value if value else ""
        }


    def setValue(self, value: str):
        self.property["value"] = value

    def build(self):
        return self.property


class PropertyBuilder:
    def __init__(self, id_short: str, kind: str = "Instance", value_type: str = "string", value: str = ""):
        self.property = {
            "semanticId": {"keys": []},
            "idShort": id_short,
            "kind": kind,
            "valueType": value_type,
            "qualifiers": [],
            "modelType": {"name": "Property"},
            "value": value
        }

    def setValue(self, value: str):
        self.property["value"] = value

    def build(self):
        return self.property

