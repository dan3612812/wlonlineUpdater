from os.path import normpath, join, getmtime
from datetime import datetime
from glob import glob
from typing import TypedDict, List
from .conf import config, dateFormat, DateFormat


class myFiles(TypedDict):
    path: str
    modifyTime: DateFormat


def init(datumTime: DateFormat) -> List[myFiles]:
    result: List[myFiles] = []
    targetFolderPattern = normpath(join(config["targetFolder"], "**/*"))
    allFilesPath = glob(targetFolderPattern)

    for filePath in allFilesPath:
        # 排除/user檔案
        excludePath = normpath(join(config["targetFolder"], "./user"))
        if excludePath in filePath:
            continue

        fileTime: DateFormat = datetime.fromtimestamp(
            getmtime(filePath)).strftime(dateFormat)
        if fileTime > datumTime:
            result.append({"path": filePath, "modifyTime": fileTime})

    return result
