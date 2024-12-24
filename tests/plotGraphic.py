import matplotlib.pyplot as plt
import os
import json

def plot_packet_packetSize(path, date):
    x = []
    y = []
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        with open(filePath, 'r') as fl:
            data = json.load(fl)
        x.append(data["parameters"]["packet_size"])
        y.append(data["results"]["lost_packets"])
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2, linestyle='-', marker='o')
    plt.title('Lost Packets/Packet Size')
    plt.xlabel('Packet Size', fontsize=12)  # Rótulo do eixo X
    plt.ylabel('Lost Packets', fontsize=12)  # Rótulo do eixo Y
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    base_dir = "./results"
    plot_dir = os.path.join(base_dir, f"plots_{date}")
    os.makedirs(plot_dir, exist_ok=True)
    output_file = os.path.join(plot_dir, f"packetxpsize_plot.jpg")
    plt.savefig(output_file)
    plt.show()


if __name__ == "__main__":
    plot_packet_packetSize()