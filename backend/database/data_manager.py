import sqlite3

class Database_Manager():
    _instance = None 
    def __init__(self):
        self.connection = None
        self.cursor = None

    @staticmethod
    def get_object():
        if Database_Manager._instance is None:
            Database_Manager._instance = Database_Manager()
        """define o cursor e abre connexao"""
        if(Database_Manager._instance.connection is None):
            Database_Manager._instance.connection = sqlite3.connect("backend/database/results.db", check_same_thread=False)
            Database_Manager._instance.cursor = Database_Manager._instance.connection.cursor()
        return Database_Manager._instance
        
    def commit(self):
        """Confirma transações pendentes."""
        if self._connection:
            self._connection.commit()

    def close(self):
        """Fecha cursor e conexão, liberando recursos."""
        if self._connection:
            if(self.cursor):
                self._cursor.close() # type: ignore
            self._connection.close()
            self._connection = None
            self._cursor = None
