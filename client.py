import socket
import sys

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = sys.argv[1]
  port = int(sys.argv[2])
  s.connect((host, port))

  msg = sys.argv[3].encode('UTF-8')

  s.sendall(msg)

  while(1):
    data = s.recv(1000000)
    print(data.decode('UTF-8'))
    if not data:
      break
    print('received', len(data), 'bytes')

  s.close()

if __name__ == '__main__':
  main()
