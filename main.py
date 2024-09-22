import funcoes as f
import time as t

def menu():
    while True:
        op = f.validar_num("\n 1 - opções de cadastros \n 2 - opções de exclusão e atualização \n 3 - ver registros ou tabelas\n 4 - sair\nEscolha uma opção: ", min=1, max=4)
        if op == 1:
            while True:
                print("\nOPÇÕES DE CADASTRO")
                opcad = f.validar_num("\n 1 - cadastrar cliente \n 2 - cadastrar produto \n 3 - cadastrar pedido \n 4 - sair\nEscolha uma opção: ", min=1, max=4)
                if opcad == 1:
                    f.cad_cliente()
                elif opcad == 2:
                    f.cad_produto()
                elif opcad == 3:
                    f.cad_pedido()
                else:
                    break
        elif op == 2:
            while True:
                print("\nOPÇÕES DE EXCLUSÃO E ATUALIZAÇÃO")
                opexat = f.validar_num("\n 1 - excluir item\n 2 - atualizar registro\n 3 - sair\nEscolha uma opção: ", min=1, max=3)
                if opexat == 1:
                    f.ex_item()
                elif opexat == 2:
                    f.att_item()
                else:
                    break
        elif op == 3:
            while True:
                opconsul = f.validar_num("\n 1 - consultar tabela\n 2 - consultar todos os registros de uma tabela\n 3 - consultar os registros de um ID especifico\n 4 - sair\nEscolha uma opção: ",min=1, max=4)
                if opconsul == 1:
                    f.visualizar_tabelas()
                elif opconsul == 2:
                    f.consultar_registros()
                elif opconsul == 3:
                    f.consultar_registro_por_id()
                else:
                    break
        else:
            print("FINALIZANDO PROGRAMA", end="")
            for i in range(3):
                t.sleep(0.5)
                print(".", end="")
            t.sleep(0.3)
            print("\nPROGRAMA FINALIZADO")
            return
menu()

# E-mail de contato: miguelbcassiano@gmail.com
email = "miguelbcassiano@gmail.com"
print(f"Para mais informações, entre em contato: {email}")



