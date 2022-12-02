from utils.findNewFiles import init as findNewFiles
from utils.zipFile import init as zipFile
from utils.getLastTime import init as getLastTime
from utils.store import set, get
from typing import List


def main():
    # 如果找不到lastTime 代表還未知道資料夾內最新的時間需要取得由
    if (get() == None):
        print("Never run , find the last time with all files")
        set({"updateTimes": [getLastTime()]})
    # 如果存在代表已執行過一次
    # 只需要找出比上次的時間還要新
    datumTime = get()["updateTimes"][-1]
    theNewFilenames: List[str] = []
    maxTime = ""

    print("compare file modify time")
    findFiles = findNewFiles(datumTime)
    if (len(findFiles) == 0):
        print("It's don't have more news file")
        return
    else:
        print("It's have %d new files", len(findFiles))
    for file in findFiles:
        print(file)
        if maxTime < file["modifyTime"]:
            maxTime = file["modifyTime"]
        theNewFilenames.append(file["path"])
    # 再加入壓縮檔
    print("zip this files")
    print("the zip file path:", zipFile(theNewFilenames))
    # 更新data.json資料
    data = get()
    data["updateTimes"].append(maxTime)
    set(data)
    print("record update time")
    print("done!")

if __name__ == "__main__":
    main()
