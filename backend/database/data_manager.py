import sqlite3
from singleton import MetaSingleton
import json
class Database_Manager(metaclass=MetaSingleton): #metaclasses. EHHHHHHHHHHHH
    def __init__(self, db_path):
        self.connection = None
        self.cursor = None
        self.db_path = db_path

    def get_object():
        if Database_Manager._instance == None:
            Database_Manager._instance = Database_Manager()
        return Database_Manager._instance

    def connect(self):
        """define o cursor e abre connexao"""
        if(self.connection is None):
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            return self.connection, self.cursor
        
    def commit(self):
        """Confirma transações pendentes."""
        if self._connection:
            self._connection.commit()

    def close(self):
        """Fecha cursor e conexão, liberando recursos."""
        if self._connection:
            self._cursor.close()
            self._connection.close()
            self._connection = None
            self._cursor = None
