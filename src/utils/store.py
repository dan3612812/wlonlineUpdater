import json
from .conf import config, programPath, DateFormat
from os.path import normpath
from typing import TypedDict, List


class SelfStore(TypedDict):
    updateTimes: List[DateFormat]
    # "2022-11-17"
    ftpTime: DateFormat


absFileName = normpath(programPath+'/'+config["selfFile"])


def get() -> SelfStore | None:
    try:
        with open(absFileName, 'r') as f:
            data = json.load(f)
    except:
        # 默認值,ftp檔案只下載到該時間
        set({"ftpTime": "2022-11-17"})
        return None
    return data


def set(data: SelfStore) -> None:
    with open(absFileName, 'w')as f:
        f.write(json.dumps(data))
