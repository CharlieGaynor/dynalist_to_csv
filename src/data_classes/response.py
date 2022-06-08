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


@dataclass
class Response:
    _code: str
    _msg: str
    root_file_id: str
    files: fileSpec
