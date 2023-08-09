from typing import Union

class ObjcProperty:
    """
    objc 类文本解析的属性对象
    """

    def __init__(self, name: str, property_type: str, declaration_type: str):
        self._name = name.strip()
        self._type = property_type.strip()
        self._declaration_type = declaration_type
        self.array_type = ''

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def declaration_type(self) -> str:
        return self._declaration_type

    @property
    def is_assign(self) -> bool:
        return 'assign' in self._declaration_type

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

    @property
    def is_nsstring_in_nsarray(self) -> bool:
        return self.is_nsarray and 'NSString' in self._type

    @property
    def is_nsnumber_in_nsarray(self) -> bool:
        return self.is_nsarray and 'NSNumber' in self._type
    
    @property
    def is_ksproperty(self) -> bool:
        return 'KS' in self._type
    
    @property
    def swift_type(self) -> str:
        if self._type == 'float':
            return 'Float'
        if self._type.startswith('NSString'):
            return 'String'
        if self.is_nsnumber:
            return 'NSNumber'
        if self.is_nsarray and 'NSString' in self._type:
            return '[String]'
        if self.is_nsdictionary:
            return 'NSDictionary'
        if self.is_nsdictionary_in_nsarray:
            return 'NSDictionary'
        return self.type

    def __str__(self):
        return f'<ObjcProperty: name: {self.name}, type: {self.type}, attributes: {self._attributes}>'

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'declaration_type': self._declaration_type
        }
    
    
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

    def to_json(self) -> dict:
        return {
            'file_path': self.file_path,
            'name': self.name,
            'superclass_name': self.superclass_name,
            'properties': [p.to_json() for p in self.properties]
        }
    
    def property_by_name(self, name: str) -> Union[ObjcProperty, None]:
        for p in self.properties:
            if p.name == name:
                return p
        return None

class ObjcEnum:
    def __init__(self, file_path: str, name: str, enum_type: str, enums: [str]):
        self._file_path = file_path
        self._name = name
        self._enum_type = enum_type
        self._enums = enums

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def name(self) -> str:
        return self._name

    @property
    def enum_type(self) -> str:
        return self._enum_type

    @property
    def enums(self) -> [str]:
        return self._enums
    
    def to_json(self) -> dict:
        return {
            'file_path': self.file_path,
            'name': self.name,
            'enum_type': self.enum_type,
            'enums': self.enums
        }