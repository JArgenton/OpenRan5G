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
    
    def get_or_create_test_id(self, dados_teste: dict) -> int:
        """
        Retorna o TEST_ID se já existir um teste com os mesmos parâmetros.
        Caso contrário, insere e retorna o novo ID.
        """

        sql = f"""
            SELECT TEST_ID FROM {self.table_name}
            WHERE PROTOCOL = ?
            AND DURATION_SECONDS = ?
            AND PACKET_SIZE = ?
            AND PACKET_COUNT = ?
        """

        values = (
            dados_teste.get("PROTOCOL"),
            dados_teste.get("DURATION_SECONDS", 0),
            dados_teste.get("PACKET_SIZE", 0),
            dados_teste.get("PACKET_COUNT", 0),
        )

        self._cur.execute(sql, values)
        result = self._cur.fetchone()

        if result:
            return result[0]  # TEST_ID existente

        self.insert(data=dados_teste)

        return self.get_latest_id()



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

    #(ip, duration, packet_size, packet_count)
