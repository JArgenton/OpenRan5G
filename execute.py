import json
import os
from tests.iperfr3_test import run_iperf3
from tests.ping_test import run_ping
from configuration.configuration import Configuration
from plotting.plotGraphic import plot_packet_packetSize

class Executor():
    def __init__(self):
        self.configuration = Configuration.getObject()

    def save_tests(self, results):
        ping = int(self.configuration.ping_index) #1
        iperf = int(self.configuration.iperf_index) #0

        file_path = self.build_save_file()
        iperf_data = results[iperf]
        ping_data = results[ping]

        combined_data = {
            "iperf_data" : iperf_data,
            "ping_data" : ping_data
        }
        with open(file_path, "r+") as file:
            geral_data = json.load(file)

            geral_data["tests"].append(combined_data)
            file.seek(0) #volta ao inicio do arquivo, precisa porque o r+ inicia a escrita do fim do arquivo, e nos precisamos reescrever tudo oss!
            json.dump(geral_data, file, indent=4)

    def run_tests(self, server, iperf3_config, ping_config):
        result_iperf3 = run_iperf3(server, iperf3_config["duration"], iperf3_config["packet-size"], iperf3_config["protocol"])
        result_ping = run_ping(server, ping_config["package-count"])

        results = [result_iperf3, result_ping]
        return results 

    def build_save_file(self):
        date = self.configuration.get_formated_date()
        output_file = self.configuration.output_file

        os.makedirs(output_file, exist_ok=True)

        file_path = (f"{output_file}/{date}")

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({"tests": []}, file, indent=4)
            
        return file_path

    def insert_tests(self, aux):
        inserir_novo_teste = aux
        while inserir_novo_teste == 's' or inserir_novo_teste == 'S':

            #CONFIGURAR TESTE
            packet_size = int(input("packet size: "))
            duration = int(input("duration: "))
            protocol = str(input("protocol: "))
            package_count = int(input("package count: "))

            print("\n teste inserido")

            self.configuration.make_config(packet_size, duration, protocol, package_count)
            inserir_novo_teste = str(input("Deseja inserir um novo teste? \n S \n N \n"))

    def build_tests(self):
        ip = str(input("Insira o ip: "))

        inserir_novo_teste = str(input("Deseja inserir um novo teste? \n S \n N \n"))
        if inserir_novo_teste == 's' or inserir_novo_teste == 'S':
            with open(self.configuration.parameters_path, 'w') as file:
                json.dump(self.configuration.std_test_file, file, indent=4)

            self.insert_tests(inserir_novo_teste) #essa é a primeira vez que eu senti q um do while ia ser util, nao sei se isso existe em python e o gepete morreu
        return ip
    
    def exec(self):
        
        server = self.build_tests()

        with open('configuration/tests.json', 'r') as file:
            data = json.load(file)

        for index, test in enumerate(data['tests'], start=0):
            
            iperf3 = test['iperf3']
            ping = test['ping']

            results = self.run_tests(server, iperf3, ping)

            self.save_tests(results)

        #plot_packet_packetSize(iperf3_dir, date)

if __name__ == "__main__":
    executor = Executor()
    executor.exec()