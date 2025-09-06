# 💬 Python Terminal Chat

A simple **terminal-based chat application** built using **pure Python 3.x** and **socket programming**.  
It uses a **client-server architecture** where multiple users can chat in real time over TCP/IP without external libraries.  

---

## 📛 Badges
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)

---

## 📚 Core Technologies Used

### Programming Language
- **Python 3.x** (main programming language)  
- **No external libraries** → Pure Python solution  

### Built-in Python Modules
- `socket` → Network communication (TCP sockets)  
- `threading` → Handle multiple users simultaneously  
- `time` → Delays and timing functions  
- `sys` → Command-line arguments & system functions  
- `datetime` → Message timestamps  

---

## 🌐 Network & Communication Stack

### Protocol Layers
- Application Layer → Chat Messages (Custom text protocol)  
- Transport Layer → TCP (Transmission Control Protocol)  
- Network Layer → IP (Internet Protocol)  
- Data Link Layer → Ethernet/Wi-Fi  
- Physical Layer → Network cables/Radio waves  

### Socket Programming Concepts
- TCP Sockets (`socket.AF_INET`, `socket.SOCK_STREAM`)  
- Client-Server Architecture  
- Bind / Listen / Accept pattern  
- Send / Receive operations  
- Connection management  

---


## 🎮 Server Commands

### 🔹 Chat Mode (Default)
- `SERVER> Hello everyone!` → Regular chat message  
- `SERVER> /admin` → Switch to admin mode  
- `SERVER> /users` → List connected users  
- `SERVER> /help` → Show all commands  
- `SERVER> /quit` → Shutdown server  

### 🔹 Admin Mode
- `Admin> /kick username` → Remove a user  
- `Admin> /announce message` → Send an announcement  
- `Admin> /chat` → Switch back to chat mode  
- `Admin> /users` → List users  
- `Admin> /quit` → Shutdown server  

---

## 👤 Client Commands
- `Alice> Hello everyone!` → Regular message  
- `Alice> /quit` → Leave chat  
- `Alice> /exit` → Leave chat  

