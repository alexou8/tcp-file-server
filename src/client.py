import socket
import os

HOST = "127.0.0.1"
PORT = 1234

def start_client():
    try:
        # used to create TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # Used for initial Server Message
            # Used for temporary timeout for when server is full
            s.settimeout(1.0)
            try:
                initial_msg = s.recv(1024).decode().strip()
                if initial_msg:
                    print(initial_msg)
                    if "Server full" in initial_msg:
                        # Exits when server is full
                        return
            except socket.timeout:
                pass
            finally:
                # Used to reset timeout for normal operations
                s.settimeout(None)
            
            print(f"Connected to the server at {HOST}:{PORT}")

            # Main Loop for client interaction
            while True:
                msg = input("> ").strip()
                if not msg:
                    continue

                s.send(msg.encode())

                # Used to handle exit command
                if msg.lower() == "exit":
                    response = s.recv(1024).decode()
                    print(response)
                    break

                # Used to handle File download command
                if msg.lower().endswith(".txt") or msg.lower().endswith(".pdf"):
                    # Read the short header first: b"OK\n" or b"ERR\n"
                    # Small, arrives in one go
                    header = s.recv(4) 
                    if not header:
                        print("Server closed the connection.")
                        break
                    if header.startswith(b"ERR"):
                        print(f"ERROR: File '{msg}' not found in repository.")
                        continue

                    # OK case: save the file (first bytes were just "OK\n")
                    filename = msg
                    with open(filename, "wb") as f:
                        while True:
                            chunk = s.recv(4096)
                            # Check if transfer is down or empty chunk
                            if not chunk or chunk.endswith(b"EOF"):
                                if chunk.endswith(b"EOF"):
                                    # Write everything except the EOF marker
                                    f.write(chunk[:-3])  
                                break
                            f.write(chunk)
                    print(f"File '{filename}' downloaded successfully.")
                    continue

                # Used to handle other commands 
                data = s.recv(4096)
                if not data:
                    print("Server closed the connection.")
                    break
                print(data.decode())

    except ConnectionRefusedError:
        print("Connection failed. Check if the server is running.")
    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    start_client()
