from dao import DAO


class RotinasDAO(DAO):
    @property
    def table_name(self) -> str:
        return "rotinas"

    def create_table(self) -> None:
        """
        Cria a tabela 'rotinas' para armazenar sequências de testes.
        """
        self._cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                ROUTINE_ID TEXT PRIMARY KEY,             -- ID único da rotina
                ROUTINE_NAME TEXT NOT NULL,              -- Nome descritivo da rotina
                TIMESTAMP_CREATED TEXT NOT NULL,         -- Data e hora da criação da rotina
                DESCRIPTION TEXT,                        -- Descrição detalhada da rotina
                
                -- Configuração da rotina
                TARGET_IP TEXT,                          -- IP/Host alvo principal da rotina
                TEST_SEQUENCE_IDS TEXT NOT NULL,         -- IDs dos TEST_ID da tabela 'testes_de_rede' que compõem a sequência (ex: "PING-001,IPERF-TCP-001")
                SCHEDULE TEXT,                           -- Agendamento da rotina (ex: "daily", "weekly", "manual")
                IS_ACTIVE BOOLEAN NOT NULL               -- Indica se a rotina está ativa para execução automática
            )
        """)
        self._conn.commit()