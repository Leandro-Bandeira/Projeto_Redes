
from Client_udp import Client_udp
from Server_udp import Server_udp

# Função responsável pela interação com o usuário
def main():
    
    choice = int(input("""Escolha um dos tipos de requisição:
    1. Data e hora atual.
    2. Uma mensagem motivacional para o fim do semestre.
    3. A quantidade de respostas emitidas pelo servidor até o momento.
    4. Sair
    """))

    if choice == 4:
        exit(1)

    client = Client_udp()
    client.send_request(choice)
    
















if __name__ == "__main__":
    main()
