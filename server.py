import socket
import sys
import select
import re

def main():
  chanlist = { 'main': [] }
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = ''
  port = int(sys.argv[1])
  server.bind((host, port))

  server.listen(5)
  input = [server]
  
  while(1):
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

      if s == server:
        conn, addr = s.accept()
        print('client is at', addr)
        input.append(conn)
        chanlist['main'].append(conn)

      else:
        #while(1): 
        data = s.recv(1024)
          #data = data * 1000
        if not data:
          break
        msg = data.decode('UTF-8')
        if re.match(r"/+", msg):
          if re.match(r"/quit+", msg):
            s.close()
            input.remove(s)
          elif re.match(r"/join+", msg):
            msg = msg[6:]
            if msg in chanlist:
              chanlist[msg].append(s)
            else:
              chanlist[msg] = [s]
          print(chanlist)
        else:
          s.sendall(data)
  #conn.close()

if __name__ == '__main__':
  main()
