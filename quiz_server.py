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
    
    # Receive initial "START" message
    response = client_socket.recv(1024).decode().strip()
    print(f"Received from client: {response}")  # Debug: print the received message
    
    if response != "START":
        client_socket.send("STATUS:400:Bad Request\n".encode())
        client_socket.close()
        return
    
    # If "START" received, send a dashed line to separate start state from questions
    client_socket.send("DASHLINE:--------------------\n".encode())
    time.sleep(0.1)
    
    # Proceed with the quiz
    for q_id in questions:
        q_data = questions[q_id]
        
        # Send question to client
        question_message = f"QUESTION:{q_id}:{q_data['text']}\n"
        client_socket.send(question_message.encode())
        
        # Send dashed line to separate questions
        time.sleep(0.1)
        client_socket.send("DASHLINE:--------------------\n".encode())
        
        # Receive answer from client
        response = client_socket.recv(1024).decode().strip()
        print(f"Received from client: {response}")  # Debug: print the received message
        
        # Split the response and validate
        parts = response.split(':')
        print(f"Parsed parts: {parts}")  # Additional debug to see the parsed parts
        
        # Validate the format and answer
        if len(parts) == 3 and parts[0] == "ANSWER":
            client_answer = parts[2].strip().lower()
            correct_answer = q_data["answer"].strip().lower()
            print(f"Client answer: {client_answer}, Correct answer: {correct_answer}")  # Debug

            if client_answer == correct_answer:
                score += 1
                client_socket.send("STATUS:200:Correct\n".encode())
            else:
                client_socket.send("STATUS:200:Incorrect\n".encode())
        else:
            print("Bad request detected.")  # Debug to see if condition fails
            client_socket.send("STATUS:400:Bad Request\n".encode())
        
        # Send score after each question
        time.sleep(0.1)
        client_socket.send(f"SCORE:{score}\n".encode())
        time.sleep(0.1)

    # Inform the client that the quiz is complete
    client_socket.send("STATUS:200:Quiz Complete\n".encode())
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