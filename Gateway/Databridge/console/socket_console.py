#!/usr/bin/env python3
import datetime
import socket
import selectors
import threading
import traceback
import types
from mapper import Mapper
from config import ConfigManager
from protocols.communicator import Communicator
from files import FileHandler, BacnetConsumerFile

sel = selectors.DefaultSelector()


class Console:
    def __init__(self, config_manager: ConfigManager, file_handler: FileHandler, mapper: Mapper = None):
        self.mapper = mapper
        self.config_manager = config_manager
        self.file_handler = file_handler
        thread = threading.Thread(target=self.wait_for_command)
        thread.start()
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)


    def service_connection(self, key, mask):
        sock = key.fileobj
        self.data = key.data
        if mask & selectors.EVENT_READ:

            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                cmd = str(recv_data, encoding='utf-8')
                if len(cmd) == 0:
                    resp = bytes(f"No args provided\0", "utf-8")
                    self.data.msg_total = len(resp)
                    self.data.outb += resp
                elif cmd.count(" ") > 0:
                    command = cmd.split(" ")[0]
                    args = cmd.split(" ")[1:]
                else:
                    command = cmd
                    args = []
                self.execute_command(command, args, sock)
                #self.data.outb += recv_data
            else:
                print(f"Closing connection to {self.data.addr}")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if self.data.outb:
                try:
                    print(f"Echoing {self.data.outb!r} to {self.data.addr}")
                    sent = sock.send(self.data.outb)  # Should be ready to write
                    self.data.outb = self.data.outb[sent:]
                except:
                    pass

    #if len(sys.argv) != 3:
    #    print(f"Usage: {sys.argv[0]} <host> <port>")
    #    sys.exit(1)
    #host, port = sys.argv[1], int(sys.argv[2])

    def get_own_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except:
            return "127.0.0.1"

    def wait_for_command(self):
        host, port = self.get_own_ip(), 4711

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def execute_command(self, command: str, args: list, sock: socket.socket):
        match command:
            case "start":
                try:
                    if self.mapper is None:
                        resp = bytes(f"No mapping build yet. Use build-mapping-<protocol> first\0", "utf-8")
                    elif len(args) == 0:
                        resp = bytes(self.mapper.start_mapping() + "\0", 'utf-8')
                    elif len(args) == 1:
                        resp = bytes(self.mapper.start_group(args[0]) + "\0", 'utf-8')
                    elif len(args) == 2:
                        resp = bytes(self.mapper.start_subgroup(args[0], args[1]) + "\0", 'utf-8')
                    else:
                        resp = bytes(f"Cannot handle provided args: {args}\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "stop":
                try:
                    if self.mapper is None:
                        resp = bytes(f"No mapping build yet. Use build-mapping-<protocol> first\0", "utf-8")
                    elif len(args) == 0:
                        resp = bytes(self.mapper.stop_mapping() + "\0", 'utf-8')
                    elif len(args) == 1:
                        resp = bytes(self.mapper.stop_group(args[0]) + "\0", 'utf-8')
                    elif len(args) == 2:
                        resp = bytes(self.mapper.stop_subgroup(args[0], args[1]) + "\0", 'utf-8')
                    else:
                        resp = bytes(f"Cannot handle provided args: {args}\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "change-interval":
                try:
                    if self.mapper is None:
                        resp = bytes(f"No mapping build yet. Use build-mapping-<protocol> first\0", "utf-8")
                    elif len(args) == 3:
                        resp = bytes(self.mapper.change_interval(args[0], args[1], args[2]) + "\0", 'utf-8')
                    elif len(args) == 4:
                        resp = bytes(self.mapper.change_interval(args[0], args[1], args[2], Console.string_to_bool(args[3])) + "\0", 'utf-8')
                    else:
                        resp = bytes(f"Cannot handle provided args: {args}\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "reload-config":
                try:
                    unix_old, unix_new = self.config_manager.reload_config_file()
                    old_mod_time = datetime.datetime.fromtimestamp(unix_old)
                    new_mod_time = datetime.datetime.fromtimestamp(unix_new)
                    resp = bytes(f"config.json reloaded. Old file timestamp: {old_mod_time}, new file timestamp: {new_mod_time}\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "discover-bacnet":
                try:
                    sock.send(b"Starting bacnet discovery")
                    Communicator.discover_bacnet()
                    resp = bytes(f"Discovery done\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "discover-registry":
                try:
                    self.file_handler.move_files_to_archive()
                    bacnet_consumer_file = BacnetConsumerFile(self.file_handler.get_path())
                    bacnet_consumer_file.discover_registry(config_manager=self.config_manager)
                    #self.file_handler.initialize()
                    resp = bytes(f"Discovery done\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{traceback.format_exception(e)}\0", "utf-8")
                    #resp = bytes(f"{e.__class__.__name__}: {e.__traceback__}\0", "utf-8")

            case "build-mapping":
                try:
                    if not self.file_handler.is_initialized:
                        self.file_handler.initialize()
                    self.mapper = self.file_handler.build_mapping()
                    resp = bytes(f"Success\0", "utf-8")
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case "status":
                try:
                    resp = bytes(str(self.mapper.get_status()) + "\0", 'utf-8')
                except Exception as e:
                    resp = bytes(f"{e.__class__.__name__}: {e}\0", "utf-8")

            case _:
                resp = bytes(f"{command} not implemented (yet)\0", "utf-8")

        self.data.msg_total = len(resp)
        self.data.outb += resp

    @staticmethod
    def string_to_bool(string: str):
        if string.lower() in ["true", "1"]:
            return True
        return False

