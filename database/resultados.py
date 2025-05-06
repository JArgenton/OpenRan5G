from dao import DAO

class Resultados(DAO):
    @property
    def table_name(self) -> str:
        return "resultados"

    def create_table(self) -> None:
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                TEST_ID TEXT PRIMARY KEY,
                DURATION TEXT,
                PACKAGE_LOSS INTEGER,
                UTP BOOLEAN,
                TCP BOOLEAN,
                JITTER REAL
            )
        """)
        self._conn.commit()