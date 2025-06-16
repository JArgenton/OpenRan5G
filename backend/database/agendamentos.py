from dao import DAO

class AgendamentosDAO(DAO):
    def __init__(self):
        super().__init__()
        self.create_table()
    @property
    def table_name(self) -> str:
        return "agendamentos"

    def create_table(self) -> None:
        """
        Cria a tabela 'programacao' para armazenar os detalhes de agendamento das rotinas.
        """
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                PROGRAMACAO_ID TEXT PRIMARY KEY,         -- ID único da programação
                ROUTINE_ID TEXT NOT NULL,                -- Chave estrangeira para a rotina associada
                
                FREQUENCY_TYPE TEXT NOT NULL,            -- Tipo de frequência (ex: "DIARIO", "SEMANAL", "MENSAL", "CUSTOM")
                INTERVAL_VALUE INTEGER,                  -- Valor do intervalo (ex: 1 para diário, 2 para a cada 2 dias/semanas)
                DAYS_OF_WEEK TEXT,                       -- Dias da semana para repetição semanal/custom (ex: "SEG,TER,QUA")
                TIME_OF_DAY TEXT NOT NULL,               -- Horário da execução (ex: "08:00", "22:30")
                
                START_DATE TEXT NOT NULL,                -- Data de início da programação
                END_DATE TEXT,                           -- Data de término da programação (opcional)
                IS_ACTIVE BOOLEAN NOT NULL,              -- Indica se esta entrada de programação está ativa
                
                LAST_RUN_TIMESTAMP TEXT,                 -- Último timestamp em que a rotina foi agendada por esta entrada
                NEXT_RUN_TIMESTAMP TEXT,                 -- Próximo timestamp agendado por esta entrada

                FOREIGN KEY (ROUTINE_ID) REFERENCES rotinas(ROUTINE_ID)
            )
        """)
        self._conn.commit()