import threading
from elements.endpoints import Endpoint
import datetime
import time
from utils import utils


class Mapping:
    def __init__(self, source: Endpoint, sinks: list[Endpoint]):
        self._source = source
        self._sinks = sinks

    def map(self):
        value = self._source.read_value()
        #if value is not None:
        for sink in self._sinks:
            sink.write_value(value)

class TriggeredMapping(Mapping):
    def map(self):
        self._source.set_trigger(self._sinks)

    def __repr__(self):
        return f"event_based_mapping: {self._source} -> {self._sinks}"

class MappingGroup:
    def __init__(self, name: str):
        self.name = name
        self._mappings: dict[int: list[Mapping]] = {}
        self._threads: dict[int: threading.Thread] = {}
        self._do_pull: dict[int: bool] = {}
        self._triggered_mappings: list[TriggeredMapping] = []

    def get_status(self):
        pulling = []
        not_pulling = []
        for pull_interval in self._mappings.keys():
            if self._do_pull[pull_interval]:
                pulling.append(pull_interval)
            else:
                not_pulling.append(pull_interval)
        return {"pulling": pulling, "not_pulling": not_pulling, "event": self._triggered_mappings}

    def add_triggered_mapping(self, mapping: TriggeredMapping):
        self._triggered_mappings.append(mapping)

    def add_triggered_mappings(self, mappings: list[TriggeredMapping]):
        for mapping in mappings:
            self.add_triggered_mapping(mapping)

    def add_mapping(self, mapping: Mapping, pull_interval: int):
        self.add_mapping_list([mapping], pull_interval)

    def add_mapping_list(self, mapping_list: list[Mapping], pull_interval: int):
        if pull_interval not in self._mappings.keys():
            self._mappings[pull_interval] = []
            self._do_pull[pull_interval] = False
        for mapping in mapping_list:
            self._mappings[pull_interval].append(mapping)

    def start_mappings(self):
        for mapping in self._triggered_mappings:
            mapping.map()
        for pull_interval in self._mappings.keys():
            self.start_mapping(pull_interval)

    def stop_mappings(self):
        for pull_interval in self._do_pull.keys():
            self._do_pull[pull_interval] = False

    def start_mapping(self, pull_interval: int):
        if pull_interval not in self._mappings.keys():
            return f"Group {self.name}: Unknown subgroup {pull_interval}"

        if pull_interval in self._threads.keys() and self._threads[pull_interval].is_alive():
            status = f"Group {self.name}({pull_interval}) already pulling"
            return status
        else:
            args = [pull_interval]
            self._do_pull[pull_interval] = True
            self._threads[pull_interval] = threading.Thread(target=self._map, args=args)
            self._threads[pull_interval].start()
            status = f"Starting to map group '{self.name}' with an interval of {pull_interval} s"
            return status

    def stop_mapping(self, pull_interval: int):
        if pull_interval in self._do_pull.keys():
            if not self._do_pull[pull_interval]:
                return f"Group {self.name} subgroup {pull_interval} not pulling currently"
            self._do_pull[pull_interval] = False
            return f"Stopped group {self.name} subgroup {pull_interval}"
        return f"Group {self.name} has no subgroup {pull_interval}"

    def change_interval(self, old_interval: int, new_interval: int, auto_start: bool):
        if old_interval not in self._mappings.keys():
            return f"Group {self.name} has not subgroup {old_interval} to change"

        if new_interval in self._mappings.keys():
            self.stop_mapping(new_interval)
        else:
            self._mappings[new_interval] = []
        self.stop_mapping(old_interval)
        self.add_mapping_list(self._mappings[old_interval], new_interval)
        self._mappings.pop(old_interval)

        self._do_pull[new_interval] = False
        if auto_start:
            self.start_mapping(new_interval)
            return f"Group {self.name}: changed subgroup {old_interval} to {new_interval} and started mapping"
        return f"Group {self.name}: changed subgroup {old_interval} to {new_interval}"

    def _map(self, pull_interval: int):
        mapping_list = self._mappings[pull_interval]
        while self._do_pull[pull_interval]:
            t1 = datetime.datetime.now()
            for mapping in mapping_list:
                mapping.map()
                if not self._do_pull[pull_interval]:
                    break
            if not self._do_pull[pull_interval]:
                break
            t2 = datetime.datetime.now()
            pull_duration = (t2 - t1).total_seconds()
            utils.log(f"{self.name}({pull_interval}): Pull completed. Took {str(pull_duration)} s")
            if pull_duration < pull_interval:
                rest_time = int(pull_interval - pull_duration)
                rested_sec = 0
                for s in range(rest_time):
                    rested_sec += 1
                    time.sleep(1)
                    if not self._do_pull[pull_interval]:
                        break
        utils.log(f"{self.name}({pull_interval}): Stopped pulling")



class Mapper:
    def __init__(self):
        self._groups: dict[str: MappingGroup] = {}

    #def add_mapping_group(self, mapping_group: MappingGroup):
    #    self._mappings[mapping_group.name] = mapping_group

    def add_triggered_mapping(self, source: Endpoint, sinks: list[Endpoint], group: str = None):
        """group can be a bacnet device id for example"""
        if group is None:
            group = "unmonitored"
        if group not in self._groups.keys():
            self._groups[group] = MappingGroup(group)

        self._groups[group].add_triggered_mapping(TriggeredMapping(source, sinks))

    def add_mapping(self, source: Endpoint, sinks: list[Endpoint], pull_interval: int, group: str = None):
        """group can be a bacnet device id for example"""
        if group is None:
            group = "unmonitored"
        if group not in self._groups.keys():
            self._groups[group] = MappingGroup(group)
        self._groups[group].add_mapping(Mapping(source, sinks), pull_interval)


    def start_mapping(self):
        for mapping_group in self._groups.values():
            mapping_group.start_mappings()
        return "Started mappings"

    def stop_mapping(self):
        for group_name in self._groups.keys():
            self.stop_group(group_name)
        return "Stopped mappings"

    def start_group(self, group_name: str) -> str:
        if group_name not in self._groups.keys():
            return f"Unknown group {group_name}"
        self._groups[group_name].start_mappings()
        return f"Group '{group_name}' started"

    def stop_group(self, group_name: str):
        if group_name in self._groups.keys():
            self._groups[group_name].stop_mappings()
            return f"Stopped group '{group_name}'"
        return f"Unknown group '{group_name}'"

    def start_subgroup(self, group_name: str, interval: int | str):
        if isinstance(interval, str):
            try:
                interval = int(interval)
            except ValueError:
                return f"Invalid interval '{interval}' provided"
        if group_name not in self._groups.keys():
            return f"Unknown group {group_name}"
        return self._groups[group_name].start_mapping(interval)

    def stop_subgroup(self, group_name: str, interval: int | str):
        if isinstance(interval, str):
            try:
                interval = int(interval)
            except ValueError:
                return f"Invalid interval '{interval}' provided"
        if group_name not in self._groups.keys():
            return f"Unknown group {group_name}"
        return self._groups[group_name].stop_mapping(interval)

    def change_interval(self, group_name: str, old_interval: int | str, new_interval: int | str, auto_start: bool = False):
        if group_name not in self._groups.keys():
            return f"Unknown group {group_name}"

        if isinstance(old_interval, str) or isinstance(new_interval, str):
            try:
                old_interval = int(old_interval)
                new_interval = int(new_interval)
            except ValueError:
                return f"Invalid intervals '{old_interval}' / '{new_interval}' provided"
        return self._groups[group_name].change_interval(old_interval, new_interval, auto_start)

    def get_status(self):
        status = {}
        for mapping_group in self._groups.values():
            status[mapping_group.name] = mapping_group.get_status()
        return status