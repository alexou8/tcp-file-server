import socket
import threading
import datetime
import os
import time

# ---------------- Config ---------------- #
HOST = "127.0.0.1"  # local
PORT = 1234
CLIENTS = 3
REPO_DIREC = os.path.join(os.getcwd(), "server_dir")
# ---------------------------------------- #

# Store client connection histories with timestamps
client_cache = []

# Thread lock to prevent race conditions during multiple client access
lock = threading.Lock()

# List of client IDs assigned on new connections
available_ids = []

for i in range(1, CLIENTS + 1):
    available_ids.append(f"Client{i:02d}")

def client_comm(conn, add, client_name):
    conn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with lock:
        client_cache.append({"name": client_name, "connected": conn_time,
            "disconnected": None
        })
        print(f"[Server] {client_name} connected at {conn_time} from {add}")
    
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            # Used for Exit command
            if data.lower() == "exit":
                conn.send(f"{client_name} connection terminated.".encode())
                break

            # Used for Status command
            elif data.lower() == "status":
                with lock:
                    status = "\n".join([
                        f"{rec ['name']}: Connected = {rec['connected']}, Disconnected = {rec['disconnected']}"
                        for rec in client_cache
                    ])
                conn.send(status.encode())

            # Used for List command 
            elif data.lower() == "list":
                files = os.listdir(REPO_DIREC)
                conn.send("\n".join(files).encode())

            # Used for File transfer
            elif data.lower().endswith((".txt", ".pdf")):
                path = os.path.join(REPO_DIREC, data)
                if not os.path.isfile(path):
                    conn.sendall(b"ERR\n")
                else:
                    conn.sendall(b"OK\n")
                    with open(path, "rb") as f:
                        # File will be sent in chunks to handle large files
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            conn.sendall(chunk)
                    # send end marker so client knows transfer is complete
                    conn.sendall(b"EOF")
                    print(f"[File Transfer] {data} sent to {client_name}")

            # Used to Echo / Normal message
            else:
                conn.send(f"{data} ACK".encode())

    except Exception as e:
        print(f"[Error] Something went wrong with {client_name}: {e}")

    finally:
        disconn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with lock:
            for record in client_cache:
                if record["name"] == client_name and record["disconnected"] is None:
                    record["disconnected"] = disconn_time
                    break
            print(f"[Server] {client_name} disconnected at {disconn_time}")

            # Free up this ID for reuse
            available_ids.append(client_name)
            # Keep them in order (Client01, 02, 03)
            available_ids.sort()  

        conn.close()

def run_server():

    print("[Server] TCP Server starting")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(CLIENTS)
    print(f"[Server] Listening on {HOST}:{PORT}")

    while True:
        connectionSocket, addr = serverSocket.accept()

        with lock:
            if len(available_ids) == 0:
            # When all slots are full reject new connections
                print(f"[Server] Refused connection from {addr} (server full)")
                try:
                    connectionSocket.send(b"Server full, please wait and try again")
                except Exception:
                    pass
                connectionSocket.close()
                continue

        clientName = available_ids.pop(0)
        print(f"[Server] Accepting {clientName} from {addr}")

        try:    
            connectionSocket.send(f"Connection successful, you are {clientName}\n".encode())

            threading.Thread(target=client_comm, args=(connectionSocket, addr, clientName)).start()

        except Exception as e:
            print(f"[Error] Failed to connection to server on {clientName}: {e}")
            connectionSocket.close()
        

if __name__ == "__main__":
    run_server()
