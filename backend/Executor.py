import json
import os
from .tests.ping_test import Ping
from .tests.iperfr3_test import Iperf
from .configuration.configuration import Configuration_
from .database.resultados import ResultadosDAO
from .database.testes_de_rede import TestesDeRedeDAO
from .programer.routine import Routine
from .programer.network_test import Test

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
        self.databaser = ResultadosDAO()
        self.databaset = TestesDeRedeDAO()
        
        
    
    def execute_iperf3(self, server, test):
        return Iperf.run_iperf3(server, test["duration"], test["packet-size"], test["protocol"])
    
    def execute_ping(self, server, test):
        return Ping.run_ping(server, test["package-count"])
    
    def insert_tests(self, packet_size: int, duration: int, protocol: str = "none", ntests: int = 1, package_count: int = -1):
        if ntests < 0:
            print('Número inválido de testes')
        for i in range(0, ntests):
            self.configuration.make_config(packet_size, duration, protocol, package_count)


    def format_save_json(self, result, protocol, ping, id, server: str):
        
        obj = {}
        if protocol == "":
            obj["TIMESTAMP_RESULT"] =  result["latency"]["timestamp"]
        else:
            obj["TIMESTAMP_RESULT"] = result["bandwidth"]["timestamp"]
        obj["TEST_ID"] = id

        obj["SERVER"] = server

        if ping:
            obj["MIN_LATENCY"] = result["latency"]["results"]["min_latency_ms"]
            obj["AVG_LATENCY"] = result["latency"]["results"]["avg_latency_ms"]
            obj["MAX_LATENCY"] = result["latency"]["results"]["max_latency_ms"]
        
        if protocol == "UDP":
            obj["LOST_PACKETS"] = result["bandwidth"]["results"]["lost_packets"]
            obj["LOST_PERCENT"] = result["bandwidth"]["results"]["lost_percent"]
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BYTES_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["JITTER"] = result["bandwidth"]["results"]["Jitter"]

        if protocol == "TCP":
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BYTES_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["RETRANSMITS"] = result["bandwidth"]["results"]["retransmits"]
        
        return obj
    
    def clean_tests(self):
        self.configuration.clean_tests()
       
    def run_server(self):
        Iperf.run_iperf3_server()

    """
    Retorno resultados
        (RESULT_ID, ROUTINE_ID, TIMESTAMP_RESULT, MIN_LATENCY, AVG_LATENCY, MAX_LATENCY, LOST_PACKETS, LOST_PERCENT, BITS_PER_SECOND, BYTES_TRANSFERRED, JITTER, RETRANSMITS)
    """
    def load_data(self):
        results_params = self.databaser.get_results_params()
        formated_results = []
        #print(results_params)
        for result in results_params:
            formatted = self.format_result_json(result)
            if formatted:  
                formated_results.append(formatted)
        return {"results": formated_results}
        
    def format_result_json(self, row: tuple) -> dict:
        (
            _,              # RESULT_ID
            _,              # TEST_ID
            timestamp,      # TIMESTAMP_RESULT
            server,
            min_latency,    # MIN_LATENCY
            avg_latency,    # AVG_LATENCY
            max_latency,    # MAX_LATENCY
            lost_packets,   # LOST_PACKETS
            lost_percent,   # LOST_PERCENT
            bits_per_second,# BITS_PER_SECOND
            bytes_transferred, # BYTES_TRANSFERED
            jitter,         # JITTER
            retransmits,    # RETRANSMITS
            protocol,       # PROTOCOL
            duration,       # DURATION_SECONDS
            packet_size,    # PACKET_SIZE
            packet_count    # PACKET_COUNT
        ) = row

        result: dict = {}

        # Latency (ping)
        if min_latency is not None and avg_latency is not None and max_latency is not None:
            result["latency"] = {
                "timestamp": timestamp,
                "test_type": "latency",
                "tool": "ping",
                "parameters": {
                    "target": server or "",
                    "packet_count": packet_count or 0
                },
                "results": {
                    "min_latency_ms": min_latency,
                    "avg_latency_ms": avg_latency,
                    "max_latency_ms": max_latency
                }
            }

        # Bandwidth (iperf3)
        if bits_per_second is not None and bytes_transferred is not None:
            bandwidth = {
                "timestamp": timestamp,
                "test_type": "bandwidth",
                "parameters": {
                    "server": server or "",
                    "duration_seconds": duration or 0,
                    "packet_size": packet_size or 0
                },
                "results": {}
            }

            if protocol and protocol.upper() == "UDP":
                bandwidth["protocol"] = "udp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "lost_packets": lost_packets or 0,
                    "lost_percent": lost_percent or 0,
                    "bytes_transferred": bytes_transferred,
                    "Jitter": jitter or 0,
                    "packets": packet_count or 0
                }

            elif protocol and protocol.upper() == "TCP":
                bandwidth["protocol"] = "tcp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "retransmits": retransmits or 0,
                    "bytes_transferred": bytes_transferred
                }

            result["bandwidth"] = bandwidth

        #print(result)

        return result

    
    def format_save_test(self, test: dict) -> dict:
        obj = {}

        # Campos diretos (protocolo pode não estar presente)
        obj["PROTOCOL"] = test.get("protocol", None)

        # duration
        try:
            obj["DURATION_SECONDS"] = float(test.get("duration", None))
        except (TypeError, ValueError):
            obj["DURATION_SECONDS"] = None

        # packet-size
        try:
            obj["PACKET_SIZE"] = int(test.get("packet-size", None))
        except (TypeError, ValueError):
            obj["PACKET_SIZE"] = None

        # package-count (ping)
        try:
            obj["PACKET_COUNT"] = int(test.get("package-count", None))
        except (TypeError, ValueError):
            obj["PACKET_COUNT"] = None

        return obj




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

            formated_test = self.format_save_test(test)
            t_id = Test.get_or_create_test_id(formated_test)

            formated_result = self.format_save_json(test_result, protocol, ping, t_id, server)
            
            self.databaser.insert(formated_result)

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
            "packet-size": 256,
            "duration": 5,
            "protocol": "TCP",
            "package-count": 0
        },
        {
            "packet-size": 128,
            "duration" : 10,
            "protocol" : "UDP"
        }
    ]
    formated_tests = [executor.format_save_test(tests[0]), executor.format_save_test(tests[1])]

    routine.create_routine_tests(routine, routine_params, formated_tests)
    print(Routine.R2T.fetch_all())





#(ip, duration, packet_size, packet_count)