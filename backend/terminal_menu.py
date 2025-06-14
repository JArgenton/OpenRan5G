from backend.Executor import Executor
import os

class Menu:
    def __init__(self):
        self.executor = Executor()

    def clientMenu(self):
        while True:
            os.system('clear')
            print("="*40)
            print("        CLIENTE - MENU DE OPÇÕES        ")
            print("="*40)
            print("1 - Rodar testes")
            print("2 - Rotinas (em breve)")
            print("3 - Histórico de testes (em breve)")
            print("4 - Voltar")
            print("-"*40)

            try:
                choice = int(input(">> Escolha uma opção: "))
            except ValueError:
                input("Opção inválida. Pressione Enter para continuar.")
                continue

            if choice == 1:
                ip = self.build_tests()
                os.system('clear')
                print("Executando testes...\n")
                self.executor.run_tests(ip)
                input('\nPressione Enter para continuar...')
            elif choice == 4:
                return
            else:
                input("Opção ainda não implementada. Pressione Enter para continuar.")

    def mainMenu(self):
        while True:
            os.system('clear')
            print("="*40)
            print("         TESTE DE REDE - MENU           ")
            print("="*40)
            print("1 - Cliente")
            print("2 - Servidor")
            print("-"*40)

            choice = input(">> Escolha uma opção: ")

            if choice == '2':
                print("\nIniciando servidor iperf3...\n")
                self.executor.run_server()
            elif choice == '1':
                self.clientMenu()
            else:
                input("Comando inválido. Pressione Enter para continuar.")

    def build_tests(self):
        os.system('clear')
        inserir_novo_teste = input("Deseja inserir um novo teste? (S/N) >> ").strip().upper()
        ip = input("Insira o IP do servidor >> ").strip()

        if inserir_novo_teste == 'S':
            self.executor.clean_tests()

        while inserir_novo_teste == 'S':
            os.system('clear')
            print("="*40)
            print("       INSERÇÃO DE NOVO TESTE           ")
            print("="*40)

            try:
                packet_size = int(input(">> Tamanho do pacote (bytes): "))
                duration = int(input(">> Duração do teste (s): "))

                protocol = input(">> Protocolo (TCP/UDP): ").strip().upper()
                if protocol not in ["TCP", "UDP"]:
                    raise ValueError("Protocolo inválido! Use TCP ou UDP.")
                
                package_count = int(input(">> Nº de pacotes para ping: "))
                ntests = int(input(">> Nº de repetições desse teste: "))
            except ValueError:
                input("\nEntrada inválida. Pressione Enter para tentar novamente.")
                continue

            self.executor.insert_tests(packet_size, duration, protocol, ntests, package_count)
            print("\n✔️ Teste inserido com sucesso!\n")

            inserir_novo_teste = input("Deseja inserir outro teste? (S/N) >> ").strip().upper()

        return ip


if __name__ == "__main__":
    menu = Menu()
    menu.mainMenu()
