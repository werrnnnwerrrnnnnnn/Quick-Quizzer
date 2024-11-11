import socket
import time
import select
import threading
from datetime import datetime
import random

# Define questions for math quiz
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

# Words for Hangman game
hangman_words = ["python", "socket", "network", "quiz", "programming"]

TIMEOUT_DURATION = 10  # seconds

def log_message(client_id, message):
    """Helper function to print log messages with timestamp and client ID."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Client {client_id}] {message}")

def handle_client(client_socket, client_id):
    # Initial mode selection
    mode = client_socket.recv(1024).decode().strip().lower()
    log_message(client_id, f"Mode selected: {mode}")

    if mode == "math":
        handle_math_quiz(client_socket, client_id)

    elif mode == "hangman":
        handle_hangman(client_socket, client_id)

    elif mode == "quit":
        client_socket.send("STATUS:411 🏁 Goodbye! Thanks for playing!\n".encode())
        client_socket.close()

    else:
        client_socket.send("STATUS:400 ⚠️ Oops! Wrong Format\n".encode())
        log_message(client_id, "Invalid mode selected. Disconnecting client.")
        client_socket.close()

def handle_math_quiz(client_socket, client_id):
    score = 0
    response_times = []
    level = None

    # Send welcome message for math quiz
    client_socket.send("WELCOME:100 🎉 You’ve Got This!\n".encode())
    client_socket.send("🌟 Choose your adventure level 🌟\n".encode())
    client_socket.send("Type one of the following:\n".encode())
    client_socket.send("  - 🟢 easy : A warm-up for beginners\n".encode())
    client_socket.send("  - 🟡 medium : For those who love a good challenge\n".encode())
    client_socket.send("  - 🔴 hard : The ultimate test of skill!\n".encode())
    client_socket.send("\n💡 Need help? Just type 'HELP' for instructions.\n".encode())
    client_socket.send("⏳ Ready to start? Make your choice and let's begin!\n".encode())

    # Wait for level selection
    while not level:
        response = client_socket.recv(1024).decode().strip().lower()
        if response in questions:
            level = response
            client_socket.send(f"STATUS:100 🎉 Level '{level.capitalize()}' Selected!\n".encode())
            client_socket.send("DASHLINE:============================\n".encode())
            log_message(client_id, f"Level selected: {level.capitalize()}")
        elif response == "quit":
            client_socket.send("STATUS:411 🏁 Goodbye! Thanks for playing!\n".encode())
            client_socket.close()
            log_message(client_id, "Client chose to quit during level selection. Disconnecting client.")
            return
        else:
            client_socket.send("STATUS:400 ⚠️ Oops! Wrong Format\n".encode())
            log_message(client_id, f"Invalid level input: {response}")
            client_socket.close()
            return

    # Start quiz
    for q_id, q_data in questions[level].items():
        log_message(client_id, f"Question {q_id}: {q_data['text']}")
        
        question_message = f"QUESTION:{q_id}:{q_data['text']}\n"
        client_socket.send("STATUS:300 💡 Question Incoming\n".encode())
        client_socket.send(question_message.encode())
        time.sleep(0.1)

        # Measure response time
        start_time = time.time()
        ready = select.select([client_socket], [], [], TIMEOUT_DURATION)
        end_time = time.time()
        latency = end_time - start_time
        response_times.append(latency)

        # Check if the client took too long
        if latency > TIMEOUT_DURATION:
            client_socket.send("STATUS:408 ⏰ Time’s Up Warning!\n".encode())
            client_socket.send(f"LATENCY:{latency:.2f} seconds (Exceeded Time Limit)\n".encode())
            log_message(client_id, f"Response exceeded timeout with latency: {latency:.2f} seconds")
        else:
            client_socket.send(f"LATENCY:{latency:.2f} seconds\n".encode())
            log_message(client_id, f"Response received in {latency:.2f} seconds")

        # Wait for and process the answer
        if ready[0]:  # Client responded
            response = client_socket.recv(1024).decode().strip()
            parts = response.split(':')
            if len(parts) == 3 and parts[0] == "ANSWER" and int(parts[1]) == q_id:
                client_answer = parts[2].strip().lower()
                correct_answer = q_data["answer"].strip().lower()
                
                # Check if the answer is numeric
                if not client_answer.isdigit():
                    client_socket.send("STATUS:401 🚫 No Cheating! Only Numbers Allowed!\n".encode())
                    log_message(client_id, f"Non-numeric answer received: {client_answer}")
                elif client_answer == correct_answer:
                    score += 1
                    client_socket.send("STATUS:200 👏 Nailed It!\n".encode())
                    client_socket.send("STATUS:101 📊 Score Updated\n".encode())
                    log_message(client_id, f"Correct answer: {client_answer}")
                else:
                    client_socket.send("STATUS:404 ❌ Try Again!\n".encode())
                    log_message(client_id, f"Incorrect answer: {client_answer} (Expected: {correct_answer})")
            else:
                client_socket.send("STATUS:400 ⚠️ Oops! Wrong Format\n".encode())
                log_message(client_id, f"Bad request or malformed answer: {response}")
        else:
            log_message(client_id, "No response from client")

        client_socket.send(f"SCORE: Your current score is {score} 🏆\n".encode())
        log_message(client_id, f"Score after question {q_id}: {score}")
        log_message(client_id, "------------------------------\n")
        time.sleep(0.1)

    # Send quiz completion stats
    total_time = sum(response_times)
    average_latency = sum(response_times) / len(response_times) if response_times else 0
    client_socket.send("DASHLINE:============================\n".encode())
    client_socket.send(f"STATUS:410 🎉 Quiz Complete! Thanks for Playing! 🏆 Final Score: {score}, Average Latency: {average_latency:.2f} seconds, Total Time: {total_time:.2f} seconds\n".encode())
    client_socket.close()

def handle_hangman(client_socket, client_id):
    word = random.choice(hangman_words)
    guessed_letters = set()
    attempts_left = 6
    display_word = "_" * len(word)

    client_socket.send("WELCOME:100 👀 Ready, Set, Guess!\n".encode())
    log_message(client_id, f"Starting Hangman with word: {word}")

    while attempts_left > 0 and "_" in display_word:
        client_socket.send(f"WORD: {' '.join(display_word)}\n".encode())
        client_socket.send(f"ATTEMPTS_LEFT: {attempts_left}\n".encode())
        client_socket.send("PROMPT: Guess a letter:\n".encode())

        response = client_socket.recv(1024).decode().strip().lower()
        if not response or len(response) != 1 or not response.isalpha():
            if response.isdigit():
                client_socket.send("STATUS:400 👎 No Digits Allowed\n".encode())
            elif not response.isalnum():
                client_socket.send("STATUS:401 🚫 Special Characters Not Allowed\n".encode())
            else:
                client_socket.send("STATUS:400 ⚠️ Oops! Wrong Format\n".encode())
            continue

        if response in guessed_letters:
            client_socket.send("STATUS:202 😬 Already Tried That!\n".encode())
            continue

        guessed_letters.add(response)

        if response in word:
            display_word = "".join([letter if letter in guessed_letters else "_" for letter in word])
            if "_" not in display_word:
                client_socket.send(f"STATUS:410 🎉 You Win! The Word Was '{word}'\n".encode())
                log_message(client_id, "Player successfully guessed the word.")
                break
            else:
                client_socket.send("STATUS:200 👍 Nice Choice!\n".encode())
        else:
            client_socket.send("STATUS:404 ❌ Wrong Guess\n".encode())
            attempts_left -= 1

        log_message(client_id, f"Guessed '{response}', Attempts left: {attempts_left}, Word: {display_word}")

    if "_" in display_word:
        client_socket.send(f"STATUS:411 😞 Game Over - Word Was '{word}'\n".encode())
        log_message(client_id, "Game over. Player failed to guess the word.")

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows immediate reuse of the address
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...\n")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_id = addr[1]  # Use port number as unique identifier
            log_message(client_id, f"Connected to {addr}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()