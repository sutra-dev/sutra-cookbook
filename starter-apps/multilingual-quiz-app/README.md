# Multilingual Quiz App 🧠

A powerful Streamlit application that allows users to create, take, and track quizzes in over 50 languages using Sutra LLM for multilingual support and the Educhain framework for quiz generation.

![Multilingual Quiz App](https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png)

## Features

- **Multilingual Support**: Create quizzes in 50+ languages including English, Hindi, Japanese, Arabic, Spanish, and many more
- **Customizable Quiz Generation**: Select topic, difficulty level, question type, and number of questions
- **Multiple Question Types**: Supports multiple choice and true/false questions
- **Quiz History Tracking**: Track performance and progress over time with built-in analytics
- **Save and Manage Quizzes**: Create a library of quizzes that can be taken anytime
- **Detailed Explanations**: Includes explanations for answers to enhance learning
- **Intuitive UI**: Clean, user-friendly interface with progress tracking during quizzes

## Installation

### Prerequisites

- Python 3.7+
- Streamlit
- Sutra API key (obtain from [Two.AI](https://www.two.ai/sutra/api))

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/multilingual-quiz-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `requirements.txt` file with the following dependencies:
   ```
   streamlit
   educhain
   langchain-openai
   pandas
   ```

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. In the sidebar:
   - Enter your Sutra API key
   - Navigate between creating quizzes, viewing saved quizzes, and quiz history

3. Create a quiz:
   - Select language, question type, and difficulty
   - Enter a topic and number of questions
   - Add optional custom instructions
   - Click "Generate Quiz"

4. Take a quiz:
   - Select from saved quizzes
   - Answer questions one by one
   - View your results and explanations at the end

5. Review your history:
   - Track performance across different topics and languages
   - Analyze your progress over time

## Configuration Options

### Languages
The app supports 50+ languages including:
- English, Hindi, Gujarati, Bengali, Tamil
- Arabic, French, German, Spanish, Chinese
- Japanese, Korean, Russian, and many more

### Question Types
- Multiple Choice
- True/False

### Difficulty Levels
- Easy
- Medium
- Hard

## File Structure

- `app.py`: Main application code
- `saved_quizzes.json`: Stores generated quizzes (created automatically)
- `quiz_history.json`: Stores quiz results and history (created automatically)

## Dependencies

- [Streamlit](https://streamlit.io/): For creating the web application interface
- [Educhain](https://github.com/satvik314/educhain): Framework for educational content generation
- [Sutra LLM](https://docs.two.ai/): Multilingual language model for quiz generation
- [LangChain](https://python.langchain.com/): For LLM integration
- [Pandas](https://pandas.pydata.org/): For data manipulation and display

## How It Works

1. **Quiz Generation**: The app uses the Educhain framework with Sutra LLM to generate questions in the selected language and format.
2. **Quiz Taking**: Questions are presented one by one with options for answering.
3. **Scoring**: The app automatically scores responses and provides immediate feedback.
4. **History Tracking**: Quiz results are stored and can be analyzed to track progress.

## Data Storage

The app saves two types of files locally:
- `saved_quizzes.json`: Contains all generated quizzes
- `quiz_history.json`: Records all quiz attempts and results

## Privacy

- All data is stored locally on your device
- API calls to Sutra LLM are made for quiz generation only

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Educhain](https://github.com/satvik314/educhain) for the educational content generation framework
- [Two.AI](https://www.two.ai/) for the Sutra LLM API
- [Streamlit](https://streamlit.io/) for the web application framework

---

Built with ❤️ using [Streamlit](https://streamlit.io) and [Sutra LLM](https://docs.two.ai/)