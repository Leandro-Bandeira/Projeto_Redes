import socket
import random


UDP_IP = '15.228.191.109'
UDP_PORT = 50000

# Classe responsável pelo cliente udp
class Client_udp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Criação do socket UDP
        #self.type_msg = 0b0000 # Valor do tipo da mensagem (requisição)
        self.type_msg = format(0, '04b')
        print(self.type_msg)
    # Função responsável por enviar a requisição para o servidor
    def send_request(self, type):
        
        #Análisa o que o usuário deseja
        # 1 Data e hora
        # 2 Uma mensagem motivacional para o fim do semestre
        # 3 A quantidade de respostas emitidas pelo servidor até o momento. 
        type_request = None 
        if type == 1:
            #type_request = 0b0000
            type_request = format(0, '04b')
        elif type == 2:
            #type_request = 0b0001
            type_request = format(1, '04b')
        else:
            #type_request = 0b0010
            type_request = format(2, '04b')

        id = format(random.randint(1, 65535), '016b') # Gera valores aleatores entre os intervalos dados inclusivos
        msg_string = self.type_msg + type_request + id
        msg = int(msg_string, 2).to_bytes(-(-len(msg_string) // 8), byteorder='big') # Cria um byte-object para enviar como mensagem
        print(msg)
        #print(msg.decode('ascii'))
         
        #self.sock.sendto(b'\x00\x37\x51', (UDP_IP, UDP_PORT))
        self.sock.sendto(msg, (UDP_IP, UDP_PORT))
        data, addr = self.sock.recvfrom(1024)
    
        print(f'Received message: {data}')

