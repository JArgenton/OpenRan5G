import json
import os

def make_config(ip, size, tcp=False):
    config = {}
    config["server"] = str(ip)
    config["tests"] = []
    prot = "UDP"
    if tcp == True:
        prot = "TCP"
    for i in range(0, size):
        config["tests"].append({
            "iperf3": {
                "packet-size": str(64 * (2 ** i)),
                "duration": "10",
                "protocol": prot
            },
            "ping": {
                "package-count": 10       
            }
        })
    return config

if __name__ == "__main__":

    output_file = "config.json"
    with open(output_file, "w") as file:
        json.dump(make_config("10.181.1.42", 10), file, indent=4)

