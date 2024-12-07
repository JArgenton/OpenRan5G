import json
import os
from iperfr3_test import run_iperf3
from ping_test import run_ping
from configuration import Configuration
if __name__ == "__main__":
    with open('config.json', 'r') as file:
        data = json.load(file)
    output_dir = "../results" #dir de saida

    server = data["configuration"]["server"]
    for index, test in enumerate(data['configuration']['test'], start=0):
        iperf3 = test['iperf3']
        ping = test['ping']


        result_iperf3 =  run_iperf3(server, iperf3["duration"], iperf3["packet-size"], iperf3["protocol"])
        output_iperf3_file = os.path.join(output_dir, f"iperf3_results_{str(index)}.json")

        result_ping =  run_ping(server, ping["package-count"])
        output_ping_file = os.path.join(output_dir, f"ping_results_{str(index)}.json")


            
        
