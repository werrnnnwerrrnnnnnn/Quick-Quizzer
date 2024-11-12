# QuickQuizzer 
- **By : Tatiya Seehatrakul st124875**
- This project is developed to fulfill the requirements of the AT70.05 Computer Networks course at the Asian Institute of Technology (AIT) for the August 2024 semester.

## 📍 Welcome to QuickQuizzer
**QuickQuizzer** – an interactive terminal quiz game with two modes: **Math Quiz** and **Hangman** 🚀  Built with a custom protocol over TCP sockets, QuickQuizzer ensures reliable, real-time communication between the client and server. With easy-to-understand status codes, it keeps gameplay smooth, updates scores quickly, and gives instant feedback to keep you engaged. Enjoy the game! 🕹️ 🙌🏻 ✨

<!-- ------------------------------------------------------- -->
## 📍 Requirements 
- Python 3.x installed on your machine
- A terminal to run the server and client
<!-- ------------------------------------------------------- -->
## 📍 Start the Game in Terminal
- Step 1: Start the Server
    - Navigate to the directory where **quiz_server.py** is located, and run: `python3 quiz_server.py`
    - You should see: `Server is listening on port 12345...`
- Step 2: Start the Client
    - Navigate to the directory where **quiz_client.py** is located, and run: `python3 quiz_client.py`
    - You should see: `Type 'start' to begin the quiz:`
    - Type `start` and hit Enter to begin the quiz!
- Important Notes
    - Run server first, then connect with the client.
    - Ensure server and client are on the same network.
    - Use the exact command format for answers, or you may get a "Bad Request" error.
<!-- ------------------------------------------------------- -->
## 📍 How to Play the Game
1. **Select a Game Mode**: Choose either `math` for a quiz or `hangman` for a word-guessing challenge.
2. **Choose Your Level** (for Math Mode): Select a level to begin your adventure: `easy`, `medium`, or `hard`.
3. **Answer Prompts**: 
   - For **Math Mode**: Respond to each question within the time limit. You'll receive feedback on speed and accuracy.
   - For **Hangman Mode**: Guess letters to reveal the word. You have limited attempts, so choose wisely!
4. **Score and Feedback**: Earn points for correct answers or guesses. Get instant feedback on each response, including your current score and response time.
5. **Completion**: Once the game ends, see your final score, average response time, and summary. Enjoy the positive feedback and celebrate your achievement!
6. Enjoy the quiz, and good luck! 🧠✨
<!-- ------------------------------------------------------- -->
## 📍 Math Quiz Mode - Custom Protocol

| Status Code | Phrase                            | Description                                                                                       |
|-------------|-----------------------------------|---------------------------------------------------------------------------------------------------|
| 100 🙌🏻      | You’ve Got This!                  | Response when a level is selected, encouraging the player.                                        |
| 101 📊      | Score Updated                     | Sent after each answer to update the player's score.                                              |
| 200 👏🏻      | Nailed It!                        | Sent for a correct answer.                                                                        |
| 300 💡      | Question Incoming                 | Sent before sending each new question.                                                            |
| 400 ⚠️       | Oops! Wrong Format                | For unexpected characters (e.g., letters when a number is expected).                              |
| 401 🚫      | Only Numbers Allowed!             | For alphabetic characters in numeric-only answers.                                                |
| 404 ❌      | Try Again!                        | For incorrect answers.                                                                            |
| 410 🎉      | Quiz Complete! Thanks for Playing!| Sent after the last question is answered or the quiz ends.                                        |
| 411 👋🏻      | Goodbye! Thanks for playing!      | Sent after the user type 'quit' to end the game.                                                  |

<!-- ------------------------------------------------------- -->
## 📍 Hangman Mode - Custom Protocol

| Status Code | Phrase                            | Description                                                                                       |
|-------------|-----------------------------------|---------------------------------------------------------------------------------------------------|
| 100 👀      | Ready, Set, Guess!                | Initial message when the game starts.                                                             |
| 200 👍🏻      | Nice Choice!                      | For a correct guess.                                                                              |
| 202 🙂‍↔️      | Already Tried That!               | When a letter has already been guessed.                                                           |
| 400 🚫      | No Digits Allowed                 | When a number is entered instead of a letter.                                                     |
| 401 ❗️      | Special Characters Not Allowed    | For special character inputs.                                                                     |
| 404 ❌      | Wrong Guess                       | For an incorrect guess.                                                                           |
| 410 🎉      | You Win! The Word Was "..."       | For completing the word successfully.                                                             |
| 411 😞      | Game Over - The Word Was "..."    | For exhausting all attempts without guessing the word.                                            |