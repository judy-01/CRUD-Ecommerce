import sqlite3

# Função para conectar ao banco de dados e criar as tabelas se não existirem
def inicializar_banco():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS carrinho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade INTEGER,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    ''')
    conn.commit()
    conn.close()

# Funções CRUD para produtos
def adicionar_produto(nome, preco, quantidade):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)', (nome, preco, quantidade))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('SELECT * FROM produtos')
    produtos = c.fetchall()
    conn.close()
    return produtos

def remover_produto(produto_id):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    conn.close()

def atualizar_produto(produto_id, nome, preco, quantidade):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?', (nome, preco, quantidade, produto_id))
    conn.commit()
    conn.close()

# Funções para gerenciar o carrinho de compras
def adicionar_ao_carrinho(produto_id, quantidade):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
    estoque = c.fetchone()[0]
    if quantidade <= estoque:
        c.execute('INSERT INTO carrinho (produto_id, quantidade) VALUES (?, ?)', (produto_id, quantidade))
        c.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?', (quantidade, produto_id))
        conn.commit()
    else:
        print("Quantidade solicitada não disponível em estoque.")
    conn.close()

def listar_carrinho():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''
        SELECT produtos.nome, produtos.preco, carrinho.quantidade
        FROM carrinho
        JOIN produtos ON carrinho.produto_id = produtos.id
    ''')
    itens = c.fetchall()
    conn.close()
    return itens

def remover_do_carrinho(carrinho_id):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('SELECT produto_id, quantidade FROM carrinho WHERE id = ?', (carrinho_id,))
    item = c.fetchone()
    if item:
        produto_id, quantidade = item
        c.execute('DELETE FROM carrinho WHERE id = ?', (carrinho_id,))
        c.execute('UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?', (quantidade, produto_id))
        conn.commit()
    conn.close()

def calcular_total():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''
        SELECT SUM(produtos.preco * carrinho.quantidade)
        FROM carrinho
        JOIN produtos ON carrinho.produto_id = produtos.id
    ''')
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0.0

# Função para simular a finalização da compra
def finalizar_compra():
    total = calcular_total()
    if total > 0:
        print(f"O total da sua compra é: R$ {total:.2f}")
        # Aqui você poderia implementar a lógica de pagamento
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute('DELETE FROM carrinho')
        conn.commit()
        conn.close()
        print("Compra finalizada com sucesso!")
    else:
        print("Seu carrinho está vazio.")

# Interface de usuário simples
def interface_usuario():
    inicializar_banco()
    while True:
        print("\nOpções:")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Remover Produto")
        print("4. Atualizar Produto")
        print("5. Adicionar ao Carrinho")
        print("6. Listar Carrinho")
        print("7. Remover do Carrinho")
        print("8. Finalizar Compra")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Digite o nome do produto: ")
            preco = float(input("Digite o preço do produto: "))
            quantidade = int(input("Digite a quantidade do produto: "))
            adicionar_produto(nome, preco, quantidade)
            print(f"Produto '{nome}' adicionado com sucesso.")

        elif opcao == '2':
            produtos = listar_produtos()
            print("Produtos disponíveis:")
            for produto in produtos:
                print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço: R$ {produto[2]:.2f}, Quantidade: {produto[3]}")

        elif opcao == '3':
            produto_id = int(input("Digite o ID do produto a ser removido: "))
            remover_produto(produto_id)
            print(f"Produto com ID '{produto_id}' removido com sucesso.")

        elif opcao == '4':
            produto_id = int(input("Digite o ID do produto a ser atualizado: "))
            nome = input("Digite o novo nome do produto: ")
            preco = float(input("Digite o novo preço do produto: "))
            quantidade = int(input("Digite a nova quantidade do produto: "))
            atualizar_produto(produto_id, nome, preco, quantidade)
            print(f"Produto com ID '{produto_id}' atualizado com sucesso.")

        elif opcao == '5':
            produto_id = int(input("Digite o ID do produto a ser adicionado ao carrinho: "))
            quantidade = int(input("Digite a quantidade desejada: "))
            adicionar_ao_carrinho(produto_id, quantidade)
            print(f"Produto com ID '{produto_id}' adicionado ao carrinho.")

        elif opcao == '6':
            itens = listar_carrinho()
            print("Itens no carrinho:")
            for item in itens:
                print(f"Produto: {item[0]}, Preço: R$ {item[1]:.2f}, Quantidade: {item[2]}")

        elif opcao == '7':
            carrinho_id = int(input("Digite o ID do item a ser removido do carrinho: "))
            remover_do_carrinho(carrinho_id)
            print(f"Item com ID '{carrinho_id}' removido do carrinho.")

        elif opcao == '8':
            finalizar_compra()

        elif opcao == '9':
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executar a interface do usuário
interface_usuario()
