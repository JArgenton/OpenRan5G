#Sever_routine.py
#Rodar rotina servidor quando executado de maneira autonoma
#salvar os resultados 
from database.server_routines_DAO import Server_Routines
from .configuration.configuration import Configuration_
from .tests.iperfr3_test import Iperf 
class server_routines():
    _instance = None
    def __init__(self) -> None:
        self.config = Configuration_.getObject()
        self.table = Server_Routines()
    @staticmethod
    def get_instance():
        if(server_routines._instance is None):
            return server_routines()
        return server_routines._instance
    
    def create_server_routine(self):
        #salvar na tabela:
        #Routine ID
        #timestamp
        ...
    def execute(self):
        hour, minute = self.config.get_HH_MM()
        hour, minute = self.config.set_round_time(hour, minute)
        time = f"{hour:02d}:{minute:02d}"
        where = f"""WHERE TIME = '{time}'"""
        rotina_resultado = self.table.fetch_where(where)
        print(rotina_resultado)

        if not rotina_resultado:
            print("Nenhuma rotina encontrada para o horário atual.")
            exit(0)
        Iperf.run_iperf3_server()
    


if __name__ == '__main__':
    server = server_routines.get_instance()
    server.execute()
 