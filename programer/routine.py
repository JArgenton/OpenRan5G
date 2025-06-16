from abc import ABC, abstractmethod
from network_test import Test
import os
import json

class Routine:
    def __init__(self):
        self._name 
        self._id
        self._tests: list[Test] = []

    @property.setter
    def name(self, name):
        self.name = name

    @property.getter
    def name(self):
        return self._name

    @property.getter
    def id(self):
        return self._id

    @property.getter
    def routine(self):
        return self._tests
    
    def save_routine(self):
        os.makedirs("programer/routines", exist_ok=True)
        ids = [test.id for test in self.routine]
        path = os.path.join("programer/routines", f"{self.name}")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ids, f, indent=4)
                

            subprocess.run(command, capture_output=True, text=True)