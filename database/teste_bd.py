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
    index 
    {
    "timestamp": "24-12_13-53",
    "test_type": "bandwidth",
    "protocol": "UDP",
    "parameters": {
        "server": "192.168.1.14",
        "duration_seconds": 10,
        "packet_size": 64
    },
    "results": {
        "bits_per_second": 1048513.0566537655,
        "lost_packets": 0,
        "lost_percent": 0,
        "bytes_transferred": 1310656,
        "Jitter": 0.02100033366138135,
        "packets": 20479
    }
}   

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
            date, test_index, protocol, test_type, duration_seconds, packet_size,
            bits_per_second, lost_packets, lost_percent, bytes_transferred,
            jitter, packets, retransmits
        )
    )
    self.conn.commit()  # Certifique-se de salvar as alterações
