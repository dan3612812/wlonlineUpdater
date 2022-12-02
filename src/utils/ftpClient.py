"""
BUG 
需要處理斷線問題
以及同步資料夾
"""
import os
from os.path import normpath
from datetime import datetime
from ftplib import FTP
from .conf import dateFormat, FullDatetimeFormat, programPath
from .store import get as getStore

downloadFolderPath = normpath(programPath+"/ftp")
"""
 FIXME  maybe use dict or others type
"""


class FileInfo:
    type: str
    size: int
    modify: FullDatetimeFormat
    perms: str
    filename: str


def main():
    initFolder()
    with FTP("210.242.171.96") as ftp:
        ftp.login()
        ls: list[str] = []
        ftp.retrlines("MLSD", ls.append)
        fileInfos: list[FileInfo] = []
        for line in ls:
            fileInfo: FileInfo = {
                "filename": line.split(";")[-1].replace(" ", "")
            }
            for st in line.split(";"):
                if "type=" in st:
                    fileInfo["type"] = st[5:]
                if "size=" in st:
                    fileInfo["size"] = int(st[5:])
                if "modify=" in st:
                    fileInfo["modify"] = parseToISO(st[7:])
                if "perms=" in st:
                    fileInfo["perms"] = st[6:]
            fileInfos.append(fileInfo)

        fileInfos.sort(key=lambda obj: obj["modify"].timestamp(), reverse=True)
        judgmentTime = getStore()["ftpTime"]
        downloadSize = 0
        for info in fileInfos:
            if info["modify"].strftime(dateFormat) > judgmentTime:
                downloadSize += info["size"]
                downloadFile(ftp, info["filename"])
        print("download %d files used storage %f MB",
              len(fileInfos), downloadSize/8/1024/1024)
    ftp.close()


def initFolder():
    path = downloadFolderPath
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)


def parseToISO(str: str) -> FullDatetimeFormat:
    year = str[:4:]
    mouth = str[4:6:]
    day = str[6:8:]
    hour = str[8:10:]
    minute = str[10:12:]
    second = str[12:14:]
    ms = str[15:]

    return datetime.fromisoformat("%s-%s-%sT%s:%s:%s.%s" % (year, mouth, day, hour, minute, second, ms))


def downloadFile(ftp: FTP, filename: str):

    localFilePath = normpath(downloadFolderPath+"/"+filename)
    with open(localFilePath, 'wb') as fp:
        ftp.retrbinary('RETR '+filename, fp.write)
