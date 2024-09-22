# **Custom Honeypot**

## **Overview**
This project is a custom honeypot written in Python that simulates vulnerable services (FTP and SSH) to attract and log malicious actors' interactions. The honeypot logs connection attempts, data sent by attackers, and other network interactions for later analysis. It can be used as a learning tool to understand attack patterns and methods in a controlled environment.

---

## **Features**
- **Simulates FTP and SSH Services**: The honeypot creates fake services on commonly attacked ports (21 for FTP and 22 for SSH) to attract potential attackers.
- **Logs Interaction**: Logs all connection attempts, including IP addresses, connection data, and the requests sent by attackers.
- **Multi-threading**: Handles multiple attackers simultaneously by running each connection in a separate thread.
- **Simple Setup**: Easy to deploy on a local machine, server, or cloud instance with minimal configuration.

---

## **Installation**

### **Prerequisites**
- Python 3.x
- Linux-based system (can also run on Windows or MacOS, but Linux is recommended).
- Basic understanding of how to use the terminal.

### **Step-by-Step Instructions**

1. **Clone the repository**:
   Open your terminal and clone the repository to your local machine or server using Git:
   ```bash
   git clone https://github.com/yourusername/custom-honeypot.git
   ```

2. **Navigate into the project directory**:
   ```bash
   cd custom-honeypot
   ```

3. **Install dependencies**:
   Install the required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure ports (optional)**:
   If you want to change the ports the honeypot listens on (default is 21 for FTP and 22 for SSH), you can do so by modifying the script's `bind()` calls in `honeypot.py`.

---

## **Usage**

### **Running the Honeypot**

Once the environment is set up and the required packages are installed, you can run the honeypot using Python:

```bash
sudo python3 honeypot.py
```

The honeypot needs **root** privileges to bind to ports below 1024 (e.g., port 21 and 22). You can either run it using `sudo` or change the ports to higher numbers.

### **Testing the Honeypot Locally**

You can simulate an attack locally using the following commands:

1. **FTP Service Test**:
   Open another terminal window or use a different machine and run:
   ```bash
   telnet <your_honeypot_IP> 21
   ```
   You should see a welcome message like `Welcome to the vulnerable FTP server`.

2. **SSH Service Test**:
   Similarly, for SSH, use the following command:
   ```bash
   ssh <your_honeypot_IP>
   ```
   It will display a fake SSH banner, and whatever you input will be logged.

### **Monitoring Logs**

All activity is logged to the `honeypot.log` file. You can view the logs using:
```bash
tail -f honeypot.log
```

This will display real-time logs of attacker interactions, such as:
```
2024-09-21 14:15:32 - Accepted connection from ('192.168.0.15', 50234)
2024-09-21 14:15:32 - Received: USER admin
2024-09-21 14:15:33 - Received: PASS password123
2024-09-21 14:15:34 - Sent fake login success response.
```

Logs contain:
- Timestamp of the interaction.
- The attacker's IP address and port number.
- The data sent by the attacker.
- The response sent by the honeypot.

---

## **Customization**

### **Adding Additional Services**

You can add more vulnerable services to attract different kinds of attackers. To add new services (e.g., HTTP, SMTP), follow these steps:
1. Open the `honeypot.py` file.
2. Create new handler functions for the services you want to mimic.
3. Bind a new socket to the appropriate port for the new service.

Example for an HTTP honeypot:
```python
def handle_http_client(client_socket):
    try:
        client_socket.send(b"HTTP/1.1 200 OK\r\n")
        request = client_socket.recv(1024)
        logging.info(f"HTTP Received: {request.decode('utf-8').strip()}")
    except Exception as e:
        logging.error(f"Error handling HTTP client: {e}")
    finally:
        client_socket.close()

# Adding a new server function
def honeypot_http_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 80))  # HTTP default port 80
    server.listen(5)
    logging.info("HTTP Honeypot started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"HTTP Connection from {addr}")
        client_handler = threading.Thread(target=handle_http_client, args=(client_socket,))
        client_handler.start()
```

### **Log Rotation**

To manage large log files, you can set up log rotation so that old logs are archived and new ones are created automatically. You can use Python's `logging.handlers.RotatingFileHandler`:
```python
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler("honeypot.log", maxBytes=1000000, backupCount=5)
logging.getLogger().addHandler(log_handler)
```

This will rotate the log file when it reaches 1MB, keeping up to 5 backup logs.

---

## **Security Considerations**

1. **Do NOT use this honeypot in a production environment**. Honeypots are designed to attract malicious traffic, and running them publicly may result in real attacks.
2. **Avoid running the honeypot on your main network**. Ideally, deploy it in an isolated network or use a cloud provider to contain any potential threats.
3. **Be aware of legal implications**. Logging attacker data or interacting with malicious actors might have legal consequences depending on your country’s laws. Always check local regulations before deploying a honeypot.

---

## **Deploying in the Cloud (Optional)**

You can deploy this honeypot on a cloud provider like AWS, Google Cloud, or DigitalOcean. Here's a high-level overview:

1. **Set up a VM**: Create a new VM instance and open the required ports (21, 22, etc.) in your cloud provider’s firewall/security group settings.
2. **SSH into the VM**: Once your instance is up and running, SSH into it and install Python, Git, and any required packages.
3. **Clone the repository**: Download your project from GitHub and run the honeypot just as you would on a local machine.

---

## **Conclusion**

This honeypot project is designed to simulate a vulnerable system, attract attackers, and log their activities. By deploying it, you can learn more about how attackers behave in real-world scenarios, providing valuable insights for network defense and cybersecurity research.

---

## **Future Enhancements**

Here are a few ideas to expand and improve this project:
- Add support for more services (SMTP, MySQL, HTTP).
- Implement IP blacklisting after a certain number of connection attempts.
- Visualize logs using tools like Grafana or Kibana.
- Create alerting functionality that notifies you via email or SMS when an attack occurs.

---

## **Contributing**

Feel free to contribute by submitting issues or pull requests. If you find a bug or have an idea for a new feature, please open an issue on GitHub.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## **Disclaimer**

This project is for **educational purposes only**. Do not use this in a production environment, and ensure that you understand the risks of deploying a honeypot, especially on public-facing servers.

---

With this documentation, users will have a clear understanding of how to install, run, and contribute to your honeypot project.
