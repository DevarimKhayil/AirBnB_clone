#!/usr/bin/python3
import json
from datetime import datetime


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all instances,
        or all instances of a specified class.
        """
        if cls is None:
            return self.__objects
        else:
            return {k: v for k,
                    v in self.__objects.items()
                    if isinstance(v, cls)}

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        try:
            from models.base_model import BaseModel
            from models.user import User
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    cls_name, obj_id = key.split('.')
                    value['created_at'] = datetime.strptime(
                        value['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    value['updated_at'] = datetime.strptime(
                        value['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    cls = eval(cls_name)
                    obj = cls(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
        except JSONDecodeError as e:
            pass

    def to_dict(self):
        """Convert instances to dictionary format."""
        new_dict = {}
        for key, value in self.__objects.items():
            new_dict[key] = value.to_dict()
        return new_dict

    def delete(self):
        """Deserialize the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    del value['__class__']
                    self.__objects[key] = eval(class_name)(**value)
        except FileNotFoundError:
            pass
