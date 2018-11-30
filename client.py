#!/usr/bin/python3

import socket
import sys
import re
import threading

keepListening = True

class listenThread (threading.Thread):
  def __init__(self, s):
    threading.Thread.__init__(self)
    self.s = s
  def run(self):
    while(keepListening):
      data = self.s.recv(1024)
      print(data.decode('UTF-8'))
      #print('received', len(data), 'bytes')

class sendThread (threading.Thread):
  def __init__(self, s):
    threading.Thread.__init__(self)
    self.s = s
  def run(self):
    s = self.s
    global keepListening
    while(keepListening):
      msg = input()

      if(msg == ''):
        continue

      if re.match(r"/+", msg):
        if re.match(r"/quit+", msg):
          s.sendall('/quit'.encode('UTF-8'))
          keepListening = False
          s.close()
          break
        elif re.match(r"/join", msg):
          s.sendall(msg.encode('UTF-8'))
          continue
        elif re.match(r"/leave", msg):
          s.sendall(msg.encode('UTF-8'))
          continue
        elif re.match(r"/list", msg):
          s.sendall(msg.encode('UTF-8'))
          continue
        else:
          print('Invalid command')
          continue

      msg = msg.encode('UTF-8')

      while(len(msg) > 1024):
        s.send(msg[:1024])
        msg = msg[1024:]

      s.sendall(msg)
  
def main():
  keepListening = True
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  nick = input("Please enter nickname: ")
  host = sys.argv[1]
  port = int(sys.argv[2])
  s.connect((host, port))
  s.sendall(nick.encode('UTF-8'))

  listen = listenThread(s)
  send = sendThread(s)
  listen.start()
  send.start()
  listen.join()
  send.join()
  
if __name__ == '__main__':
  main()
