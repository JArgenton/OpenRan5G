from .Executor import Executor
import os
import time

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
            print("2 - Rotinas ")
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
            elif choice == 2:
                self.routineMenu()
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

    def routineMenu(self):
        while True:
            os.system('clear')
            print("="*40)
            print("       GERENCIAMENTO DE ROTINAS        ")
            print("="*40)
            print("1 - Listar rotinas existentes")
            print("2 - Visualizar testes de uma rotina")
            print("3 - Criar nova rotina")
            print("4 - Ativar/Desativar rotina")
            print("5 - Excluir rotina")
            print("6 - Voltar")
            print("-"*40)

            choice = input(">> Escolha uma opção: ").strip()

            if choice == '1':
                self.list_routines()
            elif choice == '2':
                self.view_routine_tests()
            elif choice == '3':
                self.create_routine_interactive()
            elif choice == '4':
                self.toggle_routine_status()
            elif choice == '5':
                self.delete_routine_interactive()
            elif choice == '6':
                break
            else:
                input("Opção inválida. Pressione Enter para continuar.")

    def list_routines(self):
        os.system('clear')
        routines = self.executor.getRoutines()["routines"]

        if not routines:
            print("⚠️ Nenhuma rotina encontrada.")
        else:
            print(f"📋 {len(routines)} rotina(s) encontrada(s):\n")
            for routine in routines:
                print(f"🆔 ID: {routine['ROUTINE_ID']} | Nome: {routine['NAME']} | Horário: {routine['TIME']} | Ativa: {'Sim' if routine['ACTIVE'] else 'Não'}")

        input("\nPressione Enter para voltar.")

    def view_routine_tests(self):
        try:
            r_id = int(input("Digite o ID da rotina que deseja visualizar >> "))
        except ValueError:
            input("ID inválido. Pressione Enter para voltar.")
            return

        tests = self.executor.getRoutineTests(r_id)["tests"]

        if not tests:
            print("⚠️ Nenhum teste vinculado a essa rotina.")
        else:
            print(f"\n🔍 Testes da rotina {r_id}:")
            for i, test in enumerate(tests, start=1):
                print(f"\n🔹 Teste {i} (ID: {test['TEST_ID']})")
                print(f"   Protocolo: {test['PROTOCOL']}")
                print(f"   Duração: {test['DURATION_SECONDS']}s")
                print(f"   Tamanho do pacote: {test['PACKET_SIZE']} bytes")
                print(f"   Nº de pacotes ping: {test['PACKET_COUNT']}")

        input("\nPressione Enter para voltar.")

    def create_routine_interactive(self):
        os.system("clear")
        print("🆕 CRIAR NOVA ROTINA")
        print("-" * 40)

        nome = input("Nome da rotina: ").strip()
        server = input("Endereço/IP do servidor (ex: 192.168.0.1): ").strip()
        horario = input("Horário de execução (HH:MM): ").strip()

        tests = []

        while True:
            print("\n➕ Adicionando novo teste")
            protocolo = input("Protocolo (tcp/udp/nenhum): ").strip().lower()
            if protocolo not in ['tcp', 'udp', 'nenhum']:
                print("⚠️ Protocolo inválido. Use 'tcp', 'udp' ou 'nenhum'.")
                continue

            duracao = input("Duração (em segundos): ").strip()
            tamanho_pacote = input("Tamanho do pacote (em bytes): ").strip()
            pacotes_ping = input("Pacotes para o ping (0 para nenhum): ").strip()

            try:
                teste = {
                    "protocol": "" if protocolo == "nenhum" else protocolo,
                    "duration": int(duracao),
                    "packetSize": int(tamanho_pacote),
                    "pingPackets": int(pacotes_ping),
                    "ping": int(pacotes_ping) > 0,
                    "default": False
                }
                tests.append(teste)
            except ValueError:
                print("⚠️ Valores inválidos. Repita o teste.")
                continue

            mais = input("Adicionar outro teste? (s/n): ").strip().lower()
            if mais != 's':
                break

        routine_obj = {
            "params": {
                "routineName": nome,  # Corrigido aqui!
                "server": server,
                "time": horario,
                "active": True
            },
            "tests": tests
        }

        self.executor.createRoutine(routine_obj)
        input("\n✅ Rotina criada com sucesso! Pressione Enter para voltar.")

    def toggle_routine_status(self):
        os.system("clear")
        print("🔁 ATIVAR / DESATIVAR ROTINA")
        print("-" * 40)

        rotinas = self.executor.getRoutines()["routines"]
        if not rotinas:
            print("⚠️ Nenhuma rotina cadastrada.")
            input("\nPressione Enter para voltar.")
            return

        for rotina in rotinas:
            status = "🟢 Ativa" if rotina["ACTIVE"] else "🔴 Inativa"
            print(f"ID: {rotina['ROUTINE_ID']} | Nome: {rotina['NAME']} | {status} | Horário: {rotina['TIME']}")

        try:
            r_id = int(input("\nDigite o ID da rotina que deseja alterar: "))
        except ValueError:
            input("⚠️ ID inválido. Pressione Enter para voltar.")
            return

        # Verifica se a rotina existe
        rotina_alvo = next((r for r in rotinas if r["ROUTINE_ID"] == r_id), None)
        if not rotina_alvo:
            input("❌ Rotina não encontrada. Pressione Enter para voltar.")
            return

        novo_estado = not rotina_alvo["ACTIVE"]
        self.executor.activateRoutine(r_id, novo_estado, rotina_alvo["TIME"])
        estado_txt = "ativada" if novo_estado else "desativada"
        input(f"\n✅ Rotina {r_id} {estado_txt} com sucesso! Pressione Enter para voltar.")

    def delete_routine_interactive(self):
        os.system("clear")
        print("🗑️ EXCLUIR ROTINA")
        print("-" * 40)

        rotinas = self.executor.getRoutines()["routines"]
        if not rotinas:
            input("⚠️ Nenhuma rotina cadastrada. Pressione Enter para voltar.")
            return

        for rotina in rotinas:
            status = "🟢 Ativa" if rotina["ACTIVE"] else "🔴 Inativa"
            print(f"ID: {rotina['ROUTINE_ID']} | Nome: {rotina['NAME']} | {status} | Horário: {rotina['TIME']}")

        try:
            r_id = int(input("\nDigite o ID da rotina que deseja excluir: "))
        except ValueError:
            input("⚠️ ID inválido. Pressione Enter para voltar.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir a rotina {r_id}? (s/n): ").strip().lower()
        if confirmacao != 's':
            print("❌ Operação cancelada.")
            time.sleep(1)
            return

        self.executor.deleteRoutine(r_id)
        input(f"\n✅ Rotina {r_id} excluída com sucesso! Pressione Enter para voltar.")


if __name__ == "__main__":
    menu = Menu()
    menu.mainMenu()
