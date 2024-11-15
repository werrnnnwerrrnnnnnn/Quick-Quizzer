import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server.")
    print("============================")  # Add separator line after connection message

    try:
        # Initial mode selection
        print("🎉 Welcome to Quick-Quizzer! 🎉")
        print("Choose 'math' or 'hangman' mode to begin! 🕹️  [or type 'quit' to exit the game 🥺].")
        mode = input("Choose mode (math/hangman): ").strip().lower()
        client_socket.send(f"{mode}\n".encode())

        if mode == "math":
            # Math quiz mode handling (same as original logic)
            question_correctness = {}  # To store correctness per question
            while True:
                response = client_socket.recv(1024).decode().strip()
                if not response:
                    print("No response from server, closing connection.")
                    break

                messages = response.split('\n')
                for message in messages:
                    parts = message.split(':')
                    # Process server messages as in your math quiz logic
                    if "WELCOME" in message:
                        print("🎉 Welcome to Quick-Quizzer Math Mode! 🎉")
                        level = input("Choose a level to begin the quiz (easy, medium, hard): ").strip().lower()
                        client_socket.send(f"{level}\n".encode())
                    elif parts[0] == "QUESTION":
                        print(f"\n📝 {message}")
                        answer = input("Your answer: ")
                        answer_message = f"ANSWER:{parts[1]}:{answer}\n"
                        client_socket.send(answer_message.encode())
                    elif parts[0] == "DASHLINE":
                        print(parts[1])
                    elif parts[0] == "TIMEOUT":
                        print(f"⏰ Time limit: {parts[1]}")
                    elif parts[0] == "LATENCY":
                        print(f"⏱️ {message}")
                    elif parts[0] == "SCORE":
                        print(f"🏆 {message}")
                    elif parts[0] == "STATUS":
                        print(f"📣 {message}")
                        if "Quiz Complete" in message:
                            print("\nThank you for playing! 🎉")
                    elif parts[0] == "QUESTION_TIME":
                        # Display the time per question
                        question_id = parts[1]
                        time_taken = parts[2]
                        print(f"⏱️ Time for Question {question_id}: {time_taken}")
                    elif parts[0] == "QUESTION_CORRECTNESS":
                        # Store correctness info to display after time
                        question_id = parts[1]
                        correctness = parts[2]
                        question_correctness[question_id] = correctness

            # After displaying times, show correctness for each question
            print("\nSummary of Each Question! 📊")
            for question_id, correctness in question_correctness.items():
                print(f"📝 Question {question_id}: {correctness}")

        elif mode == "hangman":
            # Hangman game handling
            while True:
                response = client_socket.recv(1024).decode().strip()
                if not response:
                    print("No response from server, closing connection.")
                    break

                messages = response.split('\n')
                for message in messages:
                    parts = message.split(':', 1)
                    if parts[0] == "WELCOME":
                        print(parts[1].strip())
                    elif parts[0] == "WORD":
                        print(f"\n🔤 Current Word: {parts[1].strip()}")
                    elif parts[0] == "ATTEMPTS_LEFT":
                        print(f"❤️ Attempts Left: {parts[1].strip()}")
                    elif parts[0] == "PROMPT":
                        guess = input("\n🔡 Guess a letter: ").strip().lower()
                        client_socket.send(f"{guess}\n".encode())
                    elif parts[0] == "STATUS":
                        print(f"📣 {parts[1].strip()}")
                        if "Game Over" in parts[1] or "Congratulations" in parts[1]:
                            return
                        
        if mode == "quit":
            response = client_socket.recv(1024).decode().strip()
            print(f"📣 {response}")
            print("Exiting... Goodbye!")
            return  # Exit the function after showing the goodbye message

    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()