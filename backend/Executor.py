import json
import os
from .tests.ping_test import Ping
from .tests.iperfr3_test import Iperf
from .configuration.configuration import Configuration_
from .database.resultados import ResultadosDAO

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
        self.database = ResultadosDAO()
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
    def load_data(self, timestamp="", routine_id=-1):
        results = self.database.fetch_all()
        formated_results = []
        for result in results:
            print(result)
            self.format_result_json(result)
            formated_results.append(result)
        return {"results" : formated_results}
        
    def format_result_json(self, row: tuple) -> dict:
        (
            _,              # RESULT_ID (ignorado)
            _,              # TEST_ID (ignorado)
            timestamp,      # TIMESTAMP_RESULT
            min_latency,    # MIN_LATENCY
            avg_latency,    # AVG_LATENCY
            max_latency,    # MAX_LATENCY
            lost_packets,   # LOST_PACKETS
            lost_percent,   # LOST_PERCENT
            bits_per_second,# BITS_PER_SECOND
            bytes_transferred, # BYTES_TRANSFERRED
            jitter,         # JITTER
            retransmits     # RETRANSMITS
        ) = row

        result: dict = {}

        # Monta latency (ping_data)
        if min_latency is not None and avg_latency is not None and max_latency is not None:
            result["latency"] = {
                "timestamp": timestamp,
                "test_type": "latency",
                "tool": "ping",
                "parameters": {
                    "target": "",  # preencha se tiver essa info
                    "packet_count": 0  # preencha se tiver essa info
                },
                "results": {
                    "min_latency_ms": min_latency,
                    "avg_latency_ms": avg_latency,
                    "max_latency_ms": max_latency
                }
            }

        # Monta bandwidth (iperf_data)
        if bits_per_second is not None and bytes_transferred is not None:
            bandwidth = {
                "timestamp": timestamp,
                "test_type": "bandwidth",
                "parameters": {
                    "server": "",  # preencha se tiver essa info
                    "duration_seconds": 0,  # preencha se tiver essa info
                    "packet_size": 0  # preencha se tiver essa info
                },
                "results": {}
            }

            if lost_packets is not None and lost_percent is not None and jitter is not None:
                bandwidth["protocol"] = "udp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "lost_packets": lost_packets,
                    "lost_percent": lost_percent,
                    "bytes_transferred": bytes_transferred,
                    "Jitter": jitter,
                    "packets": 0  # preencha se tiver essa info
                }
            elif retransmits is not None:
                bandwidth["protocol"] = "tcp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "retransmits": retransmits,
                    "bytes_transferred": bytes_transferred
                }

            result["bandwidth"] = bandwidth

        return result


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
            self.database.insert(formated_results)

            results.append(test_result)

        #print({"results": results})
        
        return {"results": results}
   

if __name__ == "__main__":
    executor = Executor()
    executor.mainMenu()
    