from ..database.rotinas_DAO import RotinasDAO
from ..database.relacionamentos_R2T import _Relacionamento_R2T as R2T_DAO
from .network_test import Test
from .results import Result


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
    @staticmethod
    def formatRoutineJson(routine):
        return{
            "ROUTINE_ID": routine[0],
            "SERVER": routine[2],
            "NAME": routine[1],
            "TIME": routine[3],
            "ACTIVE": routine[4]
        }
    
    def getRoutineID(routine_name):
        return Routine.routine_table.fetch_where(f"WHERE NAME = '{routine_name}'")
        
    
    @staticmethod
    def getRoutineResultsByName(rName: str):
        sql = f"""
            SELECT 
                res.RESULT_ID,
                res.ROUTINE_ID,
                t.TEST_ID,
                res.TIMESTAMP_RESULT,
                res.SERVER,
                res.MIN_LATENCY,
                res.AVG_LATENCY,
                res.MAX_LATENCY,
                res.LOST_PACKETS,
                res.LOST_PERCENT,
                res.BITS_PER_SECOND,
                res.BYTES_TRANSFERED,
                res.JITTER,
                res.RETRANSMITS,
                t.PROTOCOL,
                t.DURATION_SECONDS,
                t.PACKET_SIZE,
                t.PACKET_COUNT
            FROM {Routine.R2T.table_name} r2t
            JOIN {Test.database.table_name} t ON t.TEST_ID = r2t.TEST_ID
            JOIN {Result.database.table_name} res ON res.TEST_ID = t.TEST_ID
            JOIN {Routine.routine_table.table_name} rout ON rout.NAME = ?
        """
        Routine.routine_table._cur.execute(sql, (rName,))
        return Routine.routine_table._cur.fetchall()
        

    @staticmethod
    def getRoutineTestResults(r_id, t_id):
        sql = f"""
            SELECT 
                res.RESULT_ID,
                res.ROUTINE_ID,
                t.TEST_ID,
                res.TIMESTAMP_RESULT,
                res.SERVER,
                res.MIN_LATENCY,
                res.AVG_LATENCY,
                res.MAX_LATENCY,
                res.LOST_PACKETS,
                res.LOST_PERCENT,
                res.BITS_PER_SECOND,
                res.BYTES_TRANSFERED,
                res.JITTER,
                res.RETRANSMITS,
                t.PROTOCOL,
                t.DURATION_SECONDS,
                t.PACKET_SIZE,
                t.PACKET_COUNT
            FROM {Routine.R2T.table_name} r2t
            JOIN {Test.database.table_name} t ON t.TEST_ID = r2t.TEST_ID
            JOIN {Result.database.table_name} res ON res.TEST_ID = t.TEST_ID
            WHERE r2t.ROUTINE_ID = ?
            AND t.TEST_ID = ?
            AND res.ROUTINE_ID = ?
        """
        try:
            Routine.routine_table._cur.execute(sql, (r_id, t_id, r_id))
            results = Routine.routine_table._cur.fetchall()
            return results if results else []
        except Exception as e:
            print(f"[ERRO SQL getRoutineTestResults] {e}")
            return []

