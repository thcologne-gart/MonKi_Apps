from files import FileHandler, BacnetConsumerFile
from config import ConfigManager, ConfigManagerStatic
from protocols.communicator import Communicator

def main():
    ConfigManagerStatic.init()
    file_handler = FileHandler(path="config")
    config_manager = ConfigManager()
    Communicator.set_config_manager(config_manager)

    """
    Diese drei Funktionen können auskommentiert werden, wenn nicht benötigt
    discover_bacnet: erkundet das BACnet-Netzwerk und erstellt die AAS samt Teilmodelle
    discover_registry: erkundet die Registry / den Server nach AIMCs und erstellt daraus die JSON-Dateien für die bridge
    start_mapping: setzt das Mapping basierend auf den JSON-Dateien um
    """

    #discover_bacnet()
    discover_registry(file_handler, config_manager)
    start_mapping(file_handler)


def discover_bacnet():
    Communicator.discover_bacnet()

def discover_registry(file_handler: FileHandler, config_manager: ConfigManager):
    file_handler.move_files_to_archive()
    bacnet_consumer_file = BacnetConsumerFile(file_handler.get_path())
    bacnet_consumer_file.discover_registry(config_manager=config_manager)

def start_mapping(file_handler: FileHandler):
    file_handler.initialize()
    mapper = file_handler.build_mapping()
    mapper.start_mapping()


if __name__ == "__main__":
    main()

