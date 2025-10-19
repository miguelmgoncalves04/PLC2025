import json
import os




STOCK = "stock.json"

def carregar_stock():
    if os.path.exists(STOCK):
        with open(STOCK, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []
    
def gravar_stock(stock):
    with open(STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=2, ensure_ascii=False)


def listar(stock):
    print("Vending:\n Código | Nome | Quantidade | Preço")
    print("*********************************************")
    for item in stock:
        print(f"{item['cod']:>3} | {item['nome']:<20} | {item['quant']:>3} | {item['preco']:.2f}€")

def inserir_moedas(saldo, comando):
    # Exemplo: "MOEDA 1e, 20c, 5c" ou "MOEDA 1E, 20C, 5C"
    texto = comando.upper().replace("MOEDA", "")
    moedas = [m.strip() for m in texto.split(",") if m.strip()]
    for m in moedas:
        # aceitar formatos como '1E', '20C', '0.5E' ou '50C'
        if m.endswith("E"):
            valor_str = m[:-1].strip()
            try:
                saldo += float(valor_str)
            except ValueError:
                print(f"maq: Moeda inválida: '{m}' ignorada")
        elif m.endswith("C"):
            valor_str = m[:-1].strip()
            try:
                saldo += float(valor_str) / 100
            except ValueError:
                print(f"maq: Moeda inválida: '{m}' ignorada")
        else:
            try:
                if valor_int := int(m):
                    saldo += valor_int / 100
            except Exception:
                if m:
                    print(f"maq: Moeda com formato desconhecido: '{m}' ignorada")
    return round(saldo, 2)

def selecionar(stock, codigo, saldo):
    for item in stock:
        if item["cod"].upper() == codigo.upper():
            if item["quant"] == 0:
                print(f'maq: O produto "{item["nome"]}" está esgotado.')
                return saldo
            if saldo >= item["preco"]:
                item["quant"] -= 1
                saldo -= item["preco"]
                print(f'maq: Pode retirar o produto dispensado "{item["nome"]}"')
            else:
                falta = round(item["preco"] - saldo, 2)
                print("maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {saldo:.2f}€; Pedido = {item['preco']:.2f}€ (Faltam {falta:.2f}€)")
            return round(saldo, 2)
    print("maq: Produto inexistente.")
    return saldo

def calcular_troco(valor):
    moedas = [2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    troco = []
    for m in moedas:
        qtd = int(valor // m)
        if qtd > 0:
            troco.append((qtd, m))
            valor = round(valor - qtd * m, 2)
    return troco

def mostrar_troco(saldo):
    troco = calcular_troco(saldo)
    if troco:
        troco_str = ", ".join([f"{q}x {int(m*100)}c" if m < 1 else f"{q}x {int(m)}e" for q, m in troco])
        print(f"maq: Pode retirar o troco: {troco_str}.")
    else:
        print("maq: Sem troco a devolver.")



#FUNÇAO EXTRA PARA ADICIONAR PRODUTOS
def adicionar_produto(stock):
    cod = input("Código do produto: ").strip().upper()
    nome = input("Nome do produto: ").strip()
    quant = int(input("Quantidade: "))
    preco = float(input("Preço (€): "))
    for item in stock:
        if item["cod"] == cod:
            item["quant"] += quant
            item["preco"] = preco
            print(f"maq: Produto {cod} atualizado.")
            return
    stock.append({"cod": cod, "nome": nome, "quant": quant, "preco": preco})
    print(f"maq: Produto {cod} adicionado.")



def main():
    stock = carregar_stock()
    saldo = 0.0

    print("maq: 2024-03-08, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while True:
        cmd = input(">> ").strip().upper()

        if cmd.startswith("LISTAR"):
            listar(stock)
        elif cmd.startswith("MOEDA"):
            saldo = inserir_moedas(saldo, cmd)
            euros = int(saldo)
            cent = int(round((saldo - euros) * 100))
            print(f"maq: Saldo = {euros}e{cent:02d}c")
        elif cmd.startswith("SELECIONAR"):
            partes = cmd.split()
            if len(partes) >= 2:
                saldo = selecionar(stock, partes[1], saldo)
                euros = int(saldo)
                cent = int(round((saldo - euros) * 100))
                print(f"maq: Saldo = {euros}e{cent:02d}c")
            else:
                print("maq: Comando inválido. Use: SELECIONAR <CÓDIGO>")
        elif cmd.startswith("ADICIONAR"):
            adicionar_produto(stock)
        elif cmd.startswith("SAIR"):
            mostrar_troco(saldo)
            print("maq: Até à próxima")
            gravar_stock(stock)
            break
        else:
            print("maq: Comando desconhecido. Use LISTAR, MOEDA, SELECIONAR ou SAIR.")

if __name__ == "__main__":
    main()