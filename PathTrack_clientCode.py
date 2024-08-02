import socket
import time

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    print("Connected to the server for sending PathIDs.")

    while True:
        try:
            path_ids = input("Enter PathID(s) to highlight (comma-separated): ")
            client_socket.sendall(path_ids.encode())
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error sending data: {e}")
            break

    client_socket.close()

start_client()
