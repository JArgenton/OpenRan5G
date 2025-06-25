from database.rotinas_DAO import RotinasDAO
from database.relacionamentos_R2T import _Relacionamento_R2T as R2T_DAO
from network_test import Test
import os
import getpass
from datetime import datetime, timedelta
from ..Executor import Executor

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
        try:
            hora_str, minuto_str = routine_dict["TIME"].split(":")
            Routine.agendar_execucao_para(int(hora_str), int(minuto_str))
        except Exception as e:
            print(f"Erro ao agendar execução: {e}")

    @staticmethod
    def agendar_execucao_para(hora: int, minuto: int):
        caminho_script = os.path.abspath(__file__)
        
        horario = datetime(2024, 1, 1, hora, minuto) - timedelta(minutes=1)
        hora_agendada = horario.hour
        minuto_agendado = horario.minute

        cron_linha = f"{minuto_agendado} {hora_agendada} * * * /usr/bin/python3 {caminho_script} # agendado_auto"
        crontab_atual = os.popen(f"crontab -l 2>/dev/null").read()

        if cron_linha in crontab_atual:
            print("Execução já agendada.")
            return

        nova_crontab = crontab_atual + f"\n{cron_linha}\n"
        with os.popen("crontab -", "w") as cron:
            cron.write(nova_crontab)

        print(f"Script agendado para {hora_agendada:02d}:{minuto_agendado:02d} diariamente.")


if __name__ == '__main__':
    #verificar qual rotina foi agendada e executar o terminal
    executor = Executor()
    executor.clean_tests()
    