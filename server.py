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
        nick = conn.recv(64).decode('UTF-8')
        input.append(conn)
        chanlist['#main'].append(conn)
        members[conn] = [nick, '#main']
        for r in chanlist['#main']:
          r.sendall(('[#main] Server: ' + nick + ' has joined #main').encode('UTF-8'))

      else:
        data = s.recv(1024)
        if not data:
          break
        msg = data.decode('UTF-8')
        if re.match(r"/+", msg):
          if re.match(r"/quit+", msg):
            input.remove(s)
            for chan in chanlist:
              if s in chanlist[chan]:
                chanlist[chan].remove(s)
                for r in chanlist[chan]:
                  r.sendall(('[' + chan + '] Server: ' + members[s][0] + ' has left ' + chan + ' ').encode('UTF-8')) 
            del members[s]
            s.close()
          elif re.match(r"/join+", msg):
            msg = msg[6:]
            if msg in chanlist:
              chanlist[msg].append(s)
            else:
              chanlist[msg] = [s]
            for r in chanlist[msg]:
              r.sendall(('[' + msg + '] Server: ' + members[s][0] + ' has joined ' + msg).encode('UTF-8'))
          elif re.match(r"/leave+", msg):
            msg = msg[7:]
            if msg in chanlist:
              chanlist[msg].remove(s)
              for r in chanlist[msg]:
                r.sendall(('[' + msg + '] Server: ' + members[s][0] + ' has left ' + msg).encode('UTF-8')) 
          elif re.match(r"/listmembers", msg):
            msg = msg[6:]
            inChan = []
            for m in chanlist[msg]:
              inChan.append(members[m][0])
            response = ', '.join(inChan)
            s.sendall(response.encode('UTF-8'))
          elif re.match(r"/list", msg):
            response = ', '.join(chanlist.keys())
            s.sendall(response.encode('UTF-8'))
          elif re.match(r"/switch", msg):
            msg = msg[8:]
            if msg in chanlist:
              members[s][1] = msg
            else:
              s.sendall('No such room. Use /join to create.'.encode('UTF-8'))
        else:
          msg = data.decode('UTF-8')
          chan = members[s][1]
          for r in chanlist[chan]:
            r.sendall(('[' + chan + '] ' + members[s][0] + ': ' + msg).encode('UTF-8'))
if __name__ == '__main__':
  main()
