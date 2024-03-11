#!/usr/bin/python3
"""
Module for the command interpreter.
"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review,
}


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class.
    """
    prompt = "(hbnb) "

    valid_classes = ["BaseModel", "User",
                     "State", "City",
                     "Amenity", "Place",
                     "Review"]

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        print()
        return True

    def do_create(self, arg):
        """
        Creates a new instance of a specified class,
        saves it (to the JSON file), and prints the id.
        Usage: create <class name>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation
        of an instance based on the class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            all_objects = storage.all()
            instance = all_objects.get(key, None)
            if instance:
                print(instance)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id (saves the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            all_objects = storage.all()
            instance = all_objects.get(key, None)
            if instance:
                del all_objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation
        of all instances based or not on the class name.
        Usage: all [<class name>]
        """
        args = arg.split()
        all_objects = storage.all()
        if not args:
            print(all_objects)
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            filtered_objects = {k: v for k,
                                v in all_objects.items() if args[0] in k}
            print(filtered_objects)

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating an attribute.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            all_objects = storage.all()
            instance = all_objects.get(key, None)
            if instance:
                attr_name = args[2]
                attr_value = args[3].strip('"')
                setattr(instance, attr_name, attr_value)
                storage.save()
            else:
                print("** no instance found **")

    def do_count(self, arg):
        """
        Retrieves the number of instances of a class.
        Usage: <class name>.count()
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            instances = storage.all(args[0])
            print(len(instances))

    def do_show_instance(self, arg):
        """
        Retrieves an instance based on its ID: <class name>.show(<id>).
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            class_name = args[0]
            instance_id = args[1]

            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                key = "{}.{}".format(class_name, instance_id)
                all_objects = storage.all()
                instance = all_objects.get(key, None)
                if instance:
                    print(instance.__str__())
                else:
                    print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
