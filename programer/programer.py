from configuration.configuration import Configuration
import os
import json

class Programmer:

    def __init__(self):
        self.configuration = Configuration.getObject()

    def insert_tests(self, dirs_name):
        packet_size = int(input("packet size: "))
        duration = int(input("duration: "))
        protocol = str(input("protocol: ")).upper()
        package_count = int(input("package count: "))

        self.configuration.make_config(f"programer/routines/{dirs_name}/routine", packet_size, duration, protocol, package_count)

        print("////////////////////////// - TESTE INSERIDO - //////////////////////////")

    def create_routine(self):
        print("/////////////////////// - CONFIGURAÇÃO DE ROTINA - /////////////////////// \n")
        
        dirs_name = input("QUAL SERÁ O NOME DA ROTINA? \n")
        os.mkdir(f"programer/routines/{dirs_name}")
        print("QUAIS TESTES DEVEM SER REALIZADOS PELA ROTINA \n")

        print(" 1 - IPERF \n")
        print(" 2 - PING \n")
        print(" 3 - TODOS \n")
        testes = input("")

        with open(f"programer/routines/{dirs_name}/routine", 'w') as file:
            json.dump(self.configuration.std_test_file, file, indent=4)

        print("///////////////////////////////////////////////////////////////////////////\n")

        inserir_novo_teste = True
        counter = 0 

        while inserir_novo_teste:
            os.system("clear")

            print("/////////////////////// - CRIAÇÃO DE TESTES - /////////////////////// \n")
            print(f"A ROTINA {dirs_name} POSSUI {counter} TESTES CADASTRADOS \n \n")

            self.insert_tests(dirs_name) 

            counter += 1

            os.system("clear")

            print("1 - INSERIR NOVO TESTE \n")
            print("2 - SAIR \n")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "2":
                inserir_novo_teste = False


if __name__ == '__main__':
        programer = Programmer()
        programer.create_routine()