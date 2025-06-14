import json
import os
from .tests.ping_test import Ping
from .tests.iperfr3_test import Iperf
from .configuration.configuration import Configuration_
from .database.teste_bd import Database
#from database.resultados import ResultadosDAO

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
        self.database = Database.get_object()
        #ResultadosDAO.create_table()
    
    def execute_iperf3(self, server, test):
        return Iperf.run_iperf3(server, test["duration"], test["packet-size"], test["protocol"])
    
    def execute_ping(self, server, test):
        return Ping.run_ping(server, test["package-count"])
    
    def insert_tests(self, packet_size: int, duration: int, protocol: str = "none", ntests: int = 1, package_count: int = -1):
        if ntests < 0:
            print('Número inválido de testes')
        for i in range(0, ntests):
            self.configuration.make_config(packet_size, duration, protocol, package_count)


    def format_save_json(self, result, protocol, ping):
        
        obj = {}
        obj["TIMESTAMP_RESULT"] = result["bandwidth"]["timestamp"]
        obj["ROUTINE_ID"] = "0"

        if ping:
            obj["AVG_LATENCY"] = result["latency"]["results"]["avg_latency_ms"]
            obj["MAX_LATENCY"] = result["latency"]["results"]["max_latency_ms"]
        
        if protocol == "udp":
            obj["LOST_PACKETS"] = result["bandwidth"]["results"]["lost_packets"]
            obj["LOST_PERCENT"] = result["bandwidth"]["results"]["lost_percent"]
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BITS_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["JITTER"] = result["bandwidth"]["results"]["Jitter"]

        if protocol == "tcp":
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BITS_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["RETRANSMITS"] = result["bandwidth"]["results"]["retransmits"]
        
        return obj

    def clean_tests(self):
        self.configuration.clean_tests()
       
    def run_server(self):
        Iperf.run_iperf3_server()

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
                

            if test.get("package-count", 0):
                ping = True
                test_result["latency"] = self.execute_ping(server, test)

            formated_results = self.format_save_json(test_result, protocol, ping)
            #ResultadosDAO.insert(formated_results)
            print(formated_results)

            results.append(test_result)

        
        
        print({"results": results})
        
        return {"results": results}
#MIN_LATENCY REAL,                  
 #               AVG_LATENCY REAL,                  
  #              MAX_LATENCY REAL,                  
   #             LOST_PACKETS REAL,                 
    #            LOST_PERCENT REAL,                 
#
 #               -- Resultados de Iperf3
  #              BITS_PER_SECOND REAL,              
   #             BYTES_TRANSFERRED REAL,            
    #            JITTER REAL,                       
     #           RETRANSMITS REAL,        

if __name__ == "__main__":
    executor = Executor()
    executor.mainMenu()
    