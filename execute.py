import json
import os
from tests.iperfr3_test import run_iperf3
from tests.ping_test import run_ping
from configuration.configuration import Configuration
from plotting.plotGraphic import plot_packet_packetSize
from configuration.make_config import make_config

class Executor():
    def __init__(self):
        self.configuration = Configuration.getObject()

    def save_tests(self, index, results):
        ping = int(self.configuration.ping_index) #1
        iperf = int(self.configuration.iperf_index) #0

        result_iperf3 = results[iperf]
        result_ping = results[ping]

        dirs = self.build_dirs()

        output_iperf3_file = (f"{dirs[iperf]}/{index}")
        output_ping_file = (f"{dirs[ping]}/{index}")
        
        with open(output_iperf3_file, "w") as file:
            json.dump(result_iperf3, file, indent=4)

        with open(output_ping_file, "w") as file:
            json.dump(result_ping, file, indent=4)

    def run_tests(self, server, iperf3_config, ping_config):
        result_iperf3 = run_iperf3(server, iperf3_config["duration"], iperf3_config["packet-size"], iperf3_config["protocol"])
        result_ping = run_ping(server, ping_config["package-count"])

        results = [result_iperf3, result_ping]
        return results 

    def build_dirs(self):
        date = self.configuration.get_formated_date()
        iperf_results = (f"{self.configuration.output_iperf}_{date}")
        ping_results = (f"{self.configuration.output_ping}_{date}")

        os.makedirs(iperf_results, exist_ok=True)
        os.makedirs(ping_results, exist_ok=True)

        return iperf_results, ping_results

    def exec(self):
        ip = input("Insira o ip: ")
        num_packet = int(input("Insira a quantidade de pacotes do teste: "))
        make_config(ip, num_packet)

        with open('configuration/tests.json', 'r') as file:
            data = json.load(file)

        server = data["server"]

        for index, test in enumerate(data['test'], start=0):
            
            iperf3 = test['iperf3']
            ping = test['ping']

            results = self.run_tests(server, iperf3, ping)

            self.save_tests(index, results)

        #plot_packet_packetSize(iperf3_dir, date)

if __name__ == "__main__":
    executor = Executor()
    executor.exec()