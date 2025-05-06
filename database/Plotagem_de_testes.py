from dao import DAO

class PlotagemDeTestesDAO(DAO):
    @property
    def table_name(self) -> str:
        return "plotagem_de_testes"

    def create_table(self) -> None:
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                PLOT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TEST_ID TEXT,
                IMAGE_PATH TEXT,
                CREATED_AT TEXT
            )
        """)
        self._conn.commit()