import json
import matplotlib.pyplot as plt # type: ignore
from ..programer.results import Result
from datetime import datetime
import os
from ..programer.routine import Routine

class Plotter:
    def __init__(self):
        self.xParam = []
        self.yParam = []


    def getValuesByTime(self, server, xParam: str, yParam: str, date: list[str]):
        self.xParam = []
        self.yParam = []
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

    def getValuesByRoutine(self, server: str, routineName: str, yParam: str):
        self.xParam = []
        self.yParam = []
        r_id = Routine.getRoutineID(routineName)
        where = f"WHERE ROUTINE_ID = '{r_id}'"
        select = f"{yParam}"
        data = Result.database.get_results_params(where, select)
        counter = 0
        for dt in data:
            self.xParam.append(counter)
            counter += 1
            self.yParam.append(dt[0])
    
    def generateGraphic(self, xLabel="X", yLabel="Y", title="Gráfico", mode = 0) -> str | None:
        if not self.yParam:
            print("⚠️ Dados insuficientes para gerar gráfico.")
            return None

        os.makedirs("plots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = "plots/"
        filename = f"{path}grafico_{timestamp}.png"

        plt.figure(figsize=(10, 6))
        print(mode)
        if mode == 0:
            if not self.xParam:
                self.xParam = list(range(len(self.yParam)))
            plt.plot(self.xParam, self.yParam, marker='o', linestyle='-', color='blue')
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)
        elif mode == 1:
            indices = list(range(len(self.yParam)))
            bars = plt.bar(indices, self.yParam, color='royalblue', alpha=0.85)

            plt.xlabel("Execução", fontsize=12)
            plt.ylabel(yLabel, fontsize=12)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xticks(indices)  # garante que os rótulos X sejam inteiros

            # Adiciona os valores no topo das barras
            for i, bar in enumerate(bars):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2.0, height,
                        f'{height:.3f}', ha='center', va='bottom', fontsize=10)

        plt.title(title)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

        return filename

    

    

    
