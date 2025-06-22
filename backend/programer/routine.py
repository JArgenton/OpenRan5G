from database.rotinas_DAO import RotinasDAO
from database.relacionamentos_R2T import _Relacionamento_R2T as R2T_DAO
from network_test import Test


class Routine:
    routine_table = RotinasDAO()
    R2T = R2T_DAO()
    last_routine_id : int
    def __init__(self, name: str):
        self.name 
        self._test: list

    @property.getter
    def routine(self):
        return self._test
    
    @staticmethod
    def create_routine_tests(rotina:'Routine', routine_dict : dict, formatted_tests_list: list[dict]): 

        print(f"\nIniciando criação rotina ")

        data = {
            "NAME"      :rotina.name,
            "SERVER"    :routine_dict["SERVER"],
            "TIME"      :routine_dict["TIME"],
            "ACTIVE"    :routine_dict["ACTIVE"]
        }
        Routine.routine_table.insert(data)
        Routine.last_routine_id = Routine.routine_table._cur.lastrowid

        print(f"\n Criação rotina {Routine.last_routine_id} concluida")
        
        for test_data_dict in formatted_tests_list: 
            test_id = Test.insert_test(test_data_dict)

            if test_id:
                rotina._test.append(test_id)
                relationship_data = {
                    "TEST_ID"       : test_id,
                    "ROUTINE_ID"    : Routine.last_routine_id
                }
            else:
                print(f"AVISO: Não foi possível obter test_id para os dados: {test_data_dict}")

        Routine.R2T.insert(relationship_data)
            
        print(f"Concluída a criação de testes e relacionamentos para a rotina '{rotina.name}'.")
        print(f"test_ids -> {rotina.routine}")
