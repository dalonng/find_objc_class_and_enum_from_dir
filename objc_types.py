class ObjcProperty:
    """
    objc 类文本解析的属性对象
    """

    def __init__(self, name: str, attributes: str):
        words = name.rsplit(maxsplit=1)
        if len(words) > 1:
            self._name = words[1].strip() 
            self._type = words[0].strip()
        else:
            self._name = words[0].strip
            self._type = ''
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

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'attributes': self._attributes
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