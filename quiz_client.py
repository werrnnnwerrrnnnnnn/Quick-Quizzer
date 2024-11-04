import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    try:
        while True:
            # Receive message from the server
            response = client_socket.recv(1024).decode()
            parts = response.split(':')
            
            # Process different types of messages
            if parts[0] == "QUESTION":
                print(f"Question {parts[1]}: {parts[2]}")
                answer = input("Your answer: ")
                answer_message = f"ANSWER:{parts[1]}:{answer}"
                client_socket.send(answer_message.encode())
            
            elif parts[0] == "SCORE":
                print(f"Your current score: {parts[1]}")
            
            elif parts[0] == "STATUS":
                print(f"Status: {parts[1]} - {parts[2]}")
                # Break if quiz is complete
                if parts[2] == "Quiz Complete":
                    break
    
    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()