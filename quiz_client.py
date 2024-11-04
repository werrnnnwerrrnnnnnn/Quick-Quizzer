import socket

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    try:
        # Prompt user to type "start" to begin the quiz
        while True:
            start_command = input("Type 'start' to begin the quiz: ").strip().lower()
            if start_command == "start":
                client_socket.send("START\n".encode())
                break
            else:
                print("Please type 'start' to begin.")
        
        while True:
            # Receive message from the server and split by newline
            response = client_socket.recv(1024).decode().strip()
            messages = response.split('\n')  # Split messages by newline
            
            for message in messages:
                parts = message.split(':')
                
                # Process different types of messages
                if parts[0] == "QUESTION":
                    print(f"Question {parts[1]}: {parts[2]}")
                    answer = input("Your answer: ")
                    answer_message = f"ANSWER:{parts[1]}:{answer}\n"
                    client_socket.send(answer_message.encode())
                
                elif parts[0] == "DASHLINE":
                    print(parts[1])  # Print the dashed line
                
                elif parts[0] == "SCORE":
                    print(f"Your current score: {parts[1]}")
                
                elif parts[0] == "STATUS":
                    print(f"Status: {parts[1]} - {parts[2]}")
                    # Break if quiz is complete
                    if parts[2] == "Quiz Complete":
                        return  # Exit the loop
    
    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()