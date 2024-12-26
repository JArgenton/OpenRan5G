import sqlite3

class DataBase():
    def __init__(self):
        conn = sqlite3.connect('results.db')
        self.cursor = conn.cursor()

def build_table(self):
    self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS testes (
        date TEXT NOT NULL,
        index INTEGER NOT NULL,
        protocol TEXT NOT NULL,
        test_type TEXT NOT NULL,
        duration_seconds REAL NOT NULL,
        packet_size INTEGER NOT NULL,
        bits_per_second REAL,
        lost_packets REAL,       
        lost_percent REAL, 
        bytes_transferred REAL,
        jitter REAL,
        packets REAL,
        retransmits REAL
    )''')

        
def insert_data(self, data):

    date = data["timestamp"]
    test_type = data["test_type"]
    protocol = data["protocol"]
    server = data["parameters"]["server"]
    duration_seconds = data["parameters"]["duration_seconds"]
    packet_size = data["parameters"]["packet_size"]
    bits_per_second = data["results"]["bits_per_second"]
    lost_packets = data["results"]["lost_packets"]
    lost_percent = data["results"]["lost_percent"]
    bytes_transferred = data["results"]["bytes_transferred"]
    jitter = data["results"]["Jitter"]
    packets = data["results"]["packets"]

    #TODO -> organizar por protocolo


    self.cursor.execute(
        '''
        INSERT INTO testes (
            date, index, protocol, test_type, duration_seconds, packet_size,
            bits_per_second, lost_packets, lost_percent, bytes_transferred,
            jitter, packets, retransmits
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            date, protocol, test_type, duration_seconds, packet_size,
            bits_per_second, lost_packets, lost_percent, bytes_transferred,
            jitter, packets, retransmits
        )
    )
    self.conn.commit()  # Certifique-se de salvar as alterações
