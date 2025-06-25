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
        Iperf.run_iperf3_server()

    def plotGraphicByTime(self,server: str, xParam: str, yParam: str, date: list[str]):
        self.plotter.getValuesByTime(server, xParam, yParam, date)
        return self.plotter.generateGraphic(xParam, yParam)
    
    def plotGraphicByRoutine(self, server: str, routineName: str, yParam: str):
        self.plotter.getValuesByRoutine(server, routineName, yParam)
        return self.plotter.generateGraphic("", yParam)

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
        fromated_results = []
        if results is None: 
            return {"results": []}
        for result in results:
            fromated_results.append(Result.format_result_json(result))
            print(fromated_results)
        return {"results": fromated_results}
        
    def activateRoutine(self, r_id, active, time):
        if(active):
            Routine.deactivate_routine_by_time(time)
        Routine.activate_routine(r_id, active)
    
    def createRoutine(self, rtParams: dict):
        formated_tests = []
        time = rtParams["params"]["time"]
        h,m = map(int, time.split(":"))
        hour, minutes = Configuration_.set_round_time(h,m)
        rtParams["params"]["time"] = f'{hour}:{minutes}'
        for test in rtParams["tests"]:
            formated_tests.append(Test.format_save_test(test))
        Routine.create_routine_tests(rtParams["params"], formated_tests)

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

            formated_test = Test.format_save_test(test)
            #print(formated_test)
            t_id = Test.get_or_create_test_id(formated_test)

            formated_result = Result.format_save_json(test_result, protocol, ping, t_id, server, routine_id)
            
            Result.database.insert(formated_result)

            results.append(test_result)
            #print(self.databaser.fetch_all())
            #print(self.databaset.fetch_all())
        #print(results)
        return {"results": results}
    
    def agendar_execucao_para(hora: int, minuto: int):
        caminho_script = os.path.abspath(__file__)
        
        horario = datetime(2024, 1, 1, hora, minuto) - timedelta(minutes=1)
        hora_agendada = horario.hour
        minuto_agendado = horario.minute

        cron_linha = f"{minuto_agendado} {hora_agendada} * * * /usr/bin/python3 {caminho_script} # agendado_auto"
        crontab_atual = os.popen(f"crontab -l 2>/dev/null").read()

        if cron_linha in crontab_atual:
            print("Execução já agendada.")
            return

        nova_crontab = crontab_atual + f"\n{cron_linha}\n"
        with os.popen("crontab -", "w") as cron:
            cron.write(nova_crontab)

        print(f"Script agendado para {hora_agendada:02d}:{minuto_agendado:02d} diariamente.")



if __name__ == '__main__':
    executor = Executor()
    tabela_rotinas = RotinasDAO()
    tabela_r2t = R2T()
    tabela_testes = TestesDeRedeDAO()

    hour, minute = executor.configuration.get_HH_MM()
    hour, minute = executor.configuration.set_round_time(hour, minute)
    time = f"{hour:02d}:{minute:02d}"

    executor.clean_tests()

    query = f"""SELECT * FROM {tabela_rotinas.table_name} WHERE TIME = '{time}'"""
    rotina_resultado = tabela_rotinas.fetch_where(query)

    if not rotina_resultado:
        print("Nenhuma rotina encontrada para o horário atual.")
        exit(0)

    rotina_info = rotina_resultado[0]
    routine_id = rotina_info['ROUTINE_ID']
    server = rotina_info['SERVER']

    print(f"Executando rotina {routine_id} no servidor {server}")

    # Busca testes relacionados
    query_rel = f"""SELECT TEST_ID FROM {tabela_r2t.table_name} WHERE ROUTINE_ID = {routine_id}"""
    relacionamentos = tabela_r2t.fetch_where(query_rel)

    if not relacionamentos:
        print(f"Nenhum teste relacionado à rotina {routine_id}")
        exit(0)

    for rel in relacionamentos:
        test_id = rel["TEST_ID"]

        # Busca o teste na tabela de testes
        query_test = f"""SELECT * FROM {tabela_testes.table_name} WHERE TEST_ID = {test_id}"""
        teste_data = tabela_testes.fetch_where(query_test)

        if not teste_data:
            print(f"⚠️  Teste {test_id} não encontrado.")
            continue

        teste = teste_data[0]

        packet_size = int(teste.get("PACKET_SIZE", 64))
        duration = int(float(teste.get("DURATION_SECONDS", 10)))
        protocol = str(teste.get("PROTOCOL", "none"))
        package_count = int(teste.get("PACKET_COUNT", -1))

        executor.insert_tests(packet_size, duration, protocol, ntests=1, package_count=package_count)

        executor.run_tests(server, routine_id)