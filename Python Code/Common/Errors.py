class WrongDeviceError(Exception):
    """Raised when the wrong port is selected, but the port exists, it's just not the Arduino temp control"""
    pass