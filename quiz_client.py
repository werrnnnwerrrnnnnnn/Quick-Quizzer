import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server.")
    print("============================")  # Add separator line after connection message

    try:
        # Initial mode selection
        print("🎉 Welcome to Quick-Quizzer! 🎉")
        print("Choose 'math' for a quiz or 'hangman' for hangman.")
        mode = input("Choose mode (math/hangman): ").strip().lower()
        client_socket.send(f"{mode}\n".encode())

        if mode == "math":
            # Math quiz mode handling
            while True:
                response = client_socket.recv(1024).decode().strip()
                if not response:
                    print("No response from server, closing connection.")
                    break

                messages = response.split('\n')
                for message in messages:
                    parts = message.split(':')
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
                        print(f"ℹ️ {message}")
                        if "Quiz Complete" in message:
                            print("\nThank you for playing! 🎉")
                            return

        elif mode == "hangman":
            # Hangman game handling
            while True:
                response = client_socket.recv(1024).decode().strip()
                if not response:
                    print("No response from server, closing connection.")
                    break

                messages = response.split('\n')
                for message in messages:
                    parts = message.split(':')

                    if parts[0] == "WELCOME":
                        print(parts[1].strip() if len(parts) > 1 else message)
                    elif parts[0] == "WORD":
                        print(f"Current Word: {parts[1].strip() if len(parts) > 1 else ''}")
                    elif parts[0] == "ATTEMPTS_LEFT":
                        print(f"Attempts Left: {parts[1].strip() if len(parts) > 1 else ''}")
                    elif parts[0] == "PROMPT":
                        guess = input("Guess a letter: ").strip().lower()
                        client_socket.send(f"{guess}\n".encode())
                    elif parts[0] == "STATUS":
                        print(parts[1].strip() if len(parts) > 1 else message)
                        if "Game Over" in message or "Congratulations" in message:
                            return

    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()