import sqlite3
import json
class Database:
    _instance = None
    def __init__(self):
        self.conn = sqlite3.connect('results.db')
        self.cursor = self.conn.cursor()
        self.__build_table__()

    def get_object():
        if Database._instance == None:
            Database._instance = Database()
        return Database._instance

    def __build_table__(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS testes (
            id PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            server TEXT NOT NULL,
            protocol TEXT NOT NULL,
            test_type_ping TEXT NOT NULL,
            test_type_iperf TEXT NOT NULL,
            duration_seconds REAL NOT NULL,
            packet_size INTEGER NOT NULL,
            bits_per_second REAL,
            lost_packets REAL,       
            lost_percent REAL, 
            bytes_transferred REAL,
            jitter REAL,
            packets REAL,
            retransmits REAL,
            target TEXT,
            packet_count INTEGER,
            min_latency REAL,
            avg_latency REAL,
            max_latency REAL
        )''')

    def add_tests_to_database(self, path):
        with open(path, 'r')as file:
            data = json.load(file)
        for result in data["tests"]:
            self.__insert_data__(result)

    def __extract_data_from_json__(self, data):
        date = data["iperf_data"]["timestamp"]
        test_type_iperf = data["iperf_data"]["test_type"]
        protocol = data["iperf_data"]["protocol"]
        server = data["iperf_data"]["parameters"]["server"]
        duration_seconds = data["iperf_data"]["parameters"]["duration_seconds"]
        packet_size = data["iperf_data"]["parameters"]["packet_size"]
        bits_per_second = data["iperf_data"]["results"]["bits_per_second"]
        bytes_transferred = data["iperf_data"]["results"]["bytes_transferred"]

        # Só adiciona se existir
        lost_packets = data["iperf_data"]["results"].get("lost_packets", None)
        lost_percent = data["iperf_data"]["results"].get("lost_percent", None)
        jitter = data["iperf_data"]["results"].get("Jitter", None)
        packets = data["iperf_data"]["results"].get("packets", None)
        retransmits = data["iperf_data"]["results"].get("retransmits", None)

        # Dados do ping
        test_type_ping = data["ping_data"]["test_type"]
        target = data["ping_data"]["parameters"]["target"]
        packet_count = data["ping_data"]["parameters"]["packet_count"]
        min_latency = data["ping_data"]["results"]["min_latency_ms"]
        avg_latency = data["ping_data"]["results"]["avg_latency_ms"]
        max_latency = data["ping_data"]["results"]["max_latency_ms"]

        return (
            date, server, protocol, test_type_ping, test_type_iperf, duration_seconds, packet_size,
            bits_per_second, lost_packets, lost_percent, bytes_transferred,
            jitter, packets, retransmits, target, packet_count,
            min_latency, avg_latency, max_latency
        )

    def __insert_data__(self, data):
        # Insere os dados no banco de dados diretamente
        self.cursor.execute(
            '''
            INSERT INTO testes (
                date, server, protocol, test_type_ping, test_type_iperf, duration_seconds, packet_size,
                bits_per_second, lost_packets, lost_percent, bytes_transferred,
                jitter, packets, retransmits, target, packet_count,
                min_latency, avg_latency, max_latency
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            self.__extract_data_from_json__(data)
        )
        self.conn.commit()

    def print_all_data(self): #func do gepete, nem olhei
        self.cursor.execute('SELECT * FROM testes')
        rows = self.cursor.fetchall()  # Retorna todos os registros da tabela

        for row in rows:
            print(row)
