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
        PROTOCOL TEXT,
        DURATION_SECONDS REAL,
        PACKET_SIZE INTEGER,
        PACKET_COUNT INTEGER
    )
        """)

        self._conn.commit()

    def get_latest_id(self):
        sql = f"SELECT MAX(TEST_ID) FROM {self.table_name}"
        self._cur.execute(sql)
        result = self._cur.fetchone()
        return result[0] if result else None  


if __name__ == '__main__':
    testes_de_rede = TestesDeRedeDAO()
    #testes_de_rede.create_table()

    dados_teste = {
        "PROTOCOL": "TCP",
        "PACKET_SIZE": 128,
        "PACKET_COUNT": 150,
    }
    testes_de_rede.insert(dados_teste)
    all = testes_de_rede.fetch_all()
    for a in all:
        print(f"{a} -> {testes_de_rede._cur.lastrowid}")

    #(ip, duration, packet_size, packet_count)
