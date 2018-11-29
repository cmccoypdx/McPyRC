import socket
import sys

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = ''
  port = int(sys.argv[1])
  s.bind((host, port))

  s.listen(5)
  while(1):
    conn, addr = s.accept()
    print('client is at', addr)

    while(1): 
      data = conn.recv(1024)
      #data = data * 1000
      if not data:
        break
      conn.sendall(data)
  #conn.close()

if __name__ == '__main__':
  main()
