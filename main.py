import os
import re
from typing import Union


class ObjcProperty:
    """
    objc 类文本解析的属性对象
    """

    def __init__(self, name: str, attributes: str):
        words = name.rsplit(maxsplit=1)
        self._name = words[1].strip()
        self._type = words[0].strip()
        self._attributes = attributes
        self.array_type = ''

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def is_assign(self) -> bool:
        return 'assign' in self._attributes

    @property
    def is_enum(self) -> bool:
        return '*' not in self.type and 'NS' in self.type

    @property
    def is_nsnumber(self) -> bool:
        return 'NSNumber' in self.type

    @property
    def is_nsarray(self) -> bool:
        return 'NSArray' in self.type

    @property
    def is_nsdictionary(self) -> bool:
        return 'NSDictionary' in self.type

    @property
    def is_nsdictionary_in_nsarray(self) -> bool:
        return self.is_nsarray and self.is_nsdictionary

    def __str__(self):
        return f'<ObjcProperty: name: {self.name}, type: {self.type}, attributes: {self._attributes}>'


class ObjcClass:

    def __init__(self, path: str, name: str, superclass_name: str):
        self._file_path = path
        self._name = name
        self._superclass_name = superclass_name
        self._properties = []

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def name(self) -> str:
        return self._name

    @property
    def superclass_name(self) -> str:
        return self._superclass_name

    @property
    def properties(self) -> list[ObjcProperty]:
        return self._properties

    def add_property(self, p: ObjcProperty):
        """
        :param p: 属性
        """
        self._properties.append(p)

    def __str__(self):
        return f'<ObjcClass: name: {self.name}, superclass: {self.superclass_name}, properties: {self.properties}>'


class ObjcEnum:
    pass


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


def find_header_files(dir_path: str) -> [str]:
    """
    查找目录内的所有头文件
    :param dir_path: dir_path (str): 目录路径
    :return: 返回找到的所有头文件路径数组
    """
    header_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".h"):
                header_files.append(os.path.join(root, file))
    return header_files


def is_class_in_file(file_path: str, class_name: str) -> bool:
    """
    头文件中是否存在指定类的声明
    :param file_path: 头文件路径
    :param class_name: 类名
    :return: True or False
    """
    with open(file_path, 'r') as file:
        content = file.read()
        pattern = r"@interface\s+(\w+)\s*:\s*(\w+)(.*?)@end"
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            if class_name in match[0]:
                return True
    return False


def find_class_file_path(dir_path: str, class_name: str) -> Union[str, None]:
    """
    查找类声明的头文件
    :param class_name: 类名
    :param dir_path:
    :return: header file path
    """
    all_header_paths = find_header_files(dir_path)
    for h_path in all_header_paths:
        if is_class_in_file(h_path, class_name):
            return h_path
    return None


def extract_objc_classes(file_path: str) -> [ObjcClass]:
    """
    从给定的头文件路径解析类并返回 [ObjcClass] 类数组

    :param file_path: 头文件路径
    :return: 返回 [ObjcClass]
    """
    objc_classes = []

    with open(file_path, 'r') as file:
        content = file.read()
        pattern = r"@interface\s+(\w+)\s*:\s*(\w+)(.*?)@end"
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            class_name = match[0]
            super_class_name = match[1]
            properties_section = match[2]

            # Regular expression pattern to extract properties
            properties_pattern = r"@property\s*\((.*?)\)\s*(.*?)\s*;\s*"

            # Matching the properties
            properties = re.findall(properties_pattern, properties_section)

            objc_cls = ObjcClass(file_path, class_name, super_class_name)
            for property_info in properties:
                attributes = property_info[0]
                property_name = property_info[1]
                p = ObjcProperty(property_name.strip(), attributes)
                objc_cls.add_property(p)
            objc_classes.append(objc_cls)
    return objc_classes


sources_dir_path = '/Users/d/develop/HelloOCRuntime'


def main():
    header_files_list = find_header_files(sources_dir_path)
    print(f"sources_dir_path: {sources_dir_path}")
    classes = []
    for header_file_path in header_files_list:
        print(f'header_file_path: {header_file_path}')
        classes.extend(extract_objc_classes(header_file_path))
    for c in classes:
        print(c)

if __name__ == '__main__':
    main()