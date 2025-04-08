import json
import os
from tests.iperfr3_test import run_iperf3
from tests.ping_test import run_ping
from configuration.configuration import Configuration
from plotting.plotGraphic import plot_packet_packetSize
from database.teste_bd import Database

class Executor():
    def __init__(self):
        self.configuration = Configuration.getObject()
        self.database = Database.get_object()

    def save_tests(self, results, output_file):
        ping = int(self.configuration.ping_index) #1
        iperf = int(self.configuration.iperf_index) #0

        combined_data = {
            "iperf_data" : results[iperf],
            "ping_data" : results[ping]
        }

        with open(output_file, "r+") as file:
            geral_data = json.load(file)

            geral_data["tests"].append(combined_data)
            file.seek(0) #volta ao inicio do arquivo, precisa porque o r+ inicia a escrita do fim do arquivo, e nos precisamos reescrever tudo oss!
            json.dump(geral_data, file, indent=4)

    def run_tests(self, server, test):

        result_iperf3 = run_iperf3(server, test["duration"], test["packet-size"], test["protocol"])
        result_ping = run_ping(server, test["package-count"])

        results = [result_iperf3, result_ping]
        return results 

    def build_save_file(self):
        date = self.configuration.get_formated_date()
        output_file = self.configuration.output_file

        os.makedirs(output_file, exist_ok=True)

        file_path = (f"{output_file}/{date}")

        with open(file_path, "w") as file:
            json.dump({"tests": []}, file, indent=4)
            
        return file_path    
    
    def exec(self):
        
        server = self.build_tests()
        output_file = self.build_save_file()
        
        with open('configuration/tests.json', 'r') as file:
            data = json.load(file)

        for index, test in enumerate(data['tests'], start=0):

            results = self.run_tests(server, test)

            self.save_tests(results, output_file)

        self.database.add_tests_to_database(output_file)
        self.database.print_all_data()
        #plot_packet_packetSize(iperf3_dir, date)

if __name__ == "__main__":
    executor = Executor()
    executor.exec()