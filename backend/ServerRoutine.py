import os
import time
from .Executor import Executor

# Atualiza o IP público no DuckDNS
def update_dns():
    domain = "openranserver"  # SEM .duckdns.org
    token = "4703b88f-f4d8-4895-a6c4-153536358bd4"
    print("🔄 Atualizando IP no DuckDNS...")
    os.system(f'curl -s "https://www.duckdns.org/update?domains={domain}&token={token}&ip="')

    

# Encerra o subprocesso do iperf3


if __name__ == "__main__":
    executor = Executor()
    update_dns()
    process = executor.run_server()
    print("⏳ Servidor ativo por 8 minutos...")
    time.sleep(8 * 60)
    executor.kill_server(process)
    print("✅ Finalizado.")
