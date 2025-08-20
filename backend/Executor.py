import json
import os
from .tests.ping_test import Ping
from .tests.iperfr3_test import Iperf
from .configuration.configuration import Configuration_
from .database.resultados import ResultadosDAO
from .database.testes_de_rede import TestesDeRedeDAO
from .programer.routine import Routine
from .programer.network_test import Test
from .programer.results import Result
from .plotting.plotGraphic import Plotter
from .database.relacionamentos_R2T import _Relacionamento_R2T as R2T
import getpass
from datetime import datetime, timedelta
from .database.rotinas_DAO import RotinasDAO
from .Server_routine import server_routines
from .plotting.statistics import Statistician
from .plotting.Potting import StatisticsPlot
from pathlib import Path
#export interface Test {
  #ip: string,
  #duration: string,
  #packetSize: string,
  #pingPackets: string,
  #protocol: string
  #ping: boolean,
 # default: boolean
#}

class Executor:
    def __init__(self):
        self.configuration = Configuration_.getObject()
        self.plotter = Plotter()
        self.statistic = Statistician()
        self.statisticPlot = StatisticsPlot()
        
    
    def execute_iperf3(self, server, test):
        return Iperf.run_iperf3(server, test["duration"], test["packetSize"], test["protocol"])
    
    def execute_ping(self, server, test):
        return Ping.run_ping(server, test["pingPackets"])
    
    def insert_tests(self, packet_size: int, duration: int, protocol: str = "none", ntests: int = 1, package_count: int = -1):
        if ntests < 0:
            print('Número inválido de testes')
        for i in range(0, ntests):
            self.configuration.make_config(packet_size, duration, protocol, package_count)

    
    def clean_tests(self):
        self.configuration.clean_tests()

    def clean_routine(self):
        self.configuration.clean_routine()
       
    def run_server(self):
        return Iperf.run_iperf3_server()

    def kill_server(self, process):
        Iperf.stop_iperf3_server(process)

    def plotGraphicByTime(self,server: str, xParam: str, yParam: str, date: list[str]):
        self.plotter.getValuesByTime(server, xParam, yParam, date)
        return self.plotter.generateGraphic(xParam, yParam)
    
    def plotGraphicByRoutine(self, server: str, routineName: str, yParam: str):
        self.plotter.getValuesByRoutine(server, routineName, yParam)
        return self.plotter.generateGraphic("", yParam, "", 1)

    """
    Retorno resultados
        (RESULT_ID, ROUTINE_ID, TIMESTAMP_RESULT, MIN_LATENCY, AVG_LATENCY, MAX_LATENCY, LOST_PACKETS, LOST_PERCENT, BITS_PER_SECOND, BYTES_TRANSFERRED, JITTER, RETRANSMITS)
    """
    def load_results(self, where: str = ""):
        return Result.load_results_data(where)
    
    def getRoutines(self):
        routines = Routine.routine_table.fetch_all()
        formated_routines = []
        if routines is None:
            return {"routines": []}
        for routine in routines:
            formated_routines.append(Routine.formatRoutineJson(routine))
        return {"routines": formated_routines}
    
    def getRoutineTests(self, r_id: int):
        tests = Test.get_tests_by_RID(r_id)
        formated_tests = []
        if tests is None: 
            return {"tests": []}
        for test in tests:
            formated_tests.append(Test.format_tests_json(test)) #TEST_ID, PROTOCOL, DURATION_SECONDS, PACKET_SIZE, PACKET_COUNT
        print(formated_tests)
        return {"tests": formated_tests}
    
    def getRoutineTestResults(self, r_id: int, t_id: int):
        results = Routine.getRoutineTestResults(r_id, t_id)
        print(results)
        fromated_results = []
        if results is None: 
            return {"results": []}
        for result in results:
            fromated_results.append(Result.format_result_json(result))
        return {"results": fromated_results}
        
    def activateRoutine(self, r_id, active, time):
        if(active):
            Routine.deactivate_routine_by_time(time)
        Routine.activate_routine(r_id, active)

    def getSavedRoutines(self):
        db = server_routines.get_instance()
        return db.view_saved_routines()
    
    def create_routine_client(self, rtParams: dict):
        formated_tests = []
        time = rtParams["params"]["time"]
        h,m = map(int, time.split(":"))
        hour, minutes = self.configuration.set_round_time(h,m)
        self.agendar_execucao_cliente(hour, minutes)
        rtParams["params"]["time"] = f'{hour:02d}:{minutes:02d}'
        for test in rtParams["tests"]:
            formated_tests.append(Test.format_save_test(test))
        Routine.create_routine_tests(rtParams["params"], formated_tests)
        

    def create_routine_server(self,hour, minute):
        db = server_routines.get_instance()
        hour, minutes = self.configuration.set_round_time(hour,minute)
        try:
            db.create_server_routine(hour, minutes)
        except:
            print("Erro ao inserir rotina")
            return
        
        self.agendar_execucao_servidor(hour, minutes)
        
        

    def deleteRoutine(self, routineID: int):
        Routine.delete_routine(routineID)

    def get_statistics_by_interval(self, test_id, start_time, end_time, column_name: str):
        try:
            results = Result.get_test_results_by_interval(test_id, start_time, end_time)
            print(f"✅ {len(results)} resultados carregados.")

            self.statistic.load_data(results)
            print("✅ Dados carregados no Statistician.")

            report = self.statistic.analyze(column_name.upper())
            print("✅ Estatísticas geradas.")
            print(report)

            self.statisticPlot.save_report_plot(report)
        except Exception as e:
            print("❌ Erro inesperado:", str(e))

    def get_statistics_by_routine(self, routine_id, test_id, column_name: str):
        try:
            results = Result.get_test_results_by_routineID(routine_id, test_id)
            print(f"✅ {len(results)} resultados carregados.")

            self.statistic.load_data(results)
            print("✅ Dados carregados no Statistician.")

            report = self.statistic.analyze(column_name.upper())
            print("✅ Estatísticas geradas.")
            print(report)

            self.statisticPlot.save_report_plot(report)
        except Exception as e:
            print("❌ Erro inesperado:", str(e))
        

    def format_result_for_terminal(self, result: dict) -> str:
        linhas = []

        timestamp = (
            result.get("latency", {}).get("timestamp") or
            result.get("bandwidth", {}).get("timestamp") or
            "Desconhecido"
        )
        linhas.append(f"\n🕒 Timestamp: {timestamp}\n")

        # Bandwidth (TCP/UDP)
        if "bandwidth" in result:
            bw = result["bandwidth"]
            protocolo = bw.get("protocol", "").upper()
            params = bw.get("parameters", {})
            res = bw.get("results", {})

            linhas.append(f"📶 TESTE DE BANDA ({protocolo})")
            linhas.append("-" * 40)
            linhas.append(f"Servidor: {params.get('server', 'N/A')}")
            linhas.append(f"Duração: {params.get('duration_seconds', 'N/A')}s")
            linhas.append(f"Tamanho do Pacote: {params.get('packet_size', 'N/A')} bytes")

            bps = res.get("bits_per_second", 0)
            linhas.append(f"Bits por segundo: {bps / 1e6:.2f} Mbps")

            bytes_transferidos = res.get("bytes_transferred", 0)
            linhas.append(f"Bytes transferidos: {bytes_transferidos / 1e6:.2f} MB")

            if protocolo == "TCP":
                linhas.append(f"Retransmissões: {res.get('retransmits', 0)}")
            elif protocolo == "UDP":
                linhas.append(f"Pacotes enviados: {res.get('packets', 0)}")
                linhas.append(f"Perda de pacotes: {res.get('lost_packets', 0)} ({res.get('lost_percent', 0):.1f}%)")
                linhas.append(f"Jitter: {res.get('Jitter', 0):.2f} ms")

            linhas.append("")  # Espaço após banda

        # Latency (Ping)
        if "latency" in result:
            lat = result["latency"]
            params = lat.get("parameters", {})
            res = lat.get("results", {})

            linhas.append("🏓 TESTE DE LATÊNCIA (Ping)")
            linhas.append("-" * 40)
            linhas.append(f"Alvo: {params.get('target', 'N/A')}")
            linhas.append(f"Pacotes: {params.get('packet_count', 'N/A')}")
            linhas.append(f"Min: {res.get('min_latency_ms', 0)} ms | "
                        f"Média: {res.get('avg_latency_ms', 0)} ms | "
                        f"Máx: {res.get('max_latency_ms', 0)} ms")

        return "\n".join(linhas)

    def run_tests(self, server, routine_id = -1):    
        with open('backend/configuration/tests.json', 'r') as file:
            data = json.load(file)

        results = []
        for index, test in enumerate(data['tests'], start=0):
            test_result = {}

            protocol = ""
            ping = False

            if test.get("protocol", 0):
                protocol = test["protocol"]
                test_result["bandwidth"] = self.execute_iperf3(server, test)
                

            if test.get("pingPackets", 0):
                ping = True
                test_result["latency"] = self.execute_ping(server, test)

            if(routine_id != -1):
                formated_test = Test.format_save_test(test)
                t_id = Test.get_or_create_test_id(formated_test)
                formated_result = Result.format_save_json(test_result, protocol, ping, t_id, server, routine_id)
                Result.database.insert(formated_result)

            results.append(test_result)

        return {"results": results}
    
    def agendar_execucao_servidor(self, hora: int, minuto: int):
        print("Agendando execução...")
        
        # Caminho para a raiz do projeto (ajuste se necessário)
        raiz_projeto = Path(__file__).resolve().parent.parent

        # Corrige horário para executar 1 minuto antes
        horario = datetime(2024, 1, 1, hora, minuto) - timedelta(minutes=2)
        hora_agendada = horario.hour
        minuto_agendado = horario.minute

        # Linha de agendamento com python -m e cd para o diretório do projeto
        cron_linha = (
            f"{minuto_agendado} {hora_agendada} * * * cd {raiz_projeto} && "
            f"/usr/bin/python3 -m backend.Server_routine # agendado_auto"
        )

        # Lê a crontab atual
        crontab_atual = os.popen("crontab -l 2>/dev/null").read()

        if cron_linha in crontab_atual:
            print("Execução já agendada.")
            return

        # Adiciona nova linha
        nova_crontab = crontab_atual + f"\n{cron_linha}\n"
        with os.popen("crontab -", "w") as cron:
            cron.write(nova_crontab)

        print(f"Script agendado para {hora_agendada:02d}:{minuto_agendado:02d} diariamente com 'python -m'.")

    def agendar_execucao_cliente(self, hora: int, minuto: int):
        print("Agendando execução...")
        
        # Caminho para a raiz do projeto (ajuste se necessário)
        raiz_projeto = Path(__file__).resolve().parent.parent
        print(raiz_projeto)

        # Corrige horário para executar 1 minuto antes
        horario = datetime(2024, 1, 1, hora, minuto) - timedelta(minutes=1)
        hora_agendada = horario.hour
        minuto_agendado = horario.minute

        # Linha de agendamento com python -m e cd para o diretório do projeto
        cron_linha = (
            f"{minuto_agendado} {hora_agendada} * * * cd {raiz_projeto} && "
            f"/usr/bin/python3 -m backend.Executor # agendado_auto"
        )

        # Lê a crontab atual
        crontab_atual = os.popen("crontab -l 2>/dev/null").read()

        if cron_linha in crontab_atual:
            print("Execução já agendada.")
            return

        # Adiciona nova linha
        nova_crontab = crontab_atual + f"\n{cron_linha}\n"
        with os.popen("crontab -", "w") as cron:
            cron.write(nova_crontab)

        print(f"Script agendado para {hora_agendada:02d}:{minuto_agendado:02d} diariamente com 'python -m'.")




if __name__ == '__main__':
    executor = Executor()
    tabela_rotinas = RotinasDAO()
    tabela_r2t = R2T()
    tabela_testes = TestesDeRedeDAO()

    hour, minute = executor.configuration.get_HH_MM()
    hour, minute = executor.configuration.set_round_time(hour, minute)
    time = f"{hour:02d}:{minute:02d}"

    executor.clean_tests()

    where = f"""WHERE TIME = '{time}'"""
    rotina_resultado = tabela_rotinas.fetch_where(where)
    print(rotina_resultado)

    if not rotina_resultado:
        print("Nenhuma rotina encontrada para o horário atual.")
        exit(0)
    routine_id = None
    for routine in rotina_resultado:
        
        if bool(int(routine[4])):
            routine_id = routine[0]
            server = routine[2]

    
    if routine_id is None:
        print("Nenhum teste encontrado no horario atual")
        exit(0)

    # Busca testes relacionados
    query_rel = f"""SELECT TEST_ID FROM {tabela_r2t.table_name} WHERE ROUTINE_ID = {routine_id}"""
    tabela_r2t._cur.execute(query_rel)
    relacionamentos = tabela_r2t._cur.fetchall()
    print(relacionamentos)

    if not relacionamentos:
        print(f"Nenhum teste relacionado à rotina {routine_id}")
        exit(0)

    for rel in relacionamentos:
        test_id = rel[0]

        # Busca o teste na tabela de testes
        where = f"""WHERE TEST_ID = {test_id}"""
        teste_data = tabela_testes.fetch_where(where)
        print(teste_data)

        if not teste_data:
            print(f"⚠️  Teste {test_id} não encontrado.")
            continue

        teste = teste_data[0]

        packet_size = int(teste[3])
        duration = int(teste[2])
        protocol = str(teste[1])
        package_count = int(teste[4])

        executor.insert_tests(packet_size, duration, protocol, ntests=1, package_count=package_count)

    executor.run_tests(server, routine_id)