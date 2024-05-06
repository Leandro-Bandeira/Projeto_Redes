
from Client_udp import Client_udp
from client_raw import Client_raw

# Função responsável pela interação com o usuário
def main():

    choice_client = int(input("""Escolha um dos tipos de cliente:
        1. Cliente UDP.
        2. Cliente RAW.
        """))

    if choice_client == 1: 

        while(1):    
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


    else: 
        while(1):    
            choice = int(input("""Escolha um dos tipos de requisição:
            1. Data e hora atual.
            2. Uma mensagem motivacional para o fim do semestre.
            3. A quantidade de respostas emitidas pelo servidor até o momento.
            4. Sair
            """))

            if choice == 4:
                exit(1)

            client = Client_raw()
            client.send_request(choice)

    
        

if __name__ == "__main__":
    main()
