#!/usr/bin/env python3

import sys
import socket
import selectors
import types

#messages = [b"Message 1 from client.", b"Message 2 from client."]
#cmd = bytes("{}".format(" ".join(sys.argv[1:])), "utf-8")
#messages = [cmd]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.recv_total += len(recv_data)
            reply = recv_data.decode("utf-8")
            print(f"Received '{reply}' from connection {data.connid}".replace("\0", ""))
            if reply.endswith("\0"):
                print(f"Closing connection {data.connid}")
                sel.unregister(sock)
                sock.close()
        if not recv_data:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


#if len(sys.argv) != 4:
#    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
#    sys.exit(1)
#
#host, port, num_conns = sys.argv[1:4]
default_port = 4711

host = input("Target ip: ")
port = input(f"Confirm default port {default_port} with enter or provide port to use: ")
if port == "":
    port = default_port
print(f"Server on {host}:{port}\n")
    
num_conns = 1

while True:

    sel = selectors.DefaultSelector()
    cmd = bytes(input("Command: "), "utf-8")
    messages = [cmd]
    start_connections(host, int(port), int(num_conns))
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

