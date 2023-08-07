import json
from typing import Union 
from objc_types import ObjcClass, ObjcProperty, ObjcEnum
from utils import extract_objc_classes_and_enum, find_header_files

class ObjcCache:

    def __init__(self):
        self.class_cache = {}
        self.enum_cache = {}

    def get_class(self, key: str) -> Union[ObjcClass, None]:
        if key in self.class_cache:
            return self.class_cache[key]
        return None

    def set_class(self, key: str, value: ObjcClass):
        self.class_cache[key] = value

    def get_enum(self, key: str) -> Union[ObjcEnum, None]:
        if key in self.enum_cache:
            return self.enum_cache[key]
        return None

    def set_enum(self, key: str, value: ObjcEnum):
        self.enum_cache[key] = value
