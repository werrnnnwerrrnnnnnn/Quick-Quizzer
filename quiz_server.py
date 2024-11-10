import socket
import time
import select
import threading
from datetime import datetime

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

TIMEOUT_DURATION = 10  # seconds

def log_message(client_id, message):
    """Helper function to print log messages with timestamp and client ID."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Client {client_id}] {message}")

def handle_client(client_socket, client_id):
    score = 0
    response_times = []
    level = None

    log_message(client_id, "==============================")
    log_message(client_id, "Connection established")

    client_socket.send("WELCOME: Choose a level to begin (easy, medium, hard) or type HELP for options.\n".encode())

    while not level:
        response = client_socket.recv(1024).decode().strip().lower()
        if response == "help":
            client_socket.send("HELP: Available commands - easy, medium, hard, quit\n".encode())
            log_message(client_id, "Requested help")
        elif response in questions:
            level = response
            client_socket.send(f"STATUS:200:Level '{level.capitalize()}' Selected 🎉\n".encode())
            client_socket.send("DASHLINE:============================\n".encode())
            log_message(client_id, f"Level selected: {level.capitalize()}")
        elif response == "quit":
            client_socket.send("STATUS:200:Disconnected\n".encode())
            client_socket.close()
            log_message(client_id, "Disconnected")
            return
        else:
            client_socket.send("STATUS:400:Invalid Level. Type 'HELP' for options.\n".encode())
            log_message(client_id, f"Invalid level input: {response}")

    # Start the timer for the total quiz duration
    quiz_start_time = time.time()

    for q_id, q_data in questions[level].items():
        log_message(client_id, f"\n----- Question {q_id} -----")
        log_message(client_id, f"Question: {q_data['text']}")
        
        question_message = f"QUESTION:{q_id}:{q_data['text']}\n"
        client_socket.send(question_message.encode())
        time.sleep(0.1)

        client_socket.send(f"TIMEOUT:{TIMEOUT_DURATION} seconds\n".encode())
        log_message(client_id, f"Timeout set for {TIMEOUT_DURATION} seconds")

        start_time = time.time()
        ready = select.select([client_socket], [], [], TIMEOUT_DURATION)

        if ready[0]:  # Client responded in time
            response = client_socket.recv(1024).decode().strip()
            end_time = time.time()
            latency = end_time - start_time
            response_times.append(latency)

            client_socket.send(f"LATENCY:{latency:.2f} seconds\n".encode())
            log_message(client_id, f"Response received in {latency:.2f} seconds")

            parts = response.split(':')
            if len(parts) == 3 and parts[0] == "ANSWER" and int(parts[1]) == q_id:
                client_answer = parts[2].strip().lower()
                correct_answer = q_data["answer"].strip().lower()
                if client_answer == correct_answer:
                    score += 1
                    client_socket.send("STATUS:200:Correct! 🎉\n".encode())
                    log_message(client_id, f"Correct answer: {client_answer}")
                else:
                    client_socket.send("STATUS:200:Incorrect ❌\n".encode())
                    log_message(client_id, f"Incorrect answer: {client_answer} (Expected: {correct_answer})")
            else:
                client_socket.send("STATUS:400:Bad Request\n".encode())
                log_message(client_id, f"Bad request or malformed answer: {response}")
        else:  # Timeout
            latency = TIMEOUT_DURATION
            response_times.append(latency)
            client_socket.send("STATUS:408:Timeout ❌\n".encode())
            client_socket.send(f"LATENCY:{latency:.2f} seconds (Timed out)\n".encode())
            log_message(client_id, f"No response - Timeout set latency to {latency} seconds")

        client_socket.send(f"SCORE: Your current score is {score} 🏆\n".encode())
        log_message(client_id, f"Score after question {q_id}: {score}")
        log_message(client_id, "------------------------------\n")
        time.sleep(0.1)

    # Calculate total quiz time and average latency
    quiz_end_time = time.time()
    total_time = quiz_end_time - quiz_start_time
    average_latency = sum(response_times) / len(response_times) if response_times else 0

    client_socket.send("DASHLINE:============================\n".encode())
    client_socket.send(f"STATUS:200:Quiz Complete! 🏁 Final Score: {score}, Average Latency: {average_latency:.2f} seconds, Total Time: {total_time:.2f} seconds\n".encode())
    client_socket.close()
    
    # Log final stats
    log_message(client_id, f"Quiz complete - Final score: {score}, Average Latency: {average_latency:.2f} seconds, Total Time: {total_time:.2f} seconds")
    log_message(client_id, "==============================\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...\n")
    
    while True:
        client_socket, addr = server_socket.accept()
        client_id = addr[1]  # Use port number as unique identifier
        log_message(client_id, f"Connected to {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

if __name__ == "__main__":
    start_server()