from .dao import DAO

class Server_Routines(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "Server_Routines"

    def create_table(self) -> None:
        """
        Cria Server_Routines com  parâmetros de configuração do teste.
        """
        self._cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
        SERVER_ROUTINE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TIME TEXT NOT NULL,
        ACTIVE BOOL NOT NULL,

        """)

        self._conn.commit()

    def get_latest_id(self):
        sql = f"SELECT MAX(SERVER_ROUTINE_ID) FROM {self.table_name}"
        self._cur.execute(sql)
        result = self._cur.fetchone()
        return result[0] if result else None  



if __name__ == '__main__':
    testes_de_rede = Server_Routines()
    #testes_de_rede.create_table()

    dados_teste = {
        "ROUTINE_ID": "5",
        "TIME": "10:00",
        "ACTIVE": True,
    }
    testes_de_rede.insert(dados_teste)
    all = testes_de_rede.fetch_all()
    for a in all:
        print(f"{a} -> {testes_de_rede._cur.lastrowid}")

    #(ip, duration, packet_size, packet_count)
