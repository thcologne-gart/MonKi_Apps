import files
from config import ConfigManager, ConfigManagerStatic
from console.socket_console import Console
from protocols.communicator import Communicator

def main():
    ConfigManagerStatic.init()
    file_handler = files.FileHandler(path="config")
    config_manager = ConfigManager()
    Communicator.set_config_manager(config_manager)
    console = Console(config_manager=config_manager, file_handler=file_handler)

if __name__ == "__main__":
    main()

