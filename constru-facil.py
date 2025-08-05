produtos = []
vendas = []
estoque = {}
comissoes = {}

def salvar_relatorio():
    linhas = []
    linhas.append("RELATÓRIO Das VENDAS - LOJA CONSTRUÇÃO FÁCIL\n")
    linhas.append("-" * 50 + "\n")

    linhas.append("\nVENDAS FeitAS:\n")
    for v in vendas:
        linha = (f"{v['produto']} | {v['quantidade']} un | R${v['valor_total']:.2f} | "
                 f"Vendedor: {v['vendedor']} | Pagamento: {v['forma_pagamento']}\n")
        linhas.append(linha)

    linhas.append("\nCOMISSÕES do VENDEDOR:\n")
    for nome, valor in comissoes.items():
        linha = f"{nome}: R${valor:.2f}\n"
        linhas.append(linha)

    linhas.append("\nPRODUTOS COM ESTOQUE ABAIXO DO MÍNIMO:\n")
    for prod in produtos:
        nome = prod["nome"]
        if estoque[nome] < prod["estoque_min"]:
            linha = f"{nome} | Estoque atual: {estoque[nome]} | Mínimo: {prod['estoque_min']}\n"
            linhas.append(linha)

    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.writelines(linhas)

def cadastrar_produto():
    nome = input("Nome do produto: ")

    print("Categoria (elétrica, hidráulica, limpeza, construção)")
    categoria = input("Informe a categoria: ").lower()
    while categoria not in ['elétrica', 'hidráulica', 'limpeza', 'construção']:
        print("Categoria inválida.")
        categoria = input("Informe a categoria: ").lower()

    print("Unidade de medida (unidades, kg, metros)")
    unidade = input("Informe a unidade de medida: ").lower()
    while unidade not in ['unidades', 'kg', 'metros']:
        print("Unidade inválida.")
        unidade = input("Informe a unidade de medida: ").lower()

    preco_custo = float(input("Preço de custo: "))
    preco_venda = float(input("Preço de venda: "))
    quantidade = int(input("Quantidade em estoque: "))
    estoque_min = int(input("Estoque mínimo: "))

    produto = {
        "nome": nome,
        "categoria": categoria,
        "unidade": unidade,
        "preco_custo": preco_custo,
        "preco_venda": preco_venda,
        "estoque_min": estoque_min
    }

    produtos.append(produto)
    estoque[nome] = quantidade

    salvar_relatorio()
    print("Produto cadastrado com sucesso.")
    input("\nPressione Enter para voltar ao menu...")

def listar_produtos():
    print("\n--- Lista de Produtos Cadastrados ---")
    for i, prod in enumerate(produtos, 1):
        print(f"{i}. {prod['nome']} | Categoria: {prod['categoria']} | "
              f"Estoque: {estoque.get(prod['nome'], 0)} {prod['unidade']}")
    input("\nPressione Enter para voltar ao menu...")

def registrar_venda():
    if not produtos:
        print("Nenhum produto cadastrado.")
        input("\nPressione Enter para voltar ao menu...")
        return

    listar_produtos()
    try:
        idx = int(input("\nDigite o número do produto vendido: ")) - 1
        produto = produtos[idx]
    except (ValueError, IndexError):
        print("Produto inválido.")
        input("\nPressione Enter para voltar ao menu...")
        return

    quantidade = int(input("Quantidade vendida: "))
    nome_prod = produto["nome"]

    if estoque[nome_prod] < quantidade:
        print("Estoque insuficiente.")
        input("\nPressione Enter para voltar ao menu...")
        return

    vendedor = input("Nome do vendedor: ")
    forma_pagamento = input("Forma de pagamento (dinheiro, pix, cartao): ").lower()

    aplicar_desconto = input("Deseja aplicar desconto? (s/n): ").lower()
    desconto = float(input("Valor do desconto: ")) if aplicar_desconto == "s" else 0.0

    valor_total = produto["preco_venda"] * quantidade - desconto

    if forma_pagamento == "cartao":
        comissao = 0.03 * valor_total
    elif forma_pagamento in ["dinheiro", "pix"]:
        comissao = 0.05 * valor_total
    else:
        comissao = 0.0

    comissoes[vendedor] = comissoes.get(vendedor, 0) + comissao
    estoque[nome_prod] -= quantidade

    venda = {
        "produto": nome_prod,
        "quantidade": quantidade,
        "valor_unitario": produto["preco_venda"],
        "valor_total": valor_total,
        "vendedor": vendedor,
        "forma_pagamento": forma_pagamento,
        "desconto": desconto
    }
    vendas.append(venda)

    salvar_relatorio()
    print("Venda registrada com sucesso.")
    input("\nPressione Enter para voltar ao menu...")

def relatorio_vendas():
    print("\n--- Relatório de Vendas ---")
    with open("relatorio.txt", "r", encoding="utf-8") as f:
        print(f.read())
    input("\nPressione Enter para voltar ao menu...")

def menu():
    while True:
        print("\n==== MENU LOJA CONSTRUÇÃO FÁCIL ====")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Registrar venda")
        print("4 - Relatório de vendas")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                cadastrar_produto()
            case "2":
                listar_produtos()
            case "3":
                registrar_venda()
            case "4":
                relatorio_vendas()
            case "0":
                print("Encerrando sistema...")
                break
            case _:
                print("Opção inválida.")
                input("\nPressione Enter para voltar ao menu...")

menu()
