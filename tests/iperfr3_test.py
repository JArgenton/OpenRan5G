import subprocess
import json
from datetime import datetime, timezone
import os

def run_iperf3(server, duration,size=512, protocol="TCP", port=5201):
    """
    Executa o iperf3 e salva os resultados em JSON.
        server: IP ou hostname do servidor.
        duration: Duracao do teste em segundos.
        protocol: Protocolo a ser utilizado (TCP ou UDP).
        port: Porta a ser usada no servidor.
    """

    command = ["iperf3", "-c", server, "-p", str(port), "-t", str(duration), "-l" ,str(size),"--json"]

    if protocol.upper() == "UDP": #verifica se estamos medindo udp e add a flag necessaria
        command.append("--udp")
    
    result = subprocess.run(command, capture_output=True, text=True) # igual ao do ping

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao executar iperf3: {result.stderr}") # igual ao do ping
    
    output = json.loads(result.stdout) # iperf retorna direto em json

    return iperf3_output(output, protocol)


def iperf3_output(data, protocol):

    metrics = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_type": "bandwidth",
        "protocol": protocol,
        "parameters": {
            "server": data["start"]["connected"][0]["remote_host"],
            "duration_seconds": data["start"]["test_start"]["duration"],
            "packet_size": data["start"]["test_start"]["blksize"]
        },

        "results": {}
    }
    
    if protocol.upper() == "TCP": #dados especificos do TCP
        metrics["results"] = {
            "bits_per_second": data["end"]["sum_received"]["bits_per_second"],
            "retransmits": data["end"]["sum_received"].get("retransmits", 0),
            "bytes_transferred": data["end"]["sum_received"]["bytes"]
        }

    elif protocol.upper() == "UDP": #dados especificos do UDP
        stream = data["end"]["streams"][0]["udp"]

        metrics["results"] = {
            "bits_per_second": stream["bits_per_second"],
            "lost_packets": stream["lost_packets"],
            "lost_percent": stream["lost_percent"],
            "bytes_transferred": stream["bytes"],
            "Jitter": stream["jitter_ms"],
            "packets": stream["packets"]
        }
    
    return metrics


if __name__ == "__main__":
    try:
        server = "10.181.1.42"
        duration = 10
        protocol = "UDP"  # TCP
        size = 512*3
        
        result = run_iperf3(server, duration,size, protocol=protocol)

        output_dir = "../results" #dir de saida
        output_file = os.path.join(output_dir, "iperf3_results.json")
        
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, "w") as file:
            json.dump(result, file, indent=4)

    except Exception as e:
        print(f"Erro: {e}")
