import json
import os
from iperfr3_test import run_iperf3
from ping_test import run_ping
from configuration import Configuration
from datetime import datetime

def save_tests(index, results, iperf3_dir, ping_dir):

    os.makedirs(iperf3_dir, exist_ok=True)
    os.makedirs(ping_dir, exist_ok=True)

    output_iperf3_file = os.path.join(iperf3_dir, f"iperf3_result_{index}.json")
    output_ping_file = os.path.join(ping_dir, f"ping_result_{index}.json")

    result_iperf3 = results[0]
    result_ping = results[1]

    with open(output_iperf3_file, "w") as file:
        json.dump(result_iperf3, file, indent=4)

    with open(output_ping_file, "w") as file:
        json.dump(result_ping, file, indent=4)


def run_tests(server, iperf3_config, ping_config):
    result_iperf3 = run_iperf3(server, iperf3_config["duration"], iperf3_config["packet-size"], iperf3_config["protocol"])
    result_ping = run_ping(server, ping_config["package-count"])

    results = [result_iperf3, result_ping]
    return results 

def get_formatted_date():
    current_time = datetime.now()
    formatted_date = current_time.strftime("%d-%m")  
    formatted_time = current_time.strftime("%H-%M") 
    return (f"{formatted_date}_ {formatted_time}")

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        data = json.load(file)
    
    output_dir = "../results"
    os.makedirs(output_dir, exist_ok=True)

    date = get_formatted_date()

    iperf3_dir = os.path.join(output_dir, f"iperf3_results_{date}")
    ping_dir = os.path.join(output_dir, f"ping_results_{date}")

    server = data["configuration"]["server"]

    for index, test in enumerate(data['configuration']['test'], start=0):
        
        iperf3 = test['iperf3']
        ping = test['ping']

        results = run_tests(index, server, iperf3, ping)

        save_tests(index, results, iperf3_dir, ping_dir)

        





