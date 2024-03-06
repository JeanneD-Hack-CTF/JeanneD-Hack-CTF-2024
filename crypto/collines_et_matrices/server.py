#!/usr/bin/python3

import datetime
import numpy as np
import signal
import socket
import string
import sys

from _thread import *

# Crypto constants and functions

FLAG = "verybeautifulcipherbutsoeasytobreak"
ALPHABET = string.ascii_lowercase[:-1] 
SIZE = len(ALPHABET)

KEY_MATRIX = np.array([
    [23,  3,  5,  7, 16],
    [22, 15,  0, 14, 19],
    [ 6,  8, 12, 21,  1],
    [17, 13, 20, 24,  4],
    [ 9, 18, 10, 11,  2]
], dtype=int)
DIM = 5

# Encrypt a message with a key using Hill Cipher
def encrypt(msg: str, key: np.array):
    splitted = [msg[i:i + DIM] for i in range(0, len(msg), DIM)]
    encrypted = ''
    a = ord('a')
    for chunk in splitted:
        chunk += 'a' * (DIM - len(chunk))
        vect = np.array([ord(c) - a for c in chunk])
        encrypted += ''.join([ALPHABET[m % SIZE] for m in key.dot(vect)])
    return encrypted


WELCOME = """Bienvenue, voici le message à déchiffrer : %s
Pour vous aider, un oracle est à votre disposition pour chiffrer vos messages.
"""

# Server and socket logic

SOCKET_HOST = "0.0.0.0"
SOCKET_PORT = 50001

def serverlog(msg, outfile=None):
    if outfile:
        outfile.write(f"\n[{datetime.datetime.now()}] {msg}")
    else:
        print(f"[{datetime.datetime.now()}] {msg}")

# Handle clients connections and encrypt received messages
def client_handler(connection, client):
    ciphertext = encrypt(FLAG, KEY_MATRIX)
    connection.send((WELCOME % ciphertext).encode())

    while True:
        try: 
            connection.send("\nEntrer le message que vous souhaitez chiffrer : ".encode())
            msg = connection.recv(1024).decode()[:-1] # Remove trailing newline
            serverlog(f"Message received from {client}: {msg}")

            if not all(c.islower() for c in msg):
                err = "Votre message ne peut contenir que des lettres minuscules !\n"
                connection.send(err.encode())
            
            elif not all(c in ALPHABET for c in msg):
                err = "Caractère invalide\n"
                connection.send(err.encode())
            
            else:
                ct = f"Message chiffré : {encrypt(msg, KEY_MATRIX)}\n"
                connection.send(ct.encode())

        except (ConnectionResetError, BrokenPipeError):
            serverlog(f"Client {client} closed connection")
            break
    
    connection.close()

# Accept a connection to the server and start a new thread
def accept_connections(socket_server):
    conn, address = socket_server.accept()
    client = f"{address[0]}:{address[1]}"
    serverlog(f"Connection from: {client}")
    start_new_thread(client_handler, (conn, client))

# Handle Ctrl+C
def handler(signum, frame):
    serverlog("Ctrl+C received: stopping the server")
    sys.exit(0)

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SOCKET_HOST, SOCKET_PORT))
    server.listen(5)
    
    serverlog("Jeanned'Hack CTF - Collines & Matrices")
    serverlog(f"Server start listening at: {SOCKET_HOST}:{SOCKET_PORT}")
    signal.signal(signal.SIGINT, handler)

    while True:
        accept_connections(server)
    
    serverlog("Server stop")


if __name__ == "__main__":
    start_server()
