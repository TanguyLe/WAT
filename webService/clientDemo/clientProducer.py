#!/usr/bin/python

from websocket import create_connection
from time import sleep

ws = create_connection("ws://localhost:8080/users/1/positionsSender")
position = 0

print("You started the producer, he will change the user1's position every 2 seconds !")
while 1:
    sleep(2)
    position += 1
    print("I'm moving the user1 regularly !")
    print("Moving to " + str(position))
    ws.send(str(position))
