from zipfile import ZipFile
from typing import List
from datetime import datetime
from os.path import normpath
from .getProgramPath import programPath
from .conf import dateFormat


def init(filePaths: List[str]) -> str:
    # 切掉倒數3個元素 變成專案目錄
    date = datetime.today().strftime(dateFormat)
    absFileName = normpath(programPath+"/zip/"+date+".zip")

    with ZipFile(absFileName, mode='w') as zf:
        for nowFilePath in filePaths:
            zf.write(nowFilePath)

    return absFileName
