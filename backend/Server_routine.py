#Sever_routine.py
#Rodar rotina servidor quando executado de maneira autonoma
#salvar os resultados 
from .database.server_routines_DAO import Server_Routines
from .configuration.configuration import Configuration_
from .tests.iperfr3_test import Iperf 
import time as t
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
    
    def deactivate_server_routine_by_time(self, time):
        update = f'UPDATE {self.table.table_name} SET ACTIVE = FALSE WHERE TIME = ?'
        self.table._cur.execute(update, (time,))
        self.table._conn.commit()

    def view_saved_routines(self):
        return self.table.fetch_all()
        
    def create_server_routine(self, hour, minutes):
        time = f'{hour:02d}:{minutes:02d}'
        if not (0 <= hour <= 23 and 0 <= minutes <= 59):
            raise ValueError("Hora ou minutos inválidos")
        
        self.deactivate_server_routine_by_time(time)
        data = {
            "TIME" : time,
            "ACTIVE" : True
        }

        self.table.insert(data)

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
        process = Iperf.run_iperf3_server()
        t.sleep(8 * 60)
        process.kill()
    


if __name__ == '__main__':
    server = server_routines.get_instance()
    server.execute()
 