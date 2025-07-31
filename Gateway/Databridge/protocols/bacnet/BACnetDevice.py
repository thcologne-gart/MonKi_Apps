class BacnetDevice:
    def __init__(self, device_id: int, ip_address: str, device_name: str):
        self.device_id = device_id
        self.ip_address = ip_address
        self.device_name = device_name

