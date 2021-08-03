#############################################################################
# Program:
#    Lab PythonWebServer, Computer Networks
#    Brother Jones, CSE354
# Author:
#    Mark Kportufe
# Summary:
#   The program is to take a command line argument for the port
#   at which the web server will listen for HTTP requests.
#
###############################################################################
#############################################################################
# fixed the 404 error 
# made the program run and accept all file types
# improved the setup and the code as a whole
# 
#############################################################################
from socket import *
import sys
import os
import mimetypes

# Return proper content type
def contentType(filepath):
   # Based on the file extension, return the content type 
   # that is part  of the "Content-type:" header"
   mimetypes.init()
   return mimetypes.guess_type(filename)[0]

# Server Connection Setup
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("Server is running on port " , str(serverPort))

CRLF = "\r\n"
try:
   # Main Server Loop
   while 1:
      #Accept connection
      connectionSocket, addr = serverSocket.accept()

      #Read request
      try:
         raw_request = connectionSocket.recv(1024).decode('ascii')  # Read the request
      except:
         connectionSocket.send(('404 Not Found').encode(ascii))

      #Isolate the first header from the request
      request_header = raw_request.partition('\n')[0]

      #Break the header into pieces
      array = request_header.split(' ')

      #Initialize items
      status = 'None'
      filename = '/'
      http = ''
      response = ''

      #Try to pull the filename from the request.
      #If no filename is found, return a code 400
      try:
         request_type = array[0]
         filename = (array[1])
         http = array[2]
      except IndexError as error:
         status = '400 Bad Request'
         print(error)

      #Create the content type header
      content_type = ' Content-Type: ' + str(contentType(filename)) + CRLF

      #initialize file data
      raw_data = None

      #Try to find the file
      try:
         f = open('.' + filename, 'rb')
         raw_data = f.read()
         f.close()
         response = '200 OK'
      except EnvironmentError as error:
         #If file wasn't found, return 404 error
          connectionSocket.send(('404 Not Found').encode('ascii'))

      status = 'HTTP/1.1 ' + response + ' ' + CRLF

      #Send header data to client
      connectionSocket.send(status.encode('ascii'))
      connectionSocket.send(content_type.encode('ascii'))
      connectionSocket.send('\n'.encode('ascii'))
      if (raw_data != None):
         connectionSocket.send(raw_data)

   print(' ')
   serverSocket.close()  # Close the connection socket


except KeyboardInterrupt:
   print("\nClosing Server")
   serverSocket.close()
   quit()
