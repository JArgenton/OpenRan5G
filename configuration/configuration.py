import json
from datetime import datetime

class Configuration:
    """Fiz meio de sacanagem, pois este nao faz muito sentido pensando em enviar os comando pelo terminal.
        Mesmo assim este sera util pois facilita o codigo, e eu estava pensando melhor quanto a cascar os 
        parametros via terminal, nao sera nada eficiente e escalavel, desse jeito fica mais facil realizar 
        varios testes em sequencia."""
    _instance = None 

    def __init__(self):
        self.date = None
        self.parameters_path = None
        self.output_iperf = None
        self.output_ping = None
        self.ping_index = None
        self.iperf_index = None

    def get_formated_date(self):
        if self.date == None:
            current_time = datetime.now()
            formatted_date = current_time.strftime("%d-%m")  
            formatted_time = current_time.strftime("%H-%M") 
            self.date = (f"{formatted_date}_{formatted_time}")
        return self.date


    @staticmethod
    def loadFromJson():
        with open('configuration/config.json', 'r') as file:
          data =  json.load(file)

        return data

    def getObject():
        if Configuration._instance is None:
            Configuration._instance = Configuration()
            data = Configuration.loadFromJson()

            instance = Configuration._instance
            instance.parameters_path = data["configuration"]["tests"]["parameters-path"]
            instance.output_iperf = data["configuration"]["tests"]["output-iperf"]
            instance.output_ping = data["configuration"]["tests"]["output-ping"]
            instance.ping_index = data["configuration"]["tests"]["ping-index"]
            instance.iperf_index = data["configuration"]["tests"]["iperf-index"]
           
        return Configuration._instance  