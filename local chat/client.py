#!/usr/bin/env python3
"""
Terminal Chat Client - Pure Python Socket Programming
Connect to a chat server running on local network
"""

import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self):
        self.client_socket = None
        self.connected = False
        self.username = ""
        
    def connect(self, server_ip, server_port=5555):
        """Connect to the chat server"""
        try:
            # Create client socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            print(f"🔗 Connecting to {server_ip}:{server_port}...")
            self.client_socket.connect((server_ip, server_port))
            
            self.connected = True
            print(f"✅ Connected to chat server!")
            print("💡 Type '/quit' or '/exit' to leave the chat\n")
            
            # Start listening for messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Handle user input
            self.handle_user_input()
            
        except socket.error as e:
            print(f"❌ Connection failed: {e}")
            print("💡 Make sure the server is running and IP address is correct")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.disconnect()
    
    def receive_messages(self):
        """Listen for messages from the server"""
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Print received message
                print(f"\r{message}", end="")
                
                # Show input prompt again if not a username prompt
                if not message.startswith("Enter your username"):
                    if self.username:
                        print(f"{self.username}> ", end="", flush=True)
                
            except socket.error:
                if self.connected:
                    print("\n❌ Lost connection to server")
                break
            except Exception as e:
                print(f"\n❌ Error receiving message: {e}")
                break
    
    def handle_user_input(self):
        """Handle user input and send to server"""
        while self.connected:
            try:
                # Get user input
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                # Check for quit commands
                if user_input.lower() in ['/quit', '/exit']:
                    print("👋 Goodbye!")
                    break
                
                # Send message to server
                self.client_socket.send(user_input.encode('utf-8'))
                
                # Set username after first input (assuming it's username)
                if not self.username and not user_input.startswith('/'):
                    self.username = user_input
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except socket.error as e:
                print(f"\n❌ Error sending message: {e}")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                break
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        
        print("🔌 Disconnected from server")

def print_usage():
    """Print usage instructions"""
    print("📱 Terminal Chat Client")
    print("Usage:")
    print("  python client.py <server-ip>")
    print("  python client.py <server-ip> <port>")
    print("\nExamples:")
    print("  python client.py 192.168.1.100")
    print("  python client.py localhost")
    print("  python client.py 10.0.0.5 5555")

def get_local_network_ips():
    """Get common local network IP ranges for reference"""
    print("\n💡 Common local network IP ranges:")
    print("   • 192.168.x.x (most home networks)")
    print("   • 10.x.x.x (corporate networks)")
    print("   • 172.16.x.x - 172.31.x.x (private networks)")
    print("   • localhost or 127.0.0.1 (same computer)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        get_local_network_ips()
        
        # Interactive mode - ask for server IP
        print("\n" + "="*50)
        server_ip = input("Enter server IP address: ").strip()
        if not server_ip:
            print("❌ No IP address provided")
            sys.exit(1)
    else:
        server_ip = sys.argv[1]
    
    # Get port (optional)
    server_port = 5555
    if len(sys.argv) >= 3:
        try:
            server_port = int(sys.argv[2])
        except ValueError:
            print("❌ Invalid port number")
            sys.exit(1)
    
    # Create and connect client
    client = ChatClient()
    client.connect(server_ip, server_port)