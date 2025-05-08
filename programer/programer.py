from configuration.config import Configuration
from database.data_manager import Database
from datetime import datetime
from routine import Routine

from typing import List, Tuple
from enum import Enum



class Programmer:

    def __init__(self):
        self.configuration = Configuration.getObject()
        self.routines: List[Tuple[Routine, datetime]] = []


    def insert_routine():
        """adiciona um objeto rotina, junto a um timestamp à lista de rotinas"""
        pass   

    def remove_routine():
         """procura a rotina por seu nome, e a remove"""

    def verify_tasks(self):
         for routine in self.routines:
              if()

    



if __name__ == '__main__':
        programer = Programmer()
        programer.create_routine()