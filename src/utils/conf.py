from dotenv import dotenv_values
from os.path import normpath
from datetime import datetime
from os.path import normpath

programPath = normpath("\\".join(__file__.split(
    "\\")[::-1][3::][::-1]))


class SelfConfig(object):
    targetFolder: str
    selfFile: str


class FullDatetimeFormat(str):
    def __init__(self) -> None:
        super().__init__()


class DateFormat(str):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def getFormat():
        return "%Y-%m-%d"


class TimeFormat(str):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def getFormat():
        return "%H:%M:%S.%f"


_config = dotenv_values(".env")
config: SelfConfig = {
    "targetFolder": normpath(_config.get("targetFolder")),
    "selfFile": _config.get("selfFile")
}


fullDatetimeFormat: FullDatetimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
dateFormat: DateFormat = fullDatetimeFormat.split("T")[0]
timeFormat: TimeFormat = fullDatetimeFormat.split("T")[1]
