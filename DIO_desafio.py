
def menu():
    print("""
--------------------------
     BANCO S.R.F.R.S
--------------------------
    1. DEPÓSITO
    2. SAQUE
    3. EXTRATO
    0. SAIR 
    """)
    escolha = int(input("Selecione a opção desejada: "))

    return escolha

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso ===")
    else:
        print("\n OPERAÇÃO FALHOU! O VALOR INFORMADO É INVÁLIDO.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n OPERAÇÃO FALHOU! VOCÊ NÃO TEM SALDO SUFICIENTE.")

    elif excedeu_limite:
        print("\n OPERAÇÃO FALHOU! O VALOR DO SAQUE EXCEDE O LIMITE.")

    elif excedeu_saques:
        print("\n OPERAÇÃO FALHOU! NÚMERO DE SAQUES EXCEDIDO.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n OPERAÇÃO FALHOU! O VALOR INFORMADO É INVÁLIDO.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("  Não existem movimentações" if not extrato else extrato)
    print(f" \nSaldo:\t\tR$ {saldo:.2f}")
    print("=============================")


def main():
    limite_saques = 3
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    while True:
        opcao = menu()

        if opcao == 1:
            valor = float(input("Informe o valor que deseja depositar: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 2:
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=limite_saques,
            )

        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 0:
            print("Encerrando o programa...")
            break
        else:
            print("OPERAÇÃO INVÁLIDA! TENTE NOVAMENTE.")


main()