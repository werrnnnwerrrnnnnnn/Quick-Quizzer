# quiz_client.py
import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server.")
    print("============================")  # Add separator line after connection message
    
    try:
        while True:
            # Receive message from the server and split by newline to process multiple messages
            response = client_socket.recv(1024).decode().strip()
            if not response:
                print("No response from server, closing connection.")
                break
            
            messages = response.split('\n')
            for message in messages:
                parts = message.split(':')
                
                # Process different types of messages from the server
                if "WELCOME" in message:
                    # Print the welcome message
                    print("🎉 WELCOME to the Ultimate Quiz Challenge! 🎉")
                    print("🌟 Choose your adventure level 🌟")
                    print("Type one of the following:")
                    print("  - 🟢 easy : A warm-up for beginners")
                    print("  - 🟡 medium : For those who love a good challenge")
                    print("  - 🔴 hard : The ultimate test of skill!")
                    print("\n💡 Need help? Just type 'HELP' for instructions.")
                    print("⏳ Ready to start? Make your choice and let's begin!\n")
                    
                    level = input("Choose a level to begin the quiz (easy, medium, hard): ").strip().lower()
                    client_socket.send(f"{level}\n".encode())
                
                elif parts[0] == "QUESTION":
                    print(f"\n📝 {message}")
                    answer = input("Your answer: ")
                    answer_message = f"ANSWER:{parts[1]}:{answer}\n"
                    client_socket.send(answer_message.encode())
                
                elif parts[0] == "DASHLINE":
                    print(parts[1])  # Print the dashed line
                
                elif parts[0] == "TIMEOUT":
                    print(f"⏰ Time limit: {parts[1]}")
                
                elif parts[0] == "LATENCY":
                    print(f"⏱️ {message}")
                
                elif parts[0] == "SCORE":
                    print(f"🏆 {message}")
                
                elif parts[0] == "STATUS":
                    print(f"ℹ️ {message}")
                    if "Quiz Complete" in message:
                        print("\nThank you for playing! 🎉")
                        return
    
    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()