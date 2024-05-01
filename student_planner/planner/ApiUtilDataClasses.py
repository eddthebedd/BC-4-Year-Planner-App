from dataclasses import dataclass
from datetime import datetime 
from typing import List

@dataclass
class MetaInfo:
    versionInd: str
    createTime: datetime
    createId: str
    updateTime: datetime
    updateId: str

@dataclass
class AtrributeInfo:
    id: str
    key: str
    value: str

@dataclass
class RichTextInfo:
    plain: str
    formatted: str

@dataclass
class TimeAmountInfo:
    atpDurationTypeKey: str
    timeQuantity: int

@dataclass
class BaseInfo:
    # typeKey: str
    # stateKey: str
    meta: MetaInfo
    attributes: List[AtrributeInfo]

@dataclass
class BaseIdDescr:
    id: str
    name: str
    descr: RichTextInfo

@dataclass
class BaseKeyDescr:
    key: str
    name: str
    descr: RichTextInfo

@dataclass
class OrgCodeInfo(BaseInfo):
    id: str
    value: str
    descr: RichTextInfo
