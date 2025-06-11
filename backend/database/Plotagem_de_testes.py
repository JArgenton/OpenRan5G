from dao import DAO

class PlotsDAO(DAO):
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
                PLOT_TYPE TEXT,                        
                DESCRIPTION TEXT,                      
                
                FOREIGN KEY (ROUTINE_ID) REFERENCES rotinas(ROUTINE_ID)
                FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID)
            )
        """)
        self._conn.commit()
