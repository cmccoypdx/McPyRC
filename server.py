#!/usr/bin/python3

import socket
import sys
import select
import re

def main():
  chanlist = { '#main': [] }
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = ''
  port = int(sys.argv[1])
  server.bind((host, port))

  server.listen(5)
  input = [server]
  members = {}
  
  while(1):
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

      if s == server:
        conn, addr = s.accept()
        #print('client is at', addr)
        nick = conn.recv(64).decode('UTF-8')
        input.append(conn)
        chanlist['#main'].append(conn)
        members[conn] = [nick, '#main']
        print(nick, ' has joined')
        for r in chanlist['#main']:
          r.sendall((nick + ' has joined').encode('UTF-8'))

      else:
        data = s.recv(1024)
        if not data:
          break
        msg = data.decode('UTF-8')
        if re.match(r"/+", msg):
          if re.match(r"/quit+", msg):
            s.close()
            input.remove(s)
            del members[s]
            for chan in chanlist:
              if s in chanlist[chan]:
                chanlist[chan].remove(s)
          elif re.match(r"/join+", msg):
            msg = msg[6:]
            if msg in chanlist:
              chanlist[msg].append(s)
            else:
              chanlist[msg] = [s]
            print(chanlist)
          elif re.match(r"/leave+", msg):
            msg = msg[7:]
            if msg in chanlist:
              chanlist[msg].remove(s)
            print(chanlist)
          elif re.match(r"/list", msg):
            msg = msg[6:]
            inChan = []
            for m in chanlist[msg]:
              inChan.append(members[m][0])
            response = ', '.join(inChan)
            s.sendall(response.encode('UTF-8'))
          elif re.match(r"/switch", msg):
            print(msg)
            msg = msg[8:]
            print(msg)
            members[s][1] = msg
        else:
          chan = members[s][1]
          for r in chanlist[chan]:
                r.sendall(data)
if __name__ == '__main__':
  main()
