#!/usr/bin/python3
"""file contains the base class that defines all the common attributes
   and methods for other classes"""
import uuid
from datetime import datetime
from models import storage


class BaseModel():
    """the base class for all other classes"""
    def __init__(self, *args, **kwargs):
        """instantiation of object directly or from a dictionary
           representation given through argument kwargs

           Args:
               *args (any): Unused.
               **kwargs (dict): Key/value of attributes.
        """
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    datetime_format = datetime.strptime(value,
                                                        "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, datetime_format)
                else:
                    setattr(self, key, value)

    def save(self):
        """updates the public instance attribute
           updated_at with the current datetime
        """
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all
           keys/values of __dict__ of the instance
        """
        dict_cpy = self.__dict__.copy()
        dict_cpy["created_at"] = self.created_at.isoformat()
        dict_cpy["updated_at"] = self.updated_at.isoformat()
        dict_cpy["__class__"] = self.__class__.__name__
        return dict_cpy

    def __str__(self):
        """print the class name, id and dictionary"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
