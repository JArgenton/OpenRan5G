import json
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self):
        self.x_label = ""
        self.y_label = ""
        self.color = "blue"
        self.line_type = "-"
        self.x_path = ""
        self.y_path = ""

    def _get_nested_value(self, data, path):
        if not path:
            return None
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def get_plotting_data(self, data_file='data.json'):
        x_data = []
        y_data = []
        with open(data_file, 'r') as f:
            data = json.load(f)
        tests = data.get('tests', [])
        for test in tests:
            x_val = self._get_nested_value(test, self.x_path)
            y_val = self._get_nested_value(test, self.y_path)
            if x_val is not None and y_val is not None:
                x_data.append(x_val)
                y_data.append(y_val)
        sorted_pairs = sorted(zip(x_data, y_data), key=lambda pair: pair[0])
        x_sorted = [x for x, y in sorted_pairs]
        y_sorted = [y for x, y in sorted_pairs]
        return x_sorted, y_sorted

    def create_graph(self, x_data, y_data):
        plt.figure()
        plt.plot(x_data, y_data, color=self.color, linestyle=self.line_type)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(f"{self.y_label} vs {self.x_label}")
        plt.grid(True)

    def plot_graph(self):
        plt.show()

    def save_graph(self, filename):
        plt.savefig(filename)
        plt.close()

    def save_plotting_config(self, config_file):
        config = {
            "x_path": self.x_path,
            "y_path": self.y_path,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "color": self.color,
            "line_type": self.line_type
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def load_graph(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.x_path = config.get('x_path', '')
        self.y_path = config.get('y_path', '')
        self.x_label = config.get('x_label', '')
        self.y_label = config.get('y_label', '')
        self.color = config.get('color', 'blue')
        self.line_type = config.get('line_type', '-')


if __name__ == '__main__':
    plotter = Plotter()
    data_path = '/home/argenton/Documentos/OpenRan5g/OpenRan5G/backend/results/07-05_17-31'
    
    # Lista de configurações para testar
    configs = [
        ('backend/plotting/JitterXbps.json', 'throughput_vs_Jitter.png'),
        ('backend/plotting/pkg_sizeXavg_lat.json', 'Latência_vs_Packet_Size.png'),
        ('backend/plotting/pkg_sizeXJitter.json', 'Jitter vs Packet Size.png'),
        ('backend/plotting/pkg_sizeXbps.json', 'lhroughput vs Packet Size.png'),
        ('backend/plotting/pkg_sizeXLoss.json', 'Packet Loss vs Packet Size.png')
    ]

    for config_file, output_file in configs:
        plotter.load_graph(config_file)
        x_data, y_data = plotter.get_plotting_data(data_path)
        plotter.create_graph(x_data, y_data)
        plotter.save_graph(output_file)
        print(f"Gráfico salvo como: {output_file}")
