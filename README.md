# Python TCP File Server — Multithreaded Client–Server System

Python TCP File Server is a socket-based client–server application that enables **concurrent client
connections**, **command-based communication**, and **file transfer** over TCP using Python’s
standard library.

An end-to-end networking system that:
- establishes TCP connections between clients and a server
- manages multiple clients concurrently using threads
- implements a lightweight application-layer command protocol
- supports file discovery and file downloads from a server repository
- tracks client connection history with timestamps

## ⚠️ Disclaimer
- This project is for **educational and demonstrative purposes only**.
- It is not intended for production use without additional security, authentication, and error handling.
- File transfer and protocol design are simplified for clarity and learning purposes.

## Key Features
- TCP socket communication using Python’s `socket` module
- Multithreaded server (thread-per-client architecture)
- Concurrent client connection handling with capacity limits
- Command-based protocol:
  - `list` – list files available on the server
  - `status` – view client connection history
  - `<filename>.txt / <filename>.pdf` – download files
  - `exit` – gracefully disconnect
- Chunked file transfer for text and PDF files
- Client identification and connection timestamp logging
- Clean separation of client and server logic

## Project Structure
- src/  
  - server.py — multithreaded TCP server  
  - client.py — TCP client  
- server_dir/ — repository of downloadable files  
- docs/ — optional demo assets (screenshots / GIFs)  
- .gitignore  
- LICENSE  
- README.md  
- requirements.txt  

## System Design Overview
- **Architecture:** TCP client–server model
- **Concurrency Model:** Thread-per-client
- **Protocol Type:** Custom text-based application-layer protocol
- **Transport Layer:** TCP (reliable, ordered delivery)

### Server Responsibilities
- Accept incoming client connections
- Enforce a maximum concurrent client limit
- Spawn a dedicated thread per connected client
- Parse and respond to client commands
- Stream requested files in fixed-size chunks
- Maintain connection history and client metadata

### Client Responsibilities
- Establish a TCP connection to the server
- Send user-issued commands
- Receive and display server responses
- Handle file downloads and local storage
- Gracefully terminate connections

## Networking Details
- **Socket Type:** `AF_INET`, `SOCK_STREAM`
- **Blocking I/O:** Used for simplicity and clarity
- **File Transfer:** Chunked transmission with application-level termination marker
- **Thread Safety:** Shared server state protected during updates

## Impact & Results
- **Concurrency Handling:** Successfully supported multiple simultaneous clients without blocking or message interleaving.
- **Protocol Design:** Designed and implemented a custom command protocol on top of TCP, reinforcing understanding of application-layer networking.
- **File Transfer Reliability:** Enabled stable transfer of text and binary files using chunked reads over persistent TCP connections.
- **Operational Visibility:** Implemented connection tracking to monitor client lifecycle events (connect/disconnect timestamps).
- **Systems Knowledge:** Strengthened understanding of socket lifecycles, blocking I/O behavior, and multithreaded server design.

## Tech Stack
- **Language:** Python  

- **Networking:**  
  - `socket` — TCP communication  

- **Concurrency:**  
  - `threading` — concurrent client handling  

- **File & System Utilities:**  
  - `os` — filesystem operations  
  - `datetime` — connection timestamp tracking  

- **Development Practices:**  
  - Clear separation of client/server responsibilities  
  - Modular, readable code structure  
  - No external dependencies (stdlib only)

## Quickstart
### 1) Clone the repository
git clone <your-repo-url>
cd python-tcp-file-server

### 2) Start the server
python src/server.py

### 3) Start a client (in a new terminal)
python src/client.py

## Client Commands
| Command    | Description                         |
| ---------- | ----------------------------------- |
| `list`     | Lists files available on the server |
| `status`   | Displays client connection history  |
| `file.txt` | Downloads a text file               |
| `file.pdf` | Downloads a PDF file                |
| `exit`     | Disconnects from the server         |

