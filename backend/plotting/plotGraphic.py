import json
import matplotlib.pyplot as plt # type: ignore
from ..programer.results import Result
from datetime import datetime
import os

class Plotter:
    def __init__(self):
        self.xParam = []
        self.yParam = []


    def getValuesByTime(self, server, xParam: str, yParam: str, date: list[str]):
        self.xParam = []
        self.yParam = []
        date[0] += " 00:00:00"
        date[1] += " 23:59:59"
        where = f"WHERE SERVER = '{server}' AND TIMESTAMP_RESULT BETWEEN '{date[0]}' AND '{date[1]}'"
        select = f'{xParam}, {yParam}'
        
        data = Result.database.get_results_params(where, select)
        print(data)
        
        for dt in data:
                if dt[0] is not None and dt[1] is not None:
                    if dt[0] in self.xParam:
                        index = self.xParam.index(dt[0])
                        self.yParam[index][0] += dt[1]
                        self.yParam[index][1] += 1
                    else:
                            self.xParam.append(dt[0])
                            self.yParam.append([dt[1], 1])

                        
        for i in range(0, len(self.yParam)):
            y = self.yParam[i]
            self.yParam[i] = y[0]/y[1]
    
    def generateGraphic(self, xLabel="X", yLabel="Y", title="Gráfico") -> str | None:
        if not self.xParam or not self.yParam:
            print("⚠️ Dados insuficientes para gerar gráfico.")
            return None

        # Garante que a pasta 'plots/' existe
        os.makedirs("plots", exist_ok=True)

        # Gera nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = "plots/"
        filename = f"{path}grafico_{timestamp}.png"

        # Gera o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(self.xParam, self.yParam, marker='o', linestyle='-', color='blue')
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        #plt.show()
        plt.close()
        return filename
    

    
