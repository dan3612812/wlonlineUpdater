from glob import glob
from .conf import config, dateFormat, DateFormat
from os.path import normpath, join, getmtime
from datetime import datetime, date


def init() -> str:
    result :DateFormat = "2005-11-18"
    targetFolderPattern = normpath(join(config["targetFolder"], "**/*"))
    allFilesPath = glob(targetFolderPattern)

    for filePath in allFilesPath:
        # 排除/user檔案
        excludePath = normpath(join(config["targetFolder"], "./user"))
        if excludePath in filePath:
            continue

        fileTime: DateFormat = (datetime.fromtimestamp(
            getmtime(filePath))).strftime(dateFormat)
        if result < fileTime:
            result = fileTime

    return result
