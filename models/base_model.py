#!/usr/bin/python3
"""
BaseModel class module.
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    BaseModel class for other classes to inherit.
    """

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    if isinstance(value, str):
                        setattr(self, key,
                                datetime.strptime(value,
                                                  '%Y-%m-%dT%H:%M:%S.%f'
                                                  ))
                    else:
                        setattr(self, key, value)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def save(self):
        """Update the updated_at attribute and save to storage."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """Return a string representation of the instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    @classmethod
    def all(cls):
        """Return a dictionary of all instances of the class."""
        from models import storage
        return storage.all(cls)
