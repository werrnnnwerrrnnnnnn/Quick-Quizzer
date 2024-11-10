# quiz_server.py
import socket
import time
import threading

# Define questions for different levels
questions = {
    "easy": {
        1: {"text": "What is 1 + 1?", "answer": "2"},
        2: {"text": "What is 2 + 3?", "answer": "5"},
        3: {"text": "What is 5 - 2?", "answer": "3"}
    },
    "medium": {
        1: {"text": "What is 12 * 3?", "answer": "36"},
        2: {"text": "What is 15 / 3?", "answer": "5"},
        3: {"text": "What is 9 + 6?", "answer": "15"}
    },
    "hard": {
        1: {"text": "What is 25 * 4?", "answer": "100"},
        2: {"text": "What is 50 / 2?", "answer": "25"},
        3: {"text": "What is 10 + 15 * 2?", "answer": "40"}
    }
}

clients = {}  # Dictionary to store client data for multiplayer

def handle_client(client_socket, client_id):
    score = 0  # Initial score
    response_times = []  # Store response times for latency calculations
    level = None

    client_socket.send("WELCOME: Choose a level to begin (easy, medium, hard) or type HELP for options.\n".encode())

    while not level:
        response = client_socket.recv(1024).decode().strip().lower()
        if response == "help":
            client_socket.send("HELP: Available commands - easy, medium, hard, quit\n".encode())
        elif response in questions:
            level = response
            client_socket.send(f"STATUS:200:Level '{level.capitalize()}' Selected 🎉\n".encode())
            client_socket.send("DASHLINE:============================\n".encode())
        elif response == "quit":
            client_socket.send("STATUS:200:Disconnected\n".encode())
            client_socket.close()
            return
        else:
            client_socket.send("STATUS:400:Invalid Level. Type 'HELP' for options.\n".encode())

    for q_id, q_data in questions[level].items():
        question_message = f"QUESTION:{q_id}:{q_data['text']}\n"
        client_socket.send(question_message.encode())
        
        # Send a timeout message if time limit per question
        timeout_seconds = 10
        client_socket.send(f"TIMEOUT:{timeout_seconds} seconds\n".encode())
        start_time = time.time()
        
        response = client_socket.recv(1024).decode().strip()
        end_time = time.time()
        latency = end_time - start_time  # Calculate latency
        response_times.append(latency)
        
        # Send latency info back to client
        client_socket.send(f"LATENCY:{latency:.2f} seconds\n".encode())
        print(f"[{client_id}] Latency for question {q_id}: {latency:.2f} seconds")

        parts = response.split(':')
        if len(parts) == 3 and parts[0] == "ANSWER" and int(parts[1]) == q_id:
            client_answer = parts[2].strip().lower()
            correct_answer = q_data["answer"].strip().lower()
            if client_answer == correct_answer:
                score += 1
                client_socket.send("STATUS:200:Correct! 🎉\n".encode())
            else:
                client_socket.send("STATUS:200:Incorrect ❌\n".encode())
        else:
            client_socket.send("STATUS:400:Bad Request\n".encode())

        # Send updated score
        time.sleep(0.1)
        client_socket.send(f"SCORE: Your current score is {score} 🏆\n".encode())
        time.sleep(0.1)

    # Send final score and average latency
    average_latency = sum(response_times) / len(response_times) if response_times else 0
    client_socket.send("DASHLINE:============================\n".encode())
    client_socket.send(f"STATUS:200:Quiz Complete! 🏁 Average Latency: {average_latency:.2f} seconds\n".encode())
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...")
    
    while True:
        client_socket, addr = server_socket.accept()
        client_id = addr[1]  # Use port number as a unique identifier for simplicity
        print(f"Connected to {addr} as {client_id}")
        
        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

if __name__ == "__main__":
    start_server()