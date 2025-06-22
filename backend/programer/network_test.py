# network_test.py (AJUSTADO)
from database.testes_de_rede import TestesDeRedeDAO

class Test:
    database = TestesDeRedeDAO()

    def __init__(self, duration: str, packet_size: str, ping_packets: str, protocol: str, server: str):
        self.duration = duration
        self.packet_size = packet_size
        self.ping_packets = ping_packets
        self.protocol = protocol
        self.server = server

    def __str__(self):
        return (f"Server: {self.server}, Protocol: {self.protocol}, Duration: {self.duration},"
                f" Packet Size: {self.packet_size}, Ping Packets: {self.ping_packets}")

    @staticmethod
    def insert_test(test_obj: dict) -> int:
        """
        Insere os dados de um objeto Test no banco de dados e retorna o ID gerado.
        """
        data = {
            "PROTOCOL" : test_obj["PROTOCOL"],
            "DURATION_SECONDS": test_obj["DURATION_SECONDS"],
            "PACKET_SIZE": test_obj["PACKET_SIZE"],
            "PACKET_COUNT": test_obj["PACKET_COUNT"]
        }
        Test.database.insert(data)
        test_id = Test.database._cur.lastrowid
        print(f"Test data sent to database for insertion. Test ID: {test_id}")
        return test_id