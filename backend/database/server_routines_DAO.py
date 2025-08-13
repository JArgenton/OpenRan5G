from .dao import DAO

class Server_Routines(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "Server_Routines"

    def create_table(self) -> None:
        self._cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            SERVER_ROUTINE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TIME TEXT NOT NULL,
            ACTIVE BOOL NOT NULL
        )
        """)
        self._conn.commit()


    def get_latest_id(self):
        sql = f"SELECT MAX(SERVER_ROUTINE_ID) FROM {self.table_name}"
        self._cur.execute(sql)
        result = self._cur.fetchone()
        return result[0] if result else None  



