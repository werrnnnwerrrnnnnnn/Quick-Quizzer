# QuickQuizzer 🎉
Welcome to **QuickQuizzer** – an interactive terminal quiz game with two modes: **Math Quiz** and **Hangman**!

## 📍 How to Play 
1. **Choose Game Mode**: Select either `math` or `hangman` to start.
2. **Follow Prompts**: Answer questions or guess letters based on the mode.
3. **Scoring**: Points for correct answers. See real-time feedback on your guesses.
4. **Game Over**: View your final score and performance summary.

### 📍 Requirements 
- Python 3.x installed on your machine
- A terminal to run the server and clien

### 📍 Start the Game
- Step 1: Start the Server
    - Navigate to the directory where `quiz_server.py` is located, and run: ```python3 quiz_server.py```
    - You should see: ``` Server is listening on port 12345... ```

- Step 2: Start the Client
    - Navigate to the same directory, and run: ```python3 quiz_client.py```
    - You should see: ```Type 'start' to begin the quiz:```
    - Type `start` and hit Enter to begin the quiz!

### 📍 Important Notes
- Run server first, then connect with the client.
- Ensure server and client are on the same network.
- Use the exact command format for answers, or you may get a "Bad Request" error.

Enjoy the quiz, and good luck! 🧠✨

<!-- ------------------------------------------------------- -->
### 📍 Math Quiz Mode

| Status Code        | Phrase                                          | Description                                                  |
|--------------------|-------------------------------------------------|--------------------------------------------------------------|
| 200 OK             | Alphabet Detected                               | When an alphabet is typed as part of an answer               |
| 200 OK             | Correct Answer                                  | When the answer is correct                                   |
| 200 OK             | Answer Received in Time                         | When the answer is received within the timeout period        |
| 200 OK             | Level Chosen - Easy                             | When the level “easy” is selected                            |
| 200 OK             | Level Chosen - Medium                           | When the level “medium” is selected                          |
| 200 OK             | Level Chosen - Hard                             | When the level “hard” is selected                            |
| 400 Bad Request    | Invalid Character - Number Expected             | When an answer is expected to be a number                    |
| 400 Bad Request    | Invalid Character - Special Character Detected  | When a special character is detected                         |
| 400 Bad Request    | Invalid Level                                   | When an invalid level is selected                            |
| 404 Not Found      | Wrong Answer                                    | When the answer is incorrect                                 |
| 408 Request Timeout| Time Exceeded                                   | When the answer times out                                    |

### 📍 Hangman Mode

| Status Code        | Phrase                                          | Description                                                  |
|--------------------|-------------------------------------------------|--------------------------------------------------------------|
| 200 OK             | Alphabet Detected                               | When an alphabet letter is typed                             |
| 200 OK             | Correct Guess                                   | For a correct guess                                          |
| 200 OK             | Already Guessed                                 | When the user tries to guess a previously guessed letter     |
| 400 Bad Request    | Invalid Character - Number Detected             | When a number is typed                                       |
| 400 Bad Request    | Invalid Character - Special Character Detected  | When a special character is typed                            |
| 404 Not Found      | Wrong Guess                                     | For an incorrect guess                                       |