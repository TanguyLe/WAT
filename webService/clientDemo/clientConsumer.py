#!/usr/bin/python

from websocket import create_connection

ws = create_connection("ws://localhost:8080/users/1/positionsGetter")

print("You started the consumer, he will tell you about any change of the user1's position")
while 1:
    print("I'm receiving indefinitely !")
    newPosition = ws.recv()
    print("Position on webService is : " + newPosition)
