from dao import DAO

class TestesDeRedeDAO(DAO):
    @property
    def table_name(self) -> str:
        return "testes_de_rede"

    def create_table(self) -> None:
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                TEST_ID TEXT PRIMARY KEY,
                TIMESTAMP TEXT,
                LATENCIA REAL,
                THROUGHPUT REAL
            )
        """)
        self._conn.commit()
