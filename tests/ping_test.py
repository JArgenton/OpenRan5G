
import subprocess
import os
from typing import Any, Dict,
from datetime import datetime
import uuid 

# --- CLASSE TESTE IMPLEMENTADA ---
class Test:

    def __init__(self, db_path: str = "app.db"):

        self.db_path = db_path
        self.testes_dao = TestesDeRedeDAO(db_path=self.db_path)
        self.resultados_dao = ResultadosDAO(db_path=self.db_path)
        self.iperf_executor = IperfExecutor() 

        self.test_config: Dict[str, Any] | None = None  # Parâmetros do teste atual
        self.test_results_raw: Dict[str, Any] | None = None # Resultados brutos da execução do teste
        self.test_id: str | None = None # ID único da configuração do teste

    def initialize(self, test_parameters: Dict[str, Any]) -> None:
        """
        Prepara a classe Test com os parâmetros para um novo teste.
        Gera um ID único para este teste e adiciona o timestamp de inicialização.

        Args:
            test_parameters: Um dicionário com os parâmetros de configuração do teste,
                             como 'SERVER', 'PROTOCOL', 'IS_PING', 'PACKET_COUNT', etc.
        """
        self.test_id = str(uuid.uuid4()) # Gera um ID único para este conjunto de parâmetros
        self.test_config = test_parameters.copy() # Copia para evitar modificações externas
        self.test_config["TEST_ID"] = self.test_id # Atribui o ID gerado
        self.test_config["TIMESTAMP"] = Configuration.getObject().get_formated_date() # Adiciona o timestamp
        print(f"Teste '{self.test_id}' inicializado com os parâmetros.")

    def run(self) -> Dict[str, Any]:
        """
        Executa o teste de rede (Ping ou Iperf) com base nos parâmetros
        previamente definidos em `initialize()`.

        Armazena os resultados brutos da execução internamente.

        Returns:
            Um dicionário contendo os resultados brutos do teste ou um dicionário de erro.

        Raises:
            ValueError: Se o teste não foi inicializado ou os parâmetros são inválidos.
            RuntimeError: Se ocorrer um erro durante a execução do `ping` ou `iperf`.
        """
        if not self.test_config:
            raise ValueError("A classe Test não foi inicializada. Chame 'initialize' primeiro.")

        is_ping = self.test_config.get("IS_PING", False)
        is_iperf = self.test_config.get("IS_IPERF", False)
        
        # Garante que apenas um tipo de teste está marcado como True
        if not (is_ping ^ is_iperf): # XOR lógico para garantir que apenas um seja True
             raise ValueError("Tipo de teste inválido. Apenas um entre 'IS_PING' ou 'IS_IPERF' deve ser True.")

        if is_ping:
            target = self.test_config.get("SERVER")
            count = self.test_config.get("PACKET_COUNT")
            if not target or count is None:
                raise ValueError("Parâmetros 'SERVER' e 'PACKET_COUNT' são obrigatórios para teste de PING.")
            
            print(f"Executando teste de PING para {target} com {count} pacotes...")
            try:
                self.test_results_raw = run_ping(target=target, count=count)
                print("Teste de PING concluído.")
            except (subprocess.CalledProcessError, RuntimeError) as e:
                error_msg = f"Erro ao executar PING: {e}"
                print(error_msg)
                self.test_results_raw = {"error": error_msg}
        
        elif is_iperf:
            server = self.test_config.get("SERVER")
            duration = self.test_config.get("DURATION_SECONDS")
            protocol = self.test_config.get("PROTOCOL", "TCP")
            size = self.test_config.get("PACKET_SIZE", 512)
            port = self.test_config.get("PORT", 5201)

            if not server or duration is None:
                raise ValueError("Parâmetros 'SERVER' e 'DURATION_SECONDS' são obrigatórios para teste de IPERF.")
            
            print(f"Executando teste de IPERF3 ({protocol}) para {server} por {duration} segundos...")
            try:
                self.test_results_raw = self.iperf_executor.run_iperf3(
                    server=server, duration=int(duration), size=size, protocol=protocol, port=port
                )
                print("Teste de IPERF3 concluído.")
            except RuntimeError as e:
                error_msg = f"Erro ao executar IPERF3: {e}"
                print(error_msg)
                self.test_results_raw = {"error": error_msg}
        
        return self.test_results_raw

    def save_test(self) -> None:
        """
        Salva a configuração do teste (parâmetros de entrada) na tabela 'testes_de_rede'.
        Deve ser chamado *após* `initialize()`.
        """
        if not self.test_config:
            raise ValueError("Não há parâmetros de teste para salvar. Chame 'initialize' primeiro.")
        
        try:
            self.testes_dao.insert(self.test_config)
            print(f"Configuração do teste '{self.test_id}' salva em 'testes_de_rede'.")
        except Exception as e:
            print(f"Erro ao salvar configuração do teste '{self.test_id}': {e}")
            raise

    def save_results(self) -> None:
        """
        Salva os resultados da medição do teste na tabela 'resultados'.
        Deve ser chamado *após* `run()` e se a execução do teste foi bem-sucedida.
        """
        if not self.test_results_raw or "error" in self.test_results_raw:
            print(f"Não há resultados válidos para salvar para o teste '{self.test_id}'.")
            return

        result_id = str(uuid.uuid4()) # ID único para este registro de resultado
        timestamp_result = self.test_results_raw.get("timestamp", Configuration.getObject().get_formated_date())
        
        results_data = self.test_results_raw.get("results", {})
        protocol = self.test_config.get("PROTOCOL", "").upper() # Usa o protocolo da config do teste

        # Mapeamento para a tabela 'resultados', preenchendo com None onde não aplicável
        data_to_save = {
            "RESULT_ID": result_id,
            "TEST_ID": self.test_id, # Vincula este resultado à sua configuração de teste
            "TIMESTAMP_RESULT": timestamp_result,
            "MIN_LATENCY": None, "AVG_LATENCY": None, "MAX_LATENCY": None,
            "LOST_PACKETS": None, "LOST_PERCENT": None, "BITS_PER_SECOND": None,
            "BYTES_TRANSFERRED": None, "JITTER": None, "RETRANSMITS": None
        }

        if protocol == "ICMP": # Resultados de PING
            data_to_save["MIN_LATENCY"] = results_data.get("min_latency_ms")
            data_to_save["AVG_LATENCY"] = results_data.get("avg_latency_ms")
            data_to_save["MAX_LATENCY"] = results_data.get("max_latency_ms")
            data_to_save["LOST_PACKETS"] = results_data.get("lost_packets")
            data_to_save["LOST_PERCENT"] = results_data.get("lost_percent")
        elif protocol == "TCP": # Resultados de IPERF3 TCP
            data_to_save["BITS_PER_SECOND"] = results_data.get("bits_per_second")
            data_to_save["BYTES_TRANSFERRED"] = results_data.get("bytes_transferred")
            data_to_save["RETRANSMITS"] = results_data.get("retransmits")
        elif protocol == "UDP": # Resultados de IPERF3 UDP
            data_to_save["BITS_PER_SECOND"] = results_data.get("bits_per_second")
            data_to_save["BYTES_TRANSFERRED"] = results_data.get("bytes_transferred")
            data_to_save["LOST_PACKETS"] = results_data.get("lost_packets")
            data_to_save["LOST_PERCENT"] = results_data.get("lost_percent")
            data_to_save["JITTER"] = results_data.get("jitter")
        
        try:
            self.resultados_dao.insert(data_to_save)
            print(f"Resultados do teste '{self.test_id}' (ID do resultado: '{result_id}') salvos em 'resultados'.")
        except Exception as e:
            print(f"Erro ao salvar resultados do teste '{self.test_id}': {e}")
            raise

    def close_db_connections(self):
        """Fecha as conexões com o banco de dados dos DAOs utilizados por esta instância de Test."""
        self.testes_dao.close()
        self.resultados_dao.close()
        print("Conexões com o banco de dados fechadas para a classe Test.")


# --- Bloco de Exemplo de Uso (para demonstração) ---
if __name__ == "__main__":
    db_file = "network_tests_v2.db" # Nome diferente para evitar conflitos anteriores
    
    # Limpa o arquivo do banco de dados para um teste limpo
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Arquivo de banco de dados '{db_file}' removido para um teste limpo.")

    # 1. Inicializar e criar as tabelas do banco de dados
    # (Isto seria feito uma vez no início da aplicação)
    testes_dao_init = TestesDeRedeDAO(db_path=db_file)
    resultados_dao_init = ResultadosDAO(db_path=db_file)
    plots_dao_init = PlotsDAO(db_path=db_file)
    rotinas_dao_init = RotinasDAO(db_path=db_file)
    execucoes_dao_init = ExecucoesAutomaticasDAO(db_path=db_file)
    programacao_dao_init = ProgramacaoDAO(db_path=db_file)

    testes_dao_init.create_table()
    resultados_dao_init.create_table()
    plots_dao_init.create_table()
    rotinas_dao_init.create_table()
    execucoes_dao_init.create_table()
    programacao_dao_init.create_table()
    
    # Fechar as conexões de inicialização (cada DAO é um singleton, mas é boa prática)
    testes_dao_init.close()
    resultados_dao_init.close()
    plots_dao_init.close()
    rotinas_dao_init.close()
    execucoes_dao_init.close()
    programacao_dao_init.close()
    print("Todas as tabelas criadas/verificadas.")

    # 2. Usando a classe Test para executar e salvar testes
    network_test_executor = Test(db_path=db_file)

    # --- Exemplo de Teste de PING ---
    print("\n--- INICIANDO FLUXO DE TESTE PING ---")
    ping_parameters = {
        "SERVER": "8.8.8.8",
        "PROTOCOL": "ICMP",
        "PACKET_COUNT": 4,
        "IS_PING": True,
        "IS_IPERF": False
    }
    try:
        network_test_executor.initialize(ping_parameters) # 1. Inicializa o teste
        network_test_executor.save_test() # 2. Salva a configuração do teste no DB
        ping_output_data = network_test_executor.run() # 3. Executa o teste
        if "error" not in ping_output_data:
            network_test_executor.save_results() # 4. Salva os resultados no DB
            print("FLUXO DE TESTE PING CONCLUÍDO COM SUCESSO.")
        else:
            print(f"FLUXO DE TESTE PING FALHOU: {ping_output_data['error']}")
    except Exception as e:
        print(f"ERRO CRÍTICO NO FLUXO DE TESTE PING: {e}")

    # --- Exemplo de Teste de IPERF3 (TCP) ---
    print("\n--- INICIANDO FLUXO DE TESTE IPERF3 (TCP) ---")
    # Nota: Para IPERF3, você precisa de um servidor iperf3 rodando no IP especificado.
    # Ex: 'iperf3 -s' no terminal do servidor.
    iperf_tcp_parameters = {
        "SERVER": "127.0.0.1", # Mude para o IP do seu servidor iperf3
        "PROTOCOL": "TCP",
        "DURATION_SECONDS": 5,
        "PACKET_SIZE": 1460,
        "IS_PING": False,
        "IS_IPERF": True,
        "PORT": 5201 
    }
    try:
        network_test_executor.initialize(iperf_tcp_parameters) # 1. Inicializa
        network_test_executor.save_test() # 2. Salva configuração
        iperf_tcp_output_data = network_test_executor.run() # 3. Executa
        if "error" not in iperf_tcp_output_data:
            network_test_executor.save_results() # 4. Salva resultados
            print("FLUXO DE TESTE IPERF3 (TCP) CONCLUÍDO COM SUCESSO.")
        else:
            print(f"FLUXO DE TESTE IPERF3 (TCP) FALHOU: {iperf_tcp_output_data['error']}")
    except Exception as e:
        print(f"ERRO CRÍTICO NO FLUXO DE TESTE IPERF3 (TCP): {e}")

    # --- Fechar as conexões do banco de dados da instância Test ---
    network_test_executor.close_db_connections()

    # --- Opcional: Verificação final dos dados no DB ---
    print("\n--- VERIFICANDO DADOS SALVOS NO BANCO ---")
    temp_testes_dao_check = TestesDeRedeDAO(db_path=db_file)
    temp_resultados_dao_check = ResultadosDAO(db_path=db_file)

    print("\nDados em 'testes_de_rede':")
    for row in temp_testes_dao_check.fetch_all():
        print(row)

    print("\nDados em 'resultados':")
    for row in temp_resultados_dao_check.fetch_all():
        print(row)

    temp_testes_dao_check.close()
    temp_resultados_dao_check.close()
    print("\nVerificação de dados concluída. Conexões temporárias fechadas.")