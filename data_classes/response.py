from dataclasses import dataclass
from typing import List


@dataclass
class fileSpec:
    id: str
    title: str
    type: str
    permission: int
    collapsed: bool
    children: List[str]
    
    def __getitem__(self, item):
        return getattr(self, item)



@dataclass
class Response:
    _code: str
    _msg: str
    root_file_id: str
    files: fileSpec
    
    def __getitem__(self, item):
        return getattr(self, item)