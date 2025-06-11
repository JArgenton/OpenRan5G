from dao import DAO

class ResultadosDAO(DAO):
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
                TEST_ID TEXT NOT NULL,              
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
