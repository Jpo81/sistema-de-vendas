import sqlite3

# Conectando ao banco de dados único (por exemplo, 'BD/meu_banco.db')
conn = sqlite3.connect('BD/meu_banco.db')
cursor = conn.cursor()

# Criando a tabela clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    email TEXT NOT NULL,
    fone TEXT
);
""")
print('Tabela clientes criada com sucesso.')

# Criando a tabela produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    qtd INTEGER NOT NULL
);
""")
print('Tabela produtos criada com sucesso.')

# Criando a tabela pedidos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    itens_pedido_id INTEGER NOT NULL,
    preco REAL NOT NULL,
    data VARCHAR(10) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (itens_pedido_id) REFERENCES itens_pedidos(id)
);
""")
print('Tabela pedidos criada com sucesso.')

# Criando a tabela itens_pedidos
cursor.execute("""
CREATE TABLE itens_pedidos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
""")
print('Tabela itens_pedidos criada com sucesso.')

# Desconectando...
conn.close()

# E-mail de contato: miguelbcassiano@gmail.com
email = "miguelbcassiano@gmail.com"
print(f"Para mais informações, entre em contato: {email}")