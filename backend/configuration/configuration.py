import json
from datetime import datetime

class Configuration_:
    """Fiz meio de sacanagem, pois este nao faz muito sentido pensando em enviar os comando pelo terminal.
        Mesmo assim este sera util pois facilita o codigo, e eu estava pensando melhor quanto a cascar os 
        parametros via terminal, nao sera nada eficiente e escalavel, desse jeito fica mais facil realizar 
        varios testes em sequencia."""
    _instance = None 

    def __init__(self):
        self.date = None
        self.parameters_path = None
        self.output_file = None
        self.ping_index = None
        self.iperf_index = None
        self.std_test_file = None

    def get_formated_date(self):
        if self.date == None:
            current_time = datetime.now()
            formatted_date = current_time.strftime("%d-%m")  
            formatted_time = current_time.strftime("%H-%M") 
            self.date = (f"{formatted_date}_{formatted_time}")
        return self.date

    def clean_tests(self):
        target = self.parameters_path
        with open(target, 'w') as file:
            json.dump({"tests": []}, file, indent=4)  
    
    def make_config(self, packet_size, duration, protocol = "none", packet_count = -1):
        if packet_count == -1 and protocol == "":
            print('Entrada de teste inválida')
            return
        
        if(packet_count == -1):
            config = {
                "packet-size":packet_size ,
                "duration": duration,
                "protocol": protocol.upper()      
            }
        elif protocol == "none":
            config = {
                "package-count": packet_count    
            }
        else:
            config = {
                "packet-size":packet_size,
                "duration": duration,
                "protocol": protocol.upper(),
                "package-count": packet_count       
            }

        output_file = self.parameters_path
        
        with open(output_file, "r+") as file:
            tests = json.load(file)
            tests["tests"].append(config)            
            file.seek(0) #volta ao inicio do arquivo, precisa porque o r+ inicia a escrita do fim do arquivo, e nos precisamos reescrever tudo oss!
            json.dump(tests, file, indent=4)


    @staticmethod
    def loadFromJson():
        with open('backend/configuration/config.json', 'r') as file:
          data =  json.load(file)
        return data 

    @staticmethod
    def getObject():
        if Configuration_._instance is None:
            Configuration_._instance = Configuration_()
            data = Configuration_.loadFromJson()

            instance = Configuration_._instance
            instance.parameters_path = data["configuration"]["tests"]["parameters-path"]
            instance.output_file= data["configuration"]["tests"]["output-file"]
            instance.ping_index = data["configuration"]["tests"]["ping-index"]
            instance.iperf_index = data["configuration"]["tests"]["iperf-index"]
            instance.std_test_file = data["configuration"]["std-test-file"]
           
        return Configuration_._instance  
    
