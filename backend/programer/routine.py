from ..database.rotinas_DAO import RotinasDAO
from ..database.relacionamentos_R2T import _Relacionamento_R2T as R2T_DAO
from .network_test import Test


class Routine:
    routine_table = RotinasDAO()
    R2T = R2T_DAO()
    last_routine_id : int = -1
    def __init__(self):
        ...
    @staticmethod
    def create_routine_tests(routine_dict : dict, formatted_tests_list: list[dict]): 

        print(f"\nIniciando criação rotina ")

        data = {
            "NAME"      :routine_dict["routineName"],
            "SERVER"    :routine_dict["server"],
            "TIME"      :routine_dict["time"],
            "ACTIVE"    :True
        }

        Routine.routine_table.deactivate_routine_by_time(data['TIME'])
                
        if not(Routine.routine_table.insert(data)):
            Routine.last_routine_id = Routine.routine_table.get_latest_id()
            return

        Routine.last_routine_id = Routine.routine_table._cur.lastrowid

        print(Routine.last_routine_id)

        print(f"\n Criação rotina {Routine.last_routine_id} concluida")
        
        for test_data_dict in formatted_tests_list: 
            test_id = Test.get_or_create_test_id(test_data_dict)

            if test_id:
                relationship_data = {
                    "TEST_ID"       : test_id,
                    "ROUTINE_ID"    : Routine.last_routine_id
                }
            else:
                print(f"AVISO: Não foi possível obter test_id para os dados: {test_data_dict}")

            Routine.R2T.insert(relationship_data)

    def formatRoutineJson(routine):
        return{
            "ROUTINE_ID": routine[0],
            "SERVER": routine[2],
            "NAME": routine[1],
            "TIME": routine[3],
            "ACTIVE": routine[4]
        }

