from .dao import DAO

class ResultadosDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "resultados"
    
    def get_results_params(self, where: str = "", select: str = ""):
        sl = "*"
        if select != "":
            sl = select
        sql = f"SELECT {sl} FROM resultados JOIN testes_de_rede USING(TEST_ID)"
        if where != "":
            sql += f' {where}'
        print(sql)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def create_table(self) -> None:
        """
        Cria 'resultados' com medições e resultados do teste.
        chave para testes de rede
        """
        self._cur.execute(f"""   
        CREATE TABLE IF NOT EXISTS {self.table_name} (
        RESULT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ROUTINE_ID INTEGER,
        TEST_ID INTEGER,
        TIMESTAMP_RESULT TEXT NOT NULL,
        SERVER TEXT NOT NULL,

        -- Resultados de Ping
        MIN_LATENCY REAL,
        AVG_LATENCY REAL,
        MAX_LATENCY REAL,
        LOST_PACKETS REAL,
        LOST_PERCENT REAL,

        -- Resultados de Iperf3
        BITS_PER_SECOND REAL,
        BYTES_TRANSFERED REAL,
        JITTER REAL,
        RETRANSMITS REAL,

        FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID)
    )
""")

        self._conn.commit()