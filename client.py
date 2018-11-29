import socket
import sys
import re

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = sys.argv[1]
  port = int(sys.argv[2])
  s.connect((host, port))

  while(1):
    msg = input()

    if(msg == ''):
      continue

    if re.match(r"/+", msg):
      if re.match(r"/quit+", msg):
        s.close()
        break
      else:
        print('Invalid command')

    msg = msg.encode('UTF-8')

    while(len(msg) > 1024):
      s.send(msg[:1024])
      msg = msg[1024:]
      data = s.recv(1024)
      print(data.decode('UTF-8'))
      print('received', len(data), 'bytes')


    else:
      s.sendall(msg)
      data = s.recv(1024)
      print(data.decode('UTF-8'))
      print('received', len(data), 'bytes')

  s.close()

if __name__ == '__main__':
  main()
