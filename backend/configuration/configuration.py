import json
from datetime import datetime

class Configuration_:
    """Fiz meio de sacanagem, pois este nao faz muito sentido pensando em enviar os comando pelo terminal.
        Mesmo assim este sera util pois facilita o codigo, e eu estava pensando melhor quanto a cascar os 
        parametros via terminal, nao sera nada eficiente e escalavel, desse jeito fica mais facil realizar 
        varios testes em sequencia."""
    _instance = None 

    def __init__(self):
        self.parameters_path = None
        self.output_file = None
        self.ping_index = None
        self.iperf_index = None
        self.std_test_file = None
        self.routines_path = None

    def get_formated_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        
    #===============================================================================#
    
    def clean_tests(self):
        target = self.parameters_path
        with open(target, 'w') as file:
            json.dump({"tests": []}, file, indent=4)  
    
    #===============================================================================#
    
    def set_round_time(hour, minute):
        rounded = ((minute + 14) // 15) * 15

        if rounded == 60:
            minute = 0
            hour = (hour + 1) % 24 
        else:
            minute = rounded

        return hour, minute

    #===============================================================================#

    def clean_routine(self):
        target = self.parameters_path
        with open(target, 'w') as file:
            json.dump({"tests": []}, file, indent=4)  
    
    #===============================================================================#

    def make_config(self, packet_size, duration, protocol = "none", packet_count = -1):
        if packet_count == -1 and protocol == "":
            print('Entrada de teste inválida')
            return
        
        if(packet_count == -1):
            config = {
                "packetSize":packet_size ,
                "duration": duration,
                "protocol": protocol.upper()      
            }
        elif protocol == "none":
            config = {
                "pingPackets": packet_count    
            }
        else:
            config = {
                "packetSize":packet_size,
                "duration": duration,
                "protocol": protocol.upper(),
                "pingPackets": packet_count       
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
            instance.parameters_path = data["configuration"]["tests"]["routines-path"]
            instance.routines_path = data["configuration"]["tests"]["parameters-path"]
            instance.output_file= data["configuration"]["tests"]["output-file"]
            instance.ping_index = data["configuration"]["tests"]["ping-index"]
            instance.iperf_index = data["configuration"]["tests"]["iperf-index"]
            instance.std_test_file = data["configuration"]["std-test-file"]
           
        return Configuration_._instance  
    
