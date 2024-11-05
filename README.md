# QuickQuizzer 🎉
Welcome to **QuickQuizzer** – a fun, interactive quiz game you can play directly from your terminal! 
Test your knowledge with a series of questions and see how high you can score!

### How to Play 🕹️
QuickQuizzer is a simple question-and-answer game. The server asks a series of questions, and the client (that's you!) responds with your best answers.

1. **Start the Game**: Begin by typing `start` when prompted.
2. **Answer Questions**: After each question is displayed, type in your answer and press Enter.
3. **Scoring**: For each correct answer, you'll get a point. If you’re incorrect, don’t worry – just try your best on the next one!
4. **End of Quiz**: After all questions are answered, you’ll receive your final score.

### Requirements 📋
- Python 3.x installed on your machine
- A terminal to run the server and clien

### Commands to Run the Game 💻
**Step 1: Start the Server**
- In one terminal window, navigate to the directory where `quiz_server.py` is located, and run: ```python3 quiz_server.py```
- You should see a message saying: ``` Server is listening on port 12345... ```
- This means the server is ready and waiting for the client to connect.

**Step 2: Start the Client**
- In the other terminal window, navigate to the same directory, and run: ```python3 quiz_client.py```
- This will connect the client to the server. You’ll see:```Type 'start' to begin the quiz:```
- Type `start` and hit Enter to begin the quiz!

### Important Notes ⚠️
- Ensure that the server is running before starting the client.
- Both the server and client must run on the same machine or local network to connect properly.
- Use the exact command format for answers, or you may get a "Bad Request" error.

### Features ✨
- **Real-time Feedback**: Know immediately whether your answer was correct or incorrect.
- **Score Tracking**: See your score updated after each question.
- **Simple Commands**: Just type and play – it’s that easy!

Enjoy the quiz, and good luck! 🧠✨