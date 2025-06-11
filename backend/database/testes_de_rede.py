from dao import DAO

class TestesDeRedeDAO(DAO):
    @property
    def table_name(self) -> str:
        return "testes_de_rede"

    def create_table(self) -> None:
        """
        Cria testes_de_rede com  parâmetros de configuração do teste.
        """
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                TEST_ID TEXT PRIMARY KEY AUTOINCREMENT,      
                TEST_NAME     
                -- Parâmetros Comuns 
                SERVER TEXT NOT NULL,            
                PROTOCOL TEXT NOT NULL,           
                DURATION_SECONDS REAL,             
                PACKET_SIZE INTEGER,               
                PACKET_COUNT INTEGER,              

                -- Indicadores de Tipo de Teste
                IS_PING BOOLEAN NOT NULL,          
                IS_IPERF BOOLEAN NOT NULL          
            )
        """)
        self._conn.commit()
