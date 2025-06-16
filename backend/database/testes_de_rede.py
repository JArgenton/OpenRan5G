from .dao import DAO

class TestesDeRedeDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "testes_de_rede"

    def create_table(self) -> None:
        """
        Cria testes_de_rede com  parâmetros de configuração do teste.
        """
        self._cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {self.table_name} (
        TEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TEST_NAME TEXT NOT NULL,
        SERVER TEXT NOT NULL,
        PROTOCOL TEXT NOT NULL,
        DURATION_SECONDS REAL,
        PACKET_SIZE INTEGER,
        PACKET_COUNT INTEGER,
        IS_PING BOOLEAN NOT NULL,
        IS_IPERF BOOLEAN NOT NULL
    )
        """)

        self._conn.commit()


if __name__ == '__main__':
    testes_de_rede = TestesDeRedeDAO()
    #testes_de_rede.create_table()

    dados_teste = {
        "TEST_NAME": "Teste Banda TCP",
        "SERVER": "10.0.0.5",
        "PROTOCOL": "TCP",

        "PACKET_SIZE": 128,
        "PACKET_COUNT": 150,
        "IS_PING": False,
        "IS_IPERF": True
    }
    all = testes_de_rede.fetch_all()
    for a in all:
        print(a)
