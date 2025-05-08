# 📚 Story Generator for Kids in Regional Languages

A Streamlit application that generates engaging, age-appropriate stories for children in multiple regional languages using the Sutra LLM.

## 🌟 Features

- **Multilingual Support**: Generate  stories in 22+ languages including Hindi, Gujarati, Bengali, Tamil, Telugu, etc.
- **Age-Appropriate Content**: Tailor stories for different age groups (3-5, 6-8, 9-12 years)
- **Customizable Stories**: Select themes, character types, settings, and moral values
- **Engaging UI**: Kid-friendly interface with icons and simple navigation
- **Educational Value**: Stories include moral lessons and discussion questions
- **Download Feature**: Save generated stories as markdown files

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shubhwithai/Sutra_Cookbooks.git
   cd Sutra_Cookbooks/starter-apps/Story_Generator_for_Kids
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Create a `.env` file with your Sutra API key:
     ```
     SUTRA_API_KEY=your_api_key_here
     ```
   - Or enter it directly in the app's sidebar

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 💡 How to Use

1. Select the story language from the sidebar
2. Choose an age group and story length
3. (Optional) Customize character types, settings, and moral values
4. Click on a story theme or enter a custom theme
5. Wait for the AI to generate a unique story
6. Read and enjoy the story, then download it if desired

## 🎨 Story Customization Options

- **24 Themes**: Adventure, Friendship, Animals, Magic, and more
- **10 Character Types**: Children, Animals, Magical Creatures, etc.
- **20 Settings**: Forest, Space, Underwater, Castle, etc.
- **20 Moral Values**: Honesty, Kindness, Courage, etc.
- **3 Name Styles**: Indian, International, and Fantasy names

## 📋 Technical Details

This application uses:
- Streamlit for the user interface
- Sutra LLM via the LangChain framework for story generation
- Pydantic for data validation and parsing
- Custom prompt engineering for age-appropriate, culturally relevant content

## 🔒 Privacy & Safety

- No data is stored from users
- Content is generated with strict safety guidelines for children
- All stories are generated with age-appropriate themes and language

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://docs.two.ai/version-2/docs/get-started-with-sutra) for the multilingual language model
- [Streamlit](https://streamlit.io) for the web app framework
- [LangChain](https://www.langchain.com) for the LLM integration
