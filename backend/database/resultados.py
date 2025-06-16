from dao import DAO

class ResultadosDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "resultados"

    def create_table(self) -> None:
        """
        Cria 'resultados' com medições e resultados do teste.
        chave para testes de rede
        """
        #test_id tem q ser routine ID
        self._cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
        RESULT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TEST_ID INTEGER,  -- <== Adicionada aqui
        ROUTINE_ID TEXT NOT NULL,
        TIMESTAMP_RESULT TEXT NOT NULL,

        -- Resultados de Ping
        MIN_LATENCY REAL,
        AVG_LATENCY REAL,
        MAX_LATENCY REAL,
        LOST_PACKETS REAL,
        LOST_PERCENT REAL,

        -- Resultados de Iperf3
        BITS_PER_SECOND REAL,
        BYTES_TRANSFERRED REAL,
        JITTER REAL,
        RETRANSMITS REAL,

        FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID)
    )
""")

        self._conn.commit()

if __name__ == '__main__':
    database = ResultadosDAO()
    #testes_de_rede.create_table()

    data = {
        "ROUTINE_ID": "rotina_001",
        "TIMESTAMP_RESULT": "2025-06-16 14:00:00",

        # Resultados de Ping
        "MIN_LATENCY": 5.2,
        "AVG_LATENCY": 2.4,
        "MAX_LATENCY": 7.5,
        "LOST_PACKETS": 2,
        "LOST_PERCENT": 1.25,

        # Resultados de Iperf3
        "BITS_PER_SECOND": 85000000,
        "BYTES_TRANSFERRED": 10625000,
        "JITTER": 0.85,
        "RETRANSMITS": 4
    }
    database.insert(data)
    all = database.fetch_all()
    for a in all:
        print(a)