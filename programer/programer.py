from execute import Executor as exec
import os 
import json

class Programer():

    def __init__(self):
        pass
    
    def create_routine():
        print("/////////////////////// - CONFIGURAÇAO DE ROTINA - /////////////////////// \n")

        dirs_name = str(input("QUAL SERA O NOME DA ROTINA? \n"))
    os.mkdir("programer/routines/{dirs_name}")


    print("//////////////////////////////////////////////////////////////////////////\n")
    
    def build_tests(self):
        ip = str(input("Insira o ip: "))

        inserir_novo_teste = str(input("Deseja inserir um novo teste? \n S \n N \n")).upper()
        if inserir_novo_teste == 'S':
            with open(self.configuration.parameters_path, 'w') as file:
                json.dump(self.configuration.std_test_file, file, indent=4)

            self.insert_tests(inserir_novo_teste) #essa é a primeira vez que eu senti q um do while ia ser util, nao sei se isso existe em python e o gepete morreu
        return ip
