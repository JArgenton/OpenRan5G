import json
import os
from tests.iperfr3_test import Iperf
from tests.ping_test import Ping
from configuration.configuration import Configuration_
from database.teste_bd import Database

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
    
    def execute_iperf3(self, server, test):
        return Iperf.run_iperf3(server, test["duration"], test["packet-size"], test["protocol"])
    
    def execute_ping(self, server, test):
        return Ping.run_ping(server, test["package-count"])
    
    def insert_tests(self, packet_size: int, duration: int, protocol: str = "none", ntests: int = 1, package_count: int = -1):
        if ntests < 0:
            print('Número inválido de testes')
        for i in range(0, ntests):
            self.configuration.make_config(packet_size, duration, protocol, package_count)
            

    def clean_tests(self):
        self.configuration.clean_tests()
       
    def run_server(self):
        run_iperf3_server()

    def run_tests(self, server):    
        with open('backend/configuration/tests.json', 'r') as file:
            data = json.load(file)

        results = []

        for index, test in enumerate(data['tests'], start=0):
            test_result = {}

            if test.get("protocol", 0):
                test_result["bandwidth"] = self.execute_iperf3(server, test)
                

            if test.get("package-count", 0):
                test_result["latency"] = self.execute_ping(server, test)

            results.append(test_result)
        
        print({"results": results})
        
        return {"results": results}


if __name__ == "__main__":
    executor = Executor()
    executor.mainMenu()
    