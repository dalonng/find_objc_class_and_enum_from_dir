import os
import re
from typing import Union
from objc_types import ObjcClass, ObjcProperty, ObjcEnum

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


def extract_objc_classes_and_enum(file_path: str) -> ([ObjcClass], [ObjcEnum]):
    """
    从给定的头文件路径解析类并返回 [ObjcClass] 类数组

    :param file_path: 头文件路径
    :return: 返回 [ObjcClass]
    """
    objc_classes = []
    objc_enums = []
    with open(file_path, 'r') as file:
        content = file.read()

        clss = _parse_interface(file_path, content)
        if clss:
            objc_classes.extend(clss)

        enums = _parse_ns_enum(file_path, content)
        if enums:
            objc_enums.extend(enums)

    return (objc_classes, objc_enums)

def _parse_interface(file_path: str, content: str) -> Union[list[ObjcClass], None]:
    """
    解析 objc class
    :param content: 文件内容
    :return: 解析到的 ObjcClass ｜ None
    """
    pattern = r"@interface\s+(\w+)\s*:\s*(\w+)(.*?)@end"
    matches = re.findall(pattern, content, re.DOTALL)
    if not matches:
        return None

    objc_classes = []
    for match in matches:
        class_name = match[0]
        super_class_name = match[1]
        properties_section = match[2]

        # Regular expression pattern to extract properties
        properties_pattern = r"@property\s*\((.*?)\)\s*(.*?)\s*;\s*"

        # Matching the properties
        properties = re.findall(properties_pattern, properties_section)

        # print(f'class_name: {class_name}, super_class_name: {super_class_name}')
        objc_cls = ObjcClass(file_path, class_name, super_class_name)
        for property_info in properties:
            attributes = property_info[0]
            property_name = property_info[1]
            # print(f'property_name: {property_name}, attributes: {attributes}')
            p = ObjcProperty(property_name.strip(), attributes)
            objc_cls.add_property(p)
        objc_classes.append(objc_cls)
        return objc_classes
    return objc_classes


def _parse_ns_enum(file_path: str, content: str) -> Union[list[ObjcEnum], None]:
    """
    解析 objc enum
    :param content: 文件内容
    :return: 解析到的 [ObjcEnum] ｜ None
    """
    # Regular expression pattern to match NS_ENUM definitions
    pattern = r'\bNS_ENUM\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*{\s*([^}]*)\s*}\s*;'

    # Find all occurrences of NS_ENUM in the header_string
    matches = re.findall(pattern, content)
    if not matches:
        return None

    enum_definitions = []
    for match in matches:
        enum_name = match[0]
        enum_type = match[1]
        enum_values = [value.strip() for value in match[2].split(',')]        
        # print(f'enum_name: {enum_name}, enum_type: {enum_type}, value: {enum_values}')
        enum_definitions.append(ObjcEnum(file_path, enum_name, enum_type, enum_values))

    return enum_definitions