import re
from datetime import datetime
import sqlite3
from os import remove


#
# funções utilitarias
#

# Função para validar input do tipo string
def validar_str(msg, qtd=2):
    while True:
        a = input(msg)
        a = a.strip()
        if len(a) <= qtd:
            print(f"\nValor inválido!")
        else:
            return a


# Função para validar números
def validar_num(msg, tipo="int", min=0, max=1000):
    while True:
        try:
            a = float(input(msg))
            if a < min or a > max:
                print(f"\nValor inválido! Digitar valores entre {min} e {max}!")
            else:
                if tipo == "int":
                    a = int(a)
                elif tipo == "float":
                    a = float(a)
                return a
        except ValueError:
            print(f"Valor inválido!")


# Função para validar e-mail
def validar_email(msg="Digite seu E-mail: ", emailpronto=None):
    while True:
        if emailpronto is None:
            email = input(msg)
        else:
            email = emailpronto
        regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if re.match(regex, email):
            return email
        else:
            print("E-mail inválido! Tente novamente.")


# Função para validar telefone
def validar_tel(msg="Insira um número de telefone: ", telpronto=None):
    while True:
        try:
            if telpronto is None:
                tel = input(msg)
                int(tel)
            else:
                tel = telpronto
                int(tel)
            tel = tel.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            if len(tel) != 11 or not tel.isdigit():
                print("Telefone inválido! Deve ter 11 dígitos.")
                tel = None
            else:
                return tel
        except:
            print("Telefone invalido, não deve conter letras ou caracteres especiais")


# Função para validar data
def validar_data(msg="Insira uma data (DD-MM-AAAA): "):
    while True:
        data = input(msg)
        if '/' in data:
            print("Formato inválido! Use apenas traços (-).")
            continue
        try:
            data_valida = datetime.strptime(data, "%d-%m-%Y")
            return data_valida.strftime("%d-%m-%Y")
        except ValueError:
            print("Data inválida! Tente novamente.")


# Função para buscar o ID do banco de dados
def bsc_ID(msg, nome_tabela='clientes', campo='nome'):
    nome_banc = input(msg)  # Nome do banco de dados
    conexao = sqlite3.connect('DB/meu_banco.db')  # Conectar ao banco de dados
    cursor = conexao.cursor()

    id_consulta = input(f"Digite o nome que deseja consultar o ID: ")  # Nome a ser consultado

    # Consulta dinâmica com a tabela e campo informados
    sql = f"SELECT {campo} FROM {nome_tabela} WHERE id = ?"
    cursor.execute(sql, (id_consulta,))

    # Buscar e exibir os resultados
    resultado = cursor.fetchone()
    if resultado:
        print(f"Resultado encontrado: {resultado[0]}")
    else:
        print(f"Nenhum resultado encontrado para o ID {id_consulta}")

    # Fechar a conexão
    conexao.close()


#
# funções de cadastro
#


# Função para cadastrar clientes
def cad_cliente():
    nome = validar_str("Digite o nome do cliente: ")
    idade = validar_num("Insira a idade do cliente: ", max=130)
    email = validar_email()
    tel = validar_tel()

    # Inserir cliente no banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO clientes (nome, idade, email, fone) VALUES (?, ?, ?, ?)
    """, (nome, idade, email, tel))

    conexao.commit()
    print(f"Cliente {nome} cadastrado com sucesso!")

    conexao.close()


# Função para cadastrar produtos
def cad_produto():
    nome = validar_str("Digite o nome do produto: ")
    preco = validar_num("Insira o valor do produto: ", tipo="float", min=0, max=100000000)
    qtd = validar_num("Insira a quantidade em estoque: ")

    # Inserir produto no banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, preco, qtd) VALUES (?, ?, ?)
    """, (nome, preco, qtd))

    conexao.commit()
    print(f"Produto {nome} cadastrado com sucesso!")

    conexao.close()


# Função para cadastrar pedidos e itens do pedido
def cad_pedido():
    # Conectar ao banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Cadastro do cliente
    id_cliente = validar_num("Digite o ID do cliente: ")

    # Cadastro dos produtos e quantidade
    id_produto = validar_num("Digite o ID do produto: ")
    qtd = validar_num("Insira a quantidade de produtos: ")
    preco = validar_num("Insira o valor do pedido: ", tipo="float", min=0, max=100000000)
    data = validar_data()

    # Inserir os itens do pedido na tabela itens_pedidos
    cursor.execute("""
    INSERT INTO itens_pedidos (cliente_id, produto_id, qtd)
    VALUES (?, ?, ?)
    """, (id_cliente, id_produto, qtd))

    # Obter o ID do item recém-criado
    item_id = cursor.lastrowid

    # Inserir o pedido na tabela pedidos
    cursor.execute("""
    INSERT INTO pedidos (cliente_id, itens_pedido_id, preco, data)
    VALUES (?, ?, ?, ?)
    """, (id_cliente, item_id, preco, data))

    # Commit e fechar a conexão
    conexao.commit()
    conexao.close()

    print(f"Pedido cadastrado com sucesso! ID do item: {item_id}")


#
# funções de exclusão e atualização
#
# função para excluir o item de uma tabela
def ex_item(msg="Insira a tabela que deseja excluir um registro: ", nome_tabela=None,
            msg2="Insira o ID do registro a ser excluído: ", id_ex=None):
    if nome_tabela is None:
        nome_tabela = validar_str(msg)

    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Recebe o ID do item a ser excluído
    if id_ex is None:
        id_ex = validar_num(msg2, tipo="int")  # Validar como número inteiro

    # Remove o item da tabela desejada
    cursor.execute(f"DELETE FROM {nome_tabela} WHERE id = ?", (id_ex,))

    conexao.commit()
    conexao.close()

    print('Registro excluído com sucesso.')
    return nome_tabela, id_ex

# função de atualizar registros
def att_item(nome_tabela=None):
    # Conectar ao banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Receber o nome da tabela caso esteja = None
    if nome_tabela is None:
        nome_tabela = validar_str("Insira o nome da tabela: ")

    # Solicitar o ID do registro que deseja atualizar
    id_registro = validar_num(f"Digite o ID do registro na tabela '{nome_tabela}' que deseja atualizar: ", tipo="int")

    # Verificar se o registro existe
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE id = ?", (id_registro,))
    if cursor.fetchone() is None:
        print(f"Nenhum registro encontrado com o ID {id_registro} na tabela '{nome_tabela}'.")
        conexao.close()
        return

    # Obter os campos disponíveis para atualização
    if nome_tabela == 'clientes':
        campo = validar_str("Digite o campo que deseja atualizar (nome, idade, email, fone): ")

        if campo == 'nome':
            novo_valor = validar_str(f"Digite o novo valor para {campo}: ")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'idade':
            novo_valor = validar_num(f"Digite o novo valor para {campo} (0 a 130): ", tipo="int", min=0, max=130)
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'email':
            novo_valor = validar_email("Digite o novo e-mail: ")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'fone':
            novo_valor = validar_tel("Digite o novo telefone: ")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        else:
            print("Campo inválido!")
            conexao.close()
            return

    elif nome_tabela == 'produtos':
        campo = validar_str("Digite o campo que deseja atualizar (nome, preco, qtd): ")

        if campo == 'nome':
            novo_valor = validar_str(f"Digite o novo valor para {campo}: ")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'preco':
            novo_valor = validar_num(f"Digite o novo valor para {campo} (0 a 100000000): ", tipo="float", min=0, max=100000000)
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'qtd':
            novo_valor = validar_num(f"Digite o novo valor para {campo} (0 a 100000): ", tipo="int", min=0, max=100000)
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        else:
            print("Campo inválido!")
            conexao.close()
            return

    elif nome_tabela == 'pedidos':
        campo = validar_str("Digite o campo que deseja atualizar (cliente_id, preco, data): ")

        if campo == 'cliente_id':
            novo_valor = validar_num(f"Digite o novo valor para {campo}: ", tipo="int")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'preco':
            novo_valor = validar_num(f"Digite o novo valor para {campo} (0 a 100000000): ", tipo="float", min=0, max=100000000)
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'data':
            novo_valor = validar_data("Digite a nova data (DD-MM-AAAA): ")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        else:
            print("Campo inválido!")
            conexao.close()
            return

    elif nome_tabela == 'itens_pedidos':
        campo = validar_str("Digite o campo que deseja atualizar (cliente_id, produto_id, qtd): ")

        if campo == 'cliente_id':
            novo_valor = validar_num(f"Digite o novo valor para {campo}: ", tipo="int")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'produto_id':
            novo_valor = validar_num(f"Digite o novo valor para {campo}: ", tipo="int")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        elif campo == 'qtd':
            novo_valor = validar_num(f"Digite o novo valor para {campo}: ", tipo="int")
            cursor.execute(f"UPDATE {nome_tabela} SET {campo} = ? WHERE id = ?", (novo_valor, id_registro))
        else:
            print("Campo inválido!")
            conexao.close()
            return

    else:
        print("Tabela inválida!")
        conexao.close()
        return

    # Commit e fechar a conexão
    conexao.commit()
    conexao.close()

    print(f"Registro na tabela '{nome_tabela}' atualizado com sucesso!")



#
# funções para visualizar tabelas e registros
#

# função para todas as tabelas
def visualizar_tabelas():

    # Conectar ao banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Consultar o nome das tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    if tabelas:
        print("Tabelas existentes:")
        for tabela in tabelas:
            print(tabela[0])
    else:
        print("Nenhuma tabela encontrada.")

    # Fechar a conexão
    conexao.close()

# função para visualizar os registros de uma tabela especifica
def consultar_registros(nome_tabela=None, msg="Insira o nome de uma tabela: "):
    # Conectar ao banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Receber o nome de uma tabela se necessário
    if nome_tabela is None:
        nome_tabela = validar_str(msg)  # Validação de string

    # Consultar todos os registros da tabela especificada
    cursor.execute(f"SELECT * FROM {nome_tabela};")
    registros = cursor.fetchall()

    if registros:
        print(f"Registros na tabela '{nome_tabela}':")
        for registro in registros:
            print(registro)
    else:
        print(f"Nenhum registro encontrado na tabela '{nome_tabela}'.")

    # Fechar a conexão
    conexao.close()

# função para visualizar os registros de um ID especifico de uma tabela
def consultar_registro_por_id(nome_tabela=None, id_registro=None, msg="Insira o nome de uma tabela: ", msg2="Insira um ID: "):
    # Conectar ao banco de dados
    conexao = sqlite3.connect('BD/meu_banco.db')
    cursor = conexao.cursor()

    # Receber o nome da tabela se necessário
    if nome_tabela is None:
        nome_tabela = validar_str(msg)  # Validação de string

    # Receber o ID do registro se necessário
    if id_registro is None:
        id_registro = validar_num(msg2, tipo="int")  # Validação como número inteiro

    # Consultar o registro com o ID especificado
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE id = ?", (id_registro,))
    registro = cursor.fetchone()

    if registro:
        print(f"Registro encontrado na tabela '{nome_tabela}': {registro}")
    else:
        print(f"Nenhum registro encontrado com o ID {id_registro} na tabela '{nome_tabela}'.")

    # Fechar a conexão
    conexao.close()

# E-mail de contato: miguelbcassiano@gmail.com
email = "miguelbcassiano@gmail.com"

if __name__ == "__main__":
    while True:
        print(f"Para mais informações, entre em contato: {email}")
        print("\nMenu:")
        print("1. Validar String")
        print("2. Validar Número")
        print("3. Validar E-mail")
        print("4. Validar Telefone")
        print("5. Validar Data")
        print("6. Buscar ID")
        print("7. Cadastrar Cliente")
        print("8. Cadastrar Produto")
        print("9. Cadastrar Pedido")
        print("10. Excluir Item")
        print("11. Atualizar Item")
        print("12. Visualizar Tabelas")
        print("13. Consultar Registros")
        print("14. Consultar Registro por ID")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            valor = validar_str("Digite uma string válida (mínimo 2 caracteres): ")
            print(f"String válida: {valor}")
        elif escolha == '2':
            numero = validar_num("Digite um número (0 a 1000): ", tipo="int", max=1000)
            print(f"Número válido: {numero}")
        elif escolha == '3':
            email = validar_email()
            print(f"E-mail válido: {email}")
        elif escolha == '4':
            telefone = validar_tel()
            print(f"Telefone válido: {telefone}")
        elif escolha == '5':
            data = validar_data()
            print(f"Data válida: {data}")
        elif escolha == '6':
            bsc_ID("Digite o nome do banco de dados: ")
        elif escolha == '7':
            cad_cliente()
        elif escolha == '8':
            cad_produto()
        elif escolha == '9':
            cad_pedido()
        elif escolha == '10':
            ex_item()
        elif escolha == '11':
            att_item()
        elif escolha == '12':
            visualizar_tabelas()
        elif escolha == '13':
            consultar_registros()
        elif escolha == '14':
            consultar_registro_por_id()
        elif escolha == '0':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# E-mail de contato: miguelbcassiano@gmail.com