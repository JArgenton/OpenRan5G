import json

class Configuration:
    """Fiz meio de sacanagem, pois este nao faz muito sentido pensando em enviar os comando pelo terminal.
        Mesmo assim este sera util pois facilita o codigo, e eu estava pensando melhor quanto a cascar os 
        parametros via terminal, nao sera nada eficiente e escalavel, desse jeito fica mais facil realizar 
        varios testes em sequencia."""
    _instance = None 

    def __init__(self):
        self.test_sequence = 0 #valor para alternar dentro do vetor de parametros teste
        self.test_size = 0 #valor para se colocar no for
        self.server = None
        self.iperf3_packet_size = None
        self.iperf3_duration = None
        self.iperf3_protocol = None
        self.ping_package_count = None

    @staticmethod
    def loadFromJson():
        with open('config.json', 'r') as file:
          data =  json.load(file)

        return data

    def getObject(index):
        if Configuration._instance is None:
            Configuration._instance = Configuration()
            data = Configuration.loadFromJson()

            instance = Configuration._instance
            instance.server = data["configuration"]["server"]
            instance.iperf3_packet_size = data["configuration"]["test"][index]["iperf3"]["packet-size"]
            instance.iperf3_duration = data["configuration"]["test"][index]["iperf3"]["duration"]
            instance.iperf3_protocol = data["configuration"]["test"][index]["iperf3"]["duration"]

            instance.ping_package_count = data["configuration"]["test"][index]["ping"]["package-count"]
        return Configuration._instance  