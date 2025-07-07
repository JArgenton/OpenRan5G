from .Executor import Executor
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
            print("3 - Histórico de testes")
            print("4 - Voltar")
            print("-"*40)

            try:
                choice = int(input(">> Escolha uma opção: "))
            except ValueError:
                input("Opção inválida. Pressione Enter para continuar.")
                continue

            if choice == 1:
                self.run_tests_interactive()
                input('\nPressione Enter para continuar...')
            elif choice == 3:
                self.data_log()
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

    def data_log(self):
        resultado = self.executor.load_results()
        for i, res in enumerate(resultado['results'], start=1):
            print(f"\n{'='*10} RESULTADO {i} {'='*10}")
            print(self.executor.format_result_for_terminal(res))


    def run_tests_interactive(self):
        os.system('clear')
        print("=" * 40)
        print("        EXECUTAR TESTES AGORA         ")
        print("=" * 40)

        server = input("Informe o IP ou domínio do servidor:\n>> ").strip()

        try:
            qtd_testes = int(input("\nQuantos testes diferentes deseja configurar?\n>> "))
            if qtd_testes <= 0:
                raise ValueError()
        except ValueError:
            input("\n❌ Valor inválido. Pressione Enter para voltar ao menu.")
            return

        self.executor.clean_tests()

        for i in range(qtd_testes):
            os.system('clear')
            print(f"--- Configuração do Teste {i+1} de {qtd_testes} ---")
            try:
                protocolo = input("Protocolo (TCP/UDP): ").strip().upper()
                if protocolo not in ["TCP", "UDP"]:
                    raise ValueError("Protocolo inválido! Use TCP ou UDP.")

                duracao = int(input("Duração (em segundos): "))
                pacote = int(input("Tamanho do pacote (em bytes): "))
                qtd_ping = int(input("Nº de pacotes para ping: "))

            except ValueError as e:
                input(f"\n❌ Entrada inválida: {e}. Pressione Enter para tentar novamente.")
                return

            self.executor.insert_tests(
                packet_size=pacote,
                duration=duracao,
                protocol=protocolo,
                ntests=1,
                package_count=qtd_ping
            )

        os.system('clear')
        print("✔️ Testes configurados. Executando...\n")
        resultado = self.executor.run_tests(server)
        for i, res in enumerate(resultado['results'], start=1):
            print(f"\n{'='*10} RESULTADO {i} {'='*10}")
            print(self.executor.format_result_for_terminal(res))


if __name__ == "__main__":
    menu = Menu()
    menu.mainMenu()
