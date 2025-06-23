from abc import ABC
from typing import Any, Dict, List, Tuple
from . import data_manager

class DAO(ABC):
    database_manager = data_manager.Database_Manager.get_object()

    """data acess object"""
    def __init__(self):
        self._conn = self.database_manager.connection
        self._cur = self.database_manager.cursor


    @property
    def table_name(self) -> str:
        """
        Deve retornar o nome da tabela.
        Subclasses **precisam** sobrescrever este método.
        """
        raise NotImplementedError("Subclasse deve implementar table_name()")
    
    def create_table(self) -> None:
        """
        Deve criar a tabela no banco caso não exista.
        Subclasses **precisam** sobrescrever este método.
        """
        raise NotImplementedError("Subclasse deve implementar create_table()") 
    
    """cara, isso gera uma fodendo Querry. 
    o **kwargs é um mapa que associa nomes a valores, exatamente como o insert de um banco
    oque acontece aqui é o seguinte, a classe que chamar o DAO precisa passar um dicionario para ela
    com todos os campos e informações que vai usar. Isso é aquilo que te falei do teste  "saber" se salvar,
    pq ele vai ter que enviar algo assim pra essa função 
    dao = ResultadosDAO()

    dao.insert(
        TEST_ID="0001",
        DURATION="30s",
        PACKAGE_LOSS=10,
        UTP=True,
        TCP=False,
        JITTER=None)
    OSS!
    """
    def insert(self, data: Dict[str, Any]) -> bool:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        try:
            sql = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
            self._cur.execute(sql, tuple(data.values()))
            self._conn.commit()
            return True
        except Exception as e:
            print(f'Erro ao inserir valor na tabela: {e}')
            return False

    def fetch_all(self) -> List[Tuple]:
        """Retorna todas as linhas da tabela."""
        sql = f"SELECT * FROM {self.table_name}"
        self._cur.execute(sql)
        return self._cur.fetchall()

    """
    monta uma querry nos parametros, deixei sem opc pra join pq pareceu meio inutil 
    Retorna os valores das colunas especificadas na tabela 'resultados'.
    
    USO
    data = dao.fetch_columns(
        ["DURATION", "PACKAGE_LOSS"],
        where="PACKAGE_LOSS IS NOT NULL"
    )
    o retorno da funçao é uma lista de dicionarios, ent tem q separar la na plot pro gráfico
    durations    = [row["DURATION"]    for row in data]
    packet_losses = [row["PACKAGE_LOSS"] for row in data]

    gepete ajudou legal nessa, mas ficou do crl
    MAGIA PURA OSS!
    """
    def fetch_where(self, where: str) -> List[Tuple]:

        sql = f"SELECT * FROM {self.table_name} {where}"
        self._cur.execute(sql) 
        return self._cur.fetchall()   

    def close(self) -> None:
        """Fecha cursor e conexão."""
        self._cur.close()
        self._conn.close()




