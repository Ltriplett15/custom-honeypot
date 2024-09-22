import socket
import threading
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_handler = RotatingFileHandler("honeypot.log", maxBytes=1000000, backupCount=5)
logging.basicConfig(handlers=[log_handler], level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# FTP service handler
def handle_ftp_client(client_socket):
    try:
        logging.info(f"Accepted FTP connection from {client_socket.getpeername()}")
        client_socket.send(b"220 Welcome to the vulnerable FTP server\r\n")

        while True:
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break

            logging.info(f"FTP Received: {request}")
            if request.startswith("USER"):
                client_socket.send(b"331 Password required for user\r\n")
            elif request.startswith("PASS"):
                client_socket.send(b"230 User logged in, proceed\r\n")
            else:
                client_socket.send(b"500 Command not understood\r\n")

    except Exception as e:
        logging.error(f"Error handling FTP client: {e}")
    finally:
        client_socket.close()

# SSH service handler
def handle_ssh_client(client_socket):
    try:
        logging.info(f"Accepted SSH connection from {client_socket.getpeername()}")
        client_socket.send(b"SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7\r\n")
        request = client_socket.recv(1024).decode('utf-8').strip()
        logging.info(f"SSH Received: {request}")

    except Exception as e:
        logging.error(f"Error handling SSH client: {e}")
    finally:
        client_socket.close()

# FTP server function
def honeypot_ftp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 21))  # FTP default port 21
    server.listen(5)
    logging.info("FTP Honeypot started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"FTP Connection from {addr}")
        client_handler = threading.Thread(target=handle_ftp_client, args=(client_socket,))
        client_handler.start()

# SSH server function
def honeypot_ssh_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 22))  # SSH default port 22
    server.listen(5)
    logging.info("SSH Honeypot started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"SSH Connection from {addr}")
        client_handler = threading.Thread(target=handle_ssh_client, args=(client_socket,))
        client_handler.start()

# Main function to start both services
def start_honeypot():
    ftp_thread = threading.Thread(target=honeypot_ftp_server)
    ftp_thread.start()

    ssh_thread = threading.Thread(target=honeypot_ssh_server)
    ssh_thread.start()

if __name__ == "__main__":
    start_honeypot()
