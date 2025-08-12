import matplotlib.pyplot as plt  # type: ignore
import matplotlib.ticker as mticker # type: ignore
from pathlib import Path
from .statistics import Statistician, StatisticsReport

class StatisticsPlot:
    def __init__(self):
        self.statistician = Statistician()
        self.output_dir = Path("plots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_report_plot(self, report: StatisticsReport) -> str:
        # Carrega os dados da coluna
        try:
            data = [row[report.column_name] for row in self.statistician._full_dataset]
        except Exception as e:
            print(f"❌ Erro ao acessar dados da coluna '{report.column_name}': {e}")
            return ""

        if not data:
            print("⚠️ Nenhum dado para plotar.")
            return ""

        # Define nome base do arquivo
        base_name = f"hist_{report.column_name}"
        existing_files = list(self.output_dir.glob(f"{base_name}_*.png"))
        plot_id = len(existing_files) + 1
        output_path = self.output_dir / f"{base_name}_{plot_id}.png"

        # Criação do histograma
        plt.figure(figsize=(10, 6))

        # Se todos os valores forem iguais, use 1 bin apenas
        unique_values = set(data)
        bins = 1 if len(unique_values) == 1 else 10
        plt.hist(data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)

        # Linhas verticais para estatísticas
        plt.axvline(report.mean, color='red', linestyle='--', label=f'Média: {report.mean:.3f}')
        plt.axvline(report.median, color='green', linestyle='--', label=f'Mediana: {report.median:.3f}')
        plt.axvline(report.quartiles['Q1'], color='orange', linestyle=':', label=f'Q1: {report.quartiles["Q1"]:.3f}')
        plt.axvline(report.quartiles['Q3'], color='purple', linestyle=':', label=f'Q3: {report.quartiles["Q3"]:.3f}')
        plt.axvline(report.mean + report.std_dev, color='red', linestyle=':', label=f'+1σ: {(report.mean + report.std_dev):.3f}')
        plt.axvline(report.mean - report.std_dev, color='red', linestyle=':', label=f'-1σ: {(report.mean - report.std_dev):.3f}')

        # Configurações de formatação do eixo X
        ax = plt.gca()
        x_max = max(data)
        if x_max < 10:
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.3f}'))
        else:
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

        # Demais configurações
        plt.title(f"Histograma - {report.column_name}")
        plt.xlabel(report.column_name)
        plt.ylabel("Frequência")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Salva o gráfico
        try:
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Histograma salvo em: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"❌ Erro ao salvar o gráfico: {e}")
            return ""
