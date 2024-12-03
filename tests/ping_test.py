import subprocess
import json
import datetime
import os


def run_ping(target="8.8.8.8", count=10):
    """
    Executa o comando ping e retorna os resultados.
        target: alvo do ping
        count: numero de pacotes enviados
    """ 
    command = ["ping", "-c", str(count), target] #comando a ser executado
    
    result = subprocess.run(command, capture_output=True, text=True) #executa o comando e captura o resultado

    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, result.stderr) #tratamento de erros (gpt tirou do bolso)

    return ping_output(result.stdout, target, count) #ping nao consegue retornar .json, tem que fazer desse jeito meio porco


def ping_output(output, target, count):

    lines = output.split("\n")
    stats_line = [line for line in lines if "rtt" in line or "min/avg/max" in line]

    if stats_line:

        metrics = stats_line[0].split("=")[-1].strip().split("/")
        min_latency, avg_latency, max_latency = metrics[:3]

        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "test_type": "latency",
            "tool": "ping",
            "parameters": {
                "target": target,
                "packet_count": count
            },
            "results": {
                "min_latency_ms": float(min_latency),
                "avg_latency_ms": float(avg_latency),
                "max_latency_ms": float(max_latency)
                }
            }

if __name__ == "__main__":
    result = run_ping()

    output_dir = "../results"  # Diretório de saída
    output_file = os.path.join(output_dir, "ping_results.json")

    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)

    print(f"Resultados salvos em '{output_file}'.")

