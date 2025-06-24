# network_test.py (AJUSTADO)
from ..database.testes_de_rede import TestesDeRedeDAO

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
        Test.database.insert(test_obj)
        test_id = Test.database._cur.lastrowid
        print(f"Test data sent to database for insertion. Test ID: {test_id}")
        return test_id
    @staticmethod
    def get_or_create_test_id(dados_teste: dict) -> int:
        conditions = []
        values = []

        for field in ["PROTOCOL", "DURATION_SECONDS", "PACKET_SIZE", "PACKET_COUNT"]:
            val = dados_teste.get(field)
            if val is None:
                conditions.append(f"{field} IS NULL")
            else:
                conditions.append(f"{field} = ?")
                values.append(val)

        sql = f"""
            SELECT TEST_ID FROM testes_de_rede
            WHERE {" AND ".join(conditions)}
        """

        Test.database._cur.execute(sql, values)
        result = Test.database._cur.fetchone()

        if result:
            return result[0]

        # Inserir se não encontrou
        Test.database.insert(data=dados_teste)
        return Test.database.get_latest_id()
    
    @staticmethod
    def format_save_test(test: dict) -> dict:
        obj = {}

        # Campos diretos (protocolo pode não estar presente)
        obj["PROTOCOL"] = test.get("protocol", None)

        # duration
        try:
            obj["DURATION_SECONDS"] = float(test.get("duration", None))
        except (TypeError, ValueError):
            obj["DURATION_SECONDS"] = None

        # packet-size
        try:
            obj["PACKET_SIZE"] = int(test.get("packetSize", None))
        except (TypeError, ValueError):
            obj["PACKET_SIZE"] = None

        # package-count (ping)
        try:
            obj["PACKET_COUNT"] = int(test.get("pingPackets", None))
        except (TypeError, ValueError):
            obj["PACKET_COUNT"] = None

        return obj
