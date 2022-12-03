import os
from os.path import normpath
from datetime import datetime
from .conf import programPath, FullDatetimeFormat, fullDatetimeFormat
from typing import List
# from .store import get as getStore
from .pyFtpClient import PyFTPclient, FileInfo

serverIP = "210.242.171.96"
downloadFolderPath = normpath(programPath+"/ftp")


class SelfFile:
    filename: str
    size: int
    modify: FullDatetimeFormat


def main():
    # 初始化同步的資料夾
    initFolder()
    # 初始化ftp物件
    ftp = PyFTPclient(serverIP)
    # 取得遠端資料目錄
    # print(ftp.dir())

    filesObj = getDiffFromTwoFolders(getLocalDir(), ftp.dir())
    # 如果要移除不存在遠端的本地檔案請打開下面的code
    # for filename in filesObj["deleteFiles"]:
    #     os.remove(normpath(downloadFolderPath+"/"+filename))
    for filename in filesObj["downloadFiles"]:
        ftp.downloadFile(filename, normpath(downloadFolderPath+"/"+filename))

    # judgmentTime = getStore()["ftpTime"]
    # downloadSize = 0
    # for info in fileInfos:
    #     if info["modify"].strftime(dateFormat) > judgmentTime:
    #         downloadSize += info["size"]
    #         downloadFile(ftp, info["filename"])
    # print("download %d files used storage %f MB",
    #       len(fileInfos), downloadSize/8/1024/1024)


def initFolder():
    path = downloadFolderPath
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)


def getLocalDir():
    # os.path.getmtime
    # os.listdir
    # os.path.getsize

    result: list[SelfFile] = []
    listdir = os.listdir(downloadFolderPath)
    for file in listdir:
        filePath = normpath(downloadFolderPath+"/"+file)
        result.append(
            {
                "filename": file,
                "size": os.path.getsize(filePath),
                "modify": datetime.fromtimestamp(os.path.getmtime(filePath)).strftime(fullDatetimeFormat)
            }
        )
    return result


def getDiffFromTwoFolders(localDir: List[SelfFile], remoteDir: List[FileInfo]):
    # 與本地的比較 同檔名 檔案大小是否相等 修改日期是否相等
    # 遠端比本地多的檔案
    # local dir
    downloadFiles: list[str] = []
    localSameFiles: list[int] = []
    remoteSameFiles: list[int] = []
    for localIndex, localFile in enumerate(localDir):
        for remoteIndex, remoteFile in enumerate(remoteDir):
            if localFile["filename"] == remoteFile["filename"]:
                localSameFiles.append(localIndex)
                remoteSameFiles.append(remoteIndex)
                # size就是不同 或是 本地的檔案時間比遠端的還舊 都需要重新下載
                if localFile["size"] != remoteFile["size"] or localFile["modify"] < remoteFile["modify"]:
                    downloadFiles.append(localFile["filename"])

    remoteDirSumSame: List[FileInfo] = []
    localDirSumSame: List[SelfFile] = []
    for i, v in enumerate(remoteDir):
        if not i in remoteSameFiles:
            remoteDirSumSame.append(v)
    for i, v in enumerate(localDir):
        if not i in localSameFiles:
            localDirSumSame.append(v)

    for remoteRemainFile in remoteDirSumSame:
        downloadFiles.append(remoteRemainFile["filename"])

    deleteFiles: list[str] = []
    for localFile in localDirSumSame:
        deleteFiles.append(localFile["filename"])
    return {
        "deleteFiles": deleteFiles,
        "downloadFiles": downloadFiles
    }
