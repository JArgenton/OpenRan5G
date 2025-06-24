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

#export interface Test {
  #ip: string,
  #duration: string,
  #packetSize: string,
  #pingPackets: string,
  #protocol: string
  #ping: boolean,
 # default: boolean
#}

#OS PROBLEMAS FALTANTES SAO: timestamp apenas em bandwidth e a routine nao foi configurada direito ainda

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
       
    def run_server(self):
        Iperf.run_iperf3_server()

    def plotGraphic(self,server: str, xParam: str, yParam: str, date: list[str]):
        self.plotter.getValuesByTime(server, xParam, yParam, date)
        return self.plotter.generateGraphic(xParam, yParam)

    """
    Retorno resultados
        (RESULT_ID, ROUTINE_ID, TIMESTAMP_RESULT, MIN_LATENCY, AVG_LATENCY, MAX_LATENCY, LOST_PACKETS, LOST_PERCENT, BITS_PER_SECOND, BYTES_TRANSFERRED, JITTER, RETRANSMITS)
    """
    def load_results(self, where: str = ""):
        return Result.load_results_data(where)
    
    def getRoutines(self):
        routines = Routine.routine_table.fetch_all()
        formated_routines = []
        for routine in routines:
            formated_routines.append(Routine.formatRoutineJson(routine))
        return {"routines": formated_routines}
        
    def activateRoutine(self, r_id, active, time):
        if(active):
            Routine.routine_table.deactivate_routine_by_time(time)
        Routine.routine_table.activate_routine(r_id, active)
        
    
    def createRoutine(self, rtParams: dict):
        formated_tests = []
        for test in rtParams["tests"]:
            formated_tests.append(Test.format_save_test(test))
        Routine.create_routine_tests(rtParams["params"], formated_tests)
        print(Routine.R2T.fetch_all())
        print(Routine.routine_table.fetch_all())
        print(Test.database.fetch_all())
        
        print(Test.database.fetch_all())

    def run_tests(self, server):    
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
            print(formated_test)
            t_id = Test.get_or_create_test_id(formated_test)

            formated_result = Result.format_save_json(test_result, protocol, ping, t_id, server)
            
            Result.database.insert(formated_result)

            results.append(test_result)
            #print(self.databaser.fetch_all())
            #print(self.databaset.fetch_all())
        #print(results)
        return {"results": results}
   

if __name__ == "__main__":
    executor = Executor()
    routine = Routine("Teste3")
    routine_params = {
        "SERVER"    : "192.168.0.21",
        "TIME"      : "16:30",
        "ACTIVE"    : 1
    }

    tests = [
        {
            "packetSize": 256,
            "duration": 5,
            "protocol": "TCP",
            "pingPackets": 0
        },
        {
            "packetSize": 128,
            "duration" : 10,
            "protocol" : "UDP"
        }
    ]
    formated_tests = [executor.format_save_test(tests[0]), executor.format_save_test(tests[1])]

    routine.create_routine_tests(routine, routine_params, formated_tests)
    print(Routine.R2T.fetch_all())





#(ip, duration, packet_size, packet_count)