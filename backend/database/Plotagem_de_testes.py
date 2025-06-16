from dao import DAO

class PlotsDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()
    @property
    def table_name(self) -> str:
        return "plots"

    def create_table(self) -> None:
        """
        Cria plots
        """
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                PLOT_ID INTEGER PRIMARY KEY AUTOINCREMENT,               
                PLOT_NAME TEXT NOT NULL,               
                TIMESTAMP_CREATED TEXT NOT NULL,        
                FIELDS_USED TEXT NOT NULL,              
                FILTER_CRITERIA TEXT,                   
                COLORS TEXT,                            
                LINE_TYPES TEXT,                        
                LABELS TEXT,                         
                ROUTINE_ID TEXT,                       
                TEST_ID INTEGER,                       
                PLOT_TYPE TEXT,                        
                DESCRIPTION TEXT,                      

                FOREIGN KEY (ROUTINE_ID) REFERENCES rotinas(ROUTINE_ID),
                FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID)
            )
        """)

        self._conn.commit()



if __name__ == '__main__':
    database = PlotsDAO()
    #testes_de_rede.create_table()

    data = {
        "PLOT_NAME": "Gráfico de Latência",
        "TIMESTAMP_CREATED": "2025-06-16 14:30:00",
        "FIELDS_USED": "MIN_LATENCY,AVG_LATENCY,MAX_LATENCY",
        "FILTER_CRITERIA": "PROTOCOLO = 'TCP'",
        "COLORS": "red,green,blue",
        "LINE_TYPES": "solid,dashed,dotted",
        "LABELS": "Mínima,Média,Máxima",
        "ROUTINE_ID": "rotina_001",
        "TEST_ID": 1,  
        "PLOT_TYPE": "line",
        "DESCRIPTION": "Gráfico gerado para análise de latência no teste TCP"
    }
    database.insert(data)
    all = database.fetch_all()
    for a in all:
        print(a)