#!/usr/bin/env python3
"""
Terminal Chat Server - Pure Python Socket Programming
Run this on one computer to host the chat room
"""

import socket
import threading
import time
from datetime import datetime

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host  # 0.0.0.0 means accept connections from any IP
        self.port = port
        self.clients = {}  # {socket: {'username': str, 'address': tuple}}
        self.server_socket = None
        self.running = False
        
    def start(self):
        """Start the chat server"""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to address and port
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)  # Allow up to 10 pending connections
            
            self.running = True
            print(f"🚀 Chat Server started on {self.host}:{self.port}")
            print(f"📡 Local IP: {self.get_local_ip()}")
            print("💡 Tell others to connect using: python client.py <your-ip>")
            print("🔄 Waiting for connections...\n")
            
            # Accept connections in main thread
            self.accept_connections()
            
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.stop()
    
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            # Connect to a remote address to determine local IP
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def accept_connections(self):
        """Accept new client connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"🔗 New connection from {address[0]}:{address[1]}")
                
                # Start a thread to handle this client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except socket.error:
                if self.running:
                    print("❌ Error accepting connections")
                break
    
    def handle_client(self, client_socket, address):
        """Handle messages from a single client"""
        username = None
        
        try:
            # Get username from client
            client_socket.send("Enter your username: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            if not username:
                client_socket.send("❌ Invalid username\n".encode('utf-8'))
                return
            
            # Add client to our list
            self.clients[client_socket] = {
                'username': username,
                'address': address
            }
            
            # Welcome messages
            welcome_msg = f"✅ Welcome {username}! You're connected to the chat.\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Notify everyone about new user
            join_msg = f"👤 {username} joined the chat ({len(self.clients)} users online)"
            self.broadcast_message(join_msg, exclude_client=client_socket)
            print(f"✅ {username} joined from {address[0]} ({len(self.clients)} users)")
            
            # Send current users list
            if len(self.clients) > 1:
                users = [info['username'] for info in self.clients.values()]
                users_msg = f"👥 Users online: {', '.join(users)}\n"
                client_socket.send(users_msg.encode('utf-8'))
            
            # Handle messages from this client
            while self.running:
                message = client_socket.recv(1024).decode('utf-8').strip()
                
                if not message:
                    break
                
                if message.lower() in ['/quit', '/exit']:
                    break
                
                # Format and broadcast message
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_msg = f"[{timestamp}] {username}: {message}"
                
                print(formatted_msg)  # Log on server
                self.broadcast_message(formatted_msg, exclude_client=client_socket)
                
        except socket.error as e:
            print(f"🔌 Client {address} disconnected: {e}")
        except Exception as e:
            print(f"❌ Error handling client {address}: {e}")
        finally:
            # Clean up client
            self.remove_client(client_socket, username)
    
    def broadcast_message(self, message, exclude_client=None):
        """Send message to all connected clients except sender"""
        message_bytes = (message + "\n").encode('utf-8')
        
        # List to track clients to remove (if disconnected)
        clients_to_remove = []
        
        for client_socket in list(self.clients.keys()):
            if client_socket != exclude_client:
                try:
                    client_socket.send(message_bytes)
                except socket.error:
                    # Client disconnected, mark for removal
                    clients_to_remove.append(client_socket)
        
        # Remove disconnected clients
        for client_socket in clients_to_remove:
            username = self.clients.get(client_socket, {}).get('username', 'Unknown')
            self.remove_client(client_socket, username)
    
    def remove_client(self, client_socket, username):
        """Remove a client from the server"""
        if client_socket in self.clients:
            del self.clients[client_socket]
            
            try:
                client_socket.close()
            except:
                pass
            
            if username:
                leave_msg = f"👋 {username} left the chat ({len(self.clients)} users online)"
                print(f"❌ {username} disconnected ({len(self.clients)} users remaining)")
                self.broadcast_message(leave_msg)
    
    def stop(self):
        """Stop the server"""
        self.running = False
        
        # Close all client connections
        for client_socket in list(self.clients.keys()):
            try:
                client_socket.send("🛑 Server shutting down...\n".encode('utf-8'))
                client_socket.close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("\n🛑 Chat server stopped")

    def start_admin_input(self):
        """Allow server admin to send messages"""
        print("💬 Server admin can now send messages!")
        print("💡 Commands: /msg <message>, /users, /kick <username>, /quit")
        
        while self.running:
            try:
                admin_input = input("Server> ").strip()
                
                if not admin_input:
                    continue
                    
                if admin_input == "/quit":
                    print("🛑 Shutting down server...")
                    self.stop()
                    break
                elif admin_input == "/users":
                    users = [info['username'] for info in self.clients.values()]
                    print(f"👥 Connected users ({len(users)}): {', '.join(users)}")
                elif admin_input.startswith("/kick "):
                    username = admin_input[6:].strip()
                    self.kick_user(username)
                elif admin_input.startswith("/msg "):
                    message = admin_input[5:].strip()
                    if message:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        server_msg = f"[{timestamp}] 🔧 SERVER: {message}"
                        print(server_msg)
                        self.broadcast_message(server_msg)
                elif admin_input.startswith("/"):
                    print("❌ Unknown command. Available: /msg, /users, /kick, /quit")
                else:
                    # Regular message (same as /msg)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    server_msg = f"[{timestamp}] 🔧 SERVER: {admin_input}"
                    print(server_msg)
                    self.broadcast_message(server_msg)
                    
            except KeyboardInterrupt:
                print("\n🛑 Server shutting down...")
                self.stop()
                break
            except Exception as e:
                print(f"❌ Admin input error: {e}")
    
    def kick_user(self, username):
        """Kick a user from the chat"""
        client_to_kick = None
        
        for client_socket, info in self.clients.items():
            if info['username'].lower() == username.lower():
                client_to_kick = client_socket
                break
        
        if client_to_kick:
            try:
                kick_msg = f"🚫 You have been kicked from the chat by server admin"
                client_to_kick.send(kick_msg.encode('utf-8'))
                self.remove_client(client_to_kick, username)
                print(f"🚫 Kicked user: {username}")
            except:
                pass
        else:
            print(f"❌ User '{username}' not found")

if __name__ == "__main__":
    # Create and start server
    server = ChatServer()
    
    try:
        # Start server in a separate thread so we can handle admin input
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()
        
        # Give server time to start
        time.sleep(1)
        
        # Handle admin commands in main thread
        if server.running:
            server.start_server_chat()
            
    except KeyboardInterrupt:
        print("\n⏹️  Server interrupted by user")
        server.stop()