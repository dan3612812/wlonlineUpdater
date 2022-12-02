import json
from .conf import config
from .getProgramPath import programPath
from os.path import normpath
from typing import TypedDict, List


class SelfStore(TypedDict):
    updateTimes: List[str]


absFileName = normpath(programPath+'/'+config["selfFile"])


def get() -> SelfStore | None:
    try:
        with open(absFileName, 'r') as f:
            data = json.load(f)
    except:
        return None
    return data


def set(data: SelfStore) -> None:
    with open(absFileName, 'w')as f:
        f.write(json.dumps(data))
