import socket
import random


UDP_IP = '15.228.191.109'
UDP_PORT = 50000

# Classe responsável pelo cliente udp
class Client_udp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Criação do socket UDP
    
    # Função responsável por enviar a requisição para o servidor
    def send_request(self, type):
        # Analisa o que o usuário deseja
        # Perceba que a notação utilizada é big endian, o mais significativo está a esquerda
        # 00000000 (0x00)- Data e hora
        # 00000001 (0x01)- Uma mensagem motivacional para o fim do semestre
        # 00000010 (0x02)- A quantidade de respostas emitidas pelo servidor até o momento. 
        type_request = None 
        if type == 1:
            type_request = b'\x00' 
        elif type == 2:
            type_request = b'\x01' 
        else:
            type_request = b'\x02'

        id = random.randint(1, 65535).to_bytes(2, "big") #Gera o numero aleatorio e o converte para bytes no padrão big endian
        msg = type_request + id # Concatena as informações 
        self.sock.sendto(msg, (UDP_IP, UDP_PORT)) #Envia as mensagens UDP para o servidor
        data, addr = self.sock.recvfrom(1024)
        
        # Para cada valor inteiro, transforma-o em ascii a partir do quarto byte que começa a mensagem
        # até o final
        if type != 3:
            msg_rcv = str(data[4:-1].decode("ascii")).rstrip()
        else:
            msg_rcv = int.from_bytes((data[4:]), "big")
            
        print(msg_rcv)
