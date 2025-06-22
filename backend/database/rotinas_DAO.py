from .dao import DAO

class RotinasDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()

    @property
    def table_name(self) -> str:
        return "rotinas"

    def create_table(self) -> None:
        """
        Cria testes_de_rede com  parâmetros de configuração do teste.
        """
        self._cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name}(
        ROUTINE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        SERVER TEXT NOT NULL,
        TIME TEXT NOT NULL,
        ACTIVE BOOL NOT NULL)
        """)

        self._conn.commit()

if __name__ == '__main__':
    rotine = RotinasDAO()

    dados_teste = {
        "NAME" : "ROTINA DE TESTE",
        "SERVER" : "127.0.0.0",
        "TIME" : "17:30",
        "ACTIVE" : 1
    }
    rotine.insert(dados_teste)
    all = rotine.fetch_all()
    for a in all:
        print(a)
    #python3 -m backend.database.rotinas_DAO