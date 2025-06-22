from .dao import DAO

class _Relacionamento_R2T(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()
    @property
    def table_name(self) -> str:
        return "relacionamentos_R2T"

    def create_table(self) -> None:

        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID),
                FOREIGN KEY (ROUTINE_ID) REFERENCES rotinas(ROUTINE_ID),
            )
        """)
        self._conn.commit()