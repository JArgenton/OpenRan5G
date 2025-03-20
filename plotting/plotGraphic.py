import matplotlib.pyplot as plt
from database.teste_bd import Database as db

class Plotting: 
       def __innit__(self):
            self.database = db.get_object() 
       
    