"""Mock data for this exercise."""
import json
from random import random

NAME_PREFIX = ('Brand new', 'Second hand', 'Almost new', 'High quality',
               'Cheap', 'Elegant', 'Funny', 'Exceptional')

NAME_MAIN = ('Monitor', 'Laptop', 'Tablet', 'Smartphone', 'Headphones',
             'Keyboard', 'Mouse', 'Router')


def rand(options):
    """Pick an item randomly."""
    index = int(random() * len(options))
    return options[index]


def composed_name(prefix=NAME_PREFIX, suffix=NAME_MAIN):
    """Return a random name."""
    return rand(prefix).capitalize() + ' ' + rand(suffix).lower()


def create(amount=100):
    """Create mock data."""
    data = []
    while len(data) < amount:
        name = composed_name()
        data.append(name)
    return data


def save(data=None, filename="warehouse"):
    """Save the mocked data into a json file."""
    if data:
        with open(f"initial/{filename}.json", "w") as file:
            file.write(json.dumps(data))

        with open(f"solution/{filename}.json", "w") as file:
            file.write(json.dumps(data))


def create_and_save(amount=100, filename="warehouse"):
    """Save a mock sample as a json file."""
    data = create(amount)
    save(data, filename)


# print(Counter(data))
confirm = input("This will replace the data in the exercise."
                " Are you sure you want to proceed?(y/n) ")

if confirm.lower() == "y":
    create_and_save(filename="warehouse1")
    create_and_save(filename="warehouse2")
    print("The dataset has been replaced with new random mock data.")
