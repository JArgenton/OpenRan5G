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
                PLOT_ID TEXT PRIMARY KEY,               
                PLOT_NAME TEXT NOT NULL,               
                TIMESTAMP_CREATED TEXT NOT NULL,        

                -- Informações sobre os dados utilizados
                FIELDS_USED TEXT NOT NULL,              -- Campos do resultado usados na plotagem (ex: "AVG_LATENCY,BITS_PER_SECOND")
                FILTER_CRITERIA TEXT,                   -- Critérios de filtro aplicados aos dados (ex: "PROTOCOL = 'TCP' AND JITTER IS NOT NULL")

                -- Aparência da plotagem
                COLORS TEXT,                            
                LINE_TYPES TEXT,                        
                LABELS TEXT,                         

                -- Relacionamento com rotinas (opcional, mas útil se uma plotagem estiver ligada a uma rotina específica)
                ROUTINE_ID TEXT,                        -- ID da rotina associada (se aplicável)

                -- Outras informações
                PLOT_TYPE TEXT,                         -- Tipo de gráfico (ex: "line", "bar", "scatter")
                DESCRIPTION TEXT,                       -- Descrição detalhada da plotagem

                FOREIGN KEY (ROUTINE_ID) REFERENCES rotinas(ROUTINE_ID)
                FOREIGN KEY (TEST_ID) REFERENCES testes_de_rede(TEST_ID)
            )
        """)
        self._conn.commit()
