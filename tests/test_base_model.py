#!/usr/bin/python3
"""
Module containing unit tests for BaseModel class.
"""
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """
    def test_base_model(self):
        """
        Test the functionality of the BaseModel class.
        """
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        print(my_model)
        my_model.save()
        print(my_model)
        my_model_json = my_model.to_dict()
        print(my_model_json)
        print("JSON of my_model:")
        for key in my_model_json.keys():
            print("\t{}: ({}) - {}".format(
                key,
                type(my_model_json[key]),
                my_model_json[key]
            ))


if __name__ == "__main__":
    unittest.main()
