import unittest
import math
from typing import List, Tuple, Dict, Any, Union
from dataclasses import dataclass

# ===============================================================================================
#  CLASSE Statistician E StatisticsReport, usadas em conjunto para gerar e guardar analise de re
#  sultados de testes
# ===============================================================================================

@dataclass(frozen=True)
class StatisticsReport:
    column_name: str
    count: int
    mean: float
    median: float
    std_dev: float
    variance: float
    quartiles: dict

    def __repr__(self) -> str:
        return (f"--- Relatório para '{self.column_name}' ---\n"
                f"  Contagem: {self.count}\n  Média:    {self.mean:.2f}\n"
                f"  Mediana:  {self.median:.2f}\n  Desv. Padrão: {self.std_dev:.2f}\n"
                f"  Quartis:  Q1={self.quartiles['Q1']:.2f}, Q2={self.quartiles['Q2']:.2f}, Q3={self.quartiles['Q3']:.2f}")

class Statistician:
    _FIXED_HEADERS = ('RESULT_ID', 'ROUTINE_ID', 'TEST_ID', 'TIMESTAMP_RESULT', 'SERVER', 'MIN_LATENCY', 'AVG_LATENCY', 'MAX_LATENCY', 'LOST_PACKETS', 'LOST_PERCENT', 'BITS_PER_SECOND', 'BYTES_TRANSFERED', 'JITTER', 'RETRANSMITS')
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._reset_state()
    def _reset_state(self):
        self._full_dataset: List[Dict[str, Any]] = []
        self._data_loaded: bool = False
    def load_data(self, data: List[Tuple]):
        self._reset_state()
        if not data: raise ValueError("A lista de dados não pode ser vazia.")
        num_headers = len(self._FIXED_HEADERS)
        if len(data[0]) != num_headers: raise ValueError(f"O número de colunas nos dados ({len(data[0])}) não corresponde ao número de cabeçalhos fixos ({num_headers}).")
        self._full_dataset = [dict(zip(self._FIXED_HEADERS, row)) for row in data]
        self._data_loaded = True
    def analyze(self, column_name: str) -> StatisticsReport:
        if not self._data_loaded: raise RuntimeError("Dados não foram carregados.")
        if column_name not in self._FIXED_HEADERS: raise ValueError(f"Nome de coluna '{column_name}' não encontrado.")
        target_data = [row[column_name] for row in self._full_dataset]
        if not all(isinstance(val, (int, float)) for val in target_data): raise TypeError(f"A coluna '{column_name}' contém dados não-numéricos.")
        sorted_data = sorted(target_data)
        count = len(sorted_data)
        if count == 0: return StatisticsReport(column_name, 0, 0, 0, 0, 0, {})
        mean = sum(target_data) / count
        mid_index = count // 2
        if count % 2 == 0: lower_half, upper_half = sorted_data[:mid_index], sorted_data[mid_index:]
        else: lower_half, upper_half = sorted_data[:mid_index], sorted_data[mid_index+1:]
        median = self._calculate_median_from_list(sorted_data)
        quartiles = {"Q1": self._calculate_median_from_list(lower_half), "Q2": median, "Q3": self._calculate_median_from_list(upper_half)}
        variance = sum((x - mean) ** 2 for x in target_data) / count
        std_dev = math.sqrt(variance)
        return StatisticsReport(column_name=column_name, count=count, mean=mean, median=median, std_dev=std_dev, variance=variance, quartiles=quartiles)
    def _calculate_median_from_list(self, data_list: list) -> float:
        n = len(data_list)
        if n == 0: return 0
        mid_index = n // 2
        return data_list[mid_index] if n % 2 == 1 else (data_list[mid_index - 1] + data_list[mid_index]) / 2.0
    def get_available_columns(self) -> Tuple[str, ...]:
        return self._FIXED_HEADERS


# ===============================================================================================
#                                   --- TESTE unittest ---
# ===============================================================================================
class TestStatistician(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Este método é executado UMA VEZ antes de todos os testes.
        É o para preparar os dados e carregar a classe.
        """
        print("\n--- Configurando ambiente de teste (setUpClass) ---")
        cls.sample_data = [
            (1, 1, 1, '2025-07-09 17:00:00', 'server_a', 10.1, 12.5, 15.3, 0, 0.0, 94.0e6, 11.75e6, 0.01, 10),
            (2, 1, 1, '2025-07-09 17:01:00', 'server_a', 9.8,  11.9, 14.8, 1, 0.1, 93.5e6, 11.68e6, 0.02, 15),
            (3, 1, 1, '2025-07-09 17:02:00', 'server_a', 10.5, 13.1, 16.0, 0, 0.0, 94.2e6, 11.77e6, 0.01, 8),
            (4, 1, 1, '2025-07-09 17:03:00', 'server_a', 11.2, 14.0, 18.1, 0, 0.0, 92.0e6, 11.50e6, 0.03, 25),
            (5, 1, 1, '2025-07-09 17:04:00', 'server_a', 10.3, 12.8, 15.5, 0, 0.0, 93.8e6, 11.72e6, 0.01, 12)
        ]
        
        cls.analisador = Statistician()
        cls.analisador.load_data(cls.sample_data)

    def test_singleton_instance(self):
        """Verifica se a classe é de fato um Singleton."""
        print("Executando: test_singleton_instance")
        instance1 = Statistician()
        self.assertIs(instance1, self.analisador, "A instância deveria ser a mesma já criada.")

    def test_data_loading(self):
        """Verifica se os dados foram carregados corretamente."""
        print("Executando: test_data_loading")
        # Verifica se o número de linhas carregadas está correto
        self.assertEqual(len(self.analisador._full_dataset), 5)
        # Verifica se os cabeçalhos estão corretos
        self.assertEqual(self.analisador.get_available_columns(), Statistician._FIXED_HEADERS)
        
    def test_analysis_results(self):
        """Verifica se os cálculos estatísticos para uma coluna estão corretos."""
        print("Executando: test_analysis_results (AVG_LATENCY)")
        report = self.analisador.analyze('AVG_LATENCY')
        
        # Verifica se o objeto de retorno é do tipo correto
        self.assertIsInstance(report, StatisticsReport)
        
        # Verifica os valores calculados
        self.assertEqual(report.count, 5)
        self.assertAlmostEqual(report.mean, 12.86, places=2)
        self.assertEqual(report.median, 12.8)
        self.assertAlmostEqual(report.std_dev, 0.69, places=2)

    def test_error_on_non_numeric_column(self):
        """Verifica se um TypeError é levantado ao analisar uma coluna de texto."""
        print("Executando: test_error_on_non_numeric_column")
        # O 'with' verifica se o erro esperado realmente acontece
        with self.assertRaises(TypeError):
            self.analisador.analyze('SERVER')

    def test_error_on_non_existent_column(self):
        """Verifica se um ValueError é levantado ao analisar uma coluna que não existe."""
        print("Executando: test_error_on_non_existent_column")
        with self.assertRaises(ValueError):
            self.analisador.analyze('NON_EXISTENT_COLUMN')

# --- Ponto de entrada para executar os testes ---
if __name__ == '__main__':
    unittest.main(verbosity=2)
