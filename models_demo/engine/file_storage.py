#!/usr/bin/python3

import json
import os


class FileStorage:
    """A class that serialize and deserialize instances to a JSON file"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects"""
        return type(self).__objects

    def new(self, obj):
        """Sets new obj in __objects dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        type(self).__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            new_dict = {}
            for key, value in type(self).__objects.items():
                new_dict[key] = value.to_dict()
            json.dump(new_dict, file)

    def class_dict(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        class_dict = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "Amenity": Amenity,
            "City": City,
            "Review": Review,
            "State": State
            }
        return class_dict

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        if os.path.exists(self.__file_path) is True:
            try:
                with open(type(self).__file_path, "r", encoding='utf-8') as file:
                    new_obj = json.load(file)
                    for key, val in new_obj.items():
                        obj = self.class_dict()[val['__class__']](**val)
                        type(self).__objects[key] = obj
            except FileNotFoundError:
                return