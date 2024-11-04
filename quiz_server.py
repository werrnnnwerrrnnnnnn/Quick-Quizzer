import socket
import time

# Define questions and answers
questions = {
    1: {"text": "What is the capital of France?", "answer": "Paris"},
    2: {"text": "What is 2 + 2?", "answer": "4"},
    3: {"text": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"}
}

def handle_client(client_socket):
    score = 0  # Initial score
    for q_id, q_data in questions.items():
        # Send question to client
        question_message = f"QUESTION:{q_id}:{q_data['text']}"
        client_socket.send(question_message.encode())
        
        # Receive answer from client
        response = client_socket.recv(1024).decode()
        parts = response.split(':')
        
        # Check if answer is valid and correct
        if parts[0] == "ANSWER" and int(parts[1]) == q_id:
            client_answer = parts[2].strip().lower()
            correct_answer = q_data["answer"].strip().lower()
            
            if client_answer == correct_answer:
                score += 1
                client_socket.send("STATUS:200:Correct".encode())
            else:
                client_socket.send("STATUS:200:Incorrect".encode())
        else:
            client_socket.send("STATUS:400:Bad Request".encode())
        
        # Separate each message with a small delay
        time.sleep(0.1)  # Small delay to ensure separate transmission
        client_socket.send(f"SCORE:{score}".encode())
        time.sleep(0.1)  # Delay before the next question or closing message

    # Inform the client that the quiz is complete
    client_socket.send("STATUS:200:Quiz Complete".encode())
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()