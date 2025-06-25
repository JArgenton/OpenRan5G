import os
from ..Executor import Executor
from .routine import Routine, RotinasDAO
def get_path():
    return os.path.abspath(__file__)

if __name__ == '__main__':
    executor = Executor()
    tabela_rotinas = RotinasDAO()

    hour, minute = executor.configuration.get_HH_MM()
    hour, minute = executor.configuration.set_round_time(hour, minute)

    time = f"{hour:02d}:{minute:02d}"

    query = f"""SELECT ROUTINE_ID FROM {tabela_rotinas.table_name} WHERE TIME = '{time}'"""


    tabela_rotinas.fetch_where(query)
    executor.clean_tests()
    executor.insert_tests()
