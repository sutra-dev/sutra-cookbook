# AI Travel Planner 🌍✈️

An intelligent Streamlit application that generates personalized travel plans in over 50 languages using Sutra LLM for multilingual support and SerpAPI for real-time travel data.

![AI Travel Planner](https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png)

## Features

- **Multilingual Support**: Create travel plans in 50+ languages including English, Hindi, Japanese, Arabic, Spanish, and many more
- **Real-time Flight Search**: Find and compare the cheapest flights using SerpAPI integration with Google Flights
- **Personalized Itineraries**: Generate custom day-by-day travel plans based on preferences and themes
- **Hotel & Restaurant Recommendations**: Discover top accommodations and dining options at your destination
- **Activity Suggestions**: Get personalized activity recommendations based on your interests
- **Travel Themes**: Choose from family vacations, adventure trips, or solo explorations
- **Budget Controls**: Specify your preferred budget level and travel class
- **Essential Travel Info**: Access visa requirements, travel insurance options, and currency exchange rates

## Installation

### Prerequisites

- Python 3.7+
- Streamlit
- Sutra API key (obtain from [Two.AI](https://www.two.ai/sutra/api))
- SerpAPI key (obtain from [SerpAPI](https://serpapi.com/))

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/ai-travel-planner
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `requirements.txt` file with the following dependencies:
   ```
   streamlit
   serpapi
   agno
   langchain-openai
   python-dotenv
   ```

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. In the sidebar:
   - Enter your Sutra API key and SerpAPI key
   - Select your preferred language for the travel plan
   - Set travel preferences (budget, flight class, hotel rating)
   - Enable travel essentials (visa requirements, insurance, currency converter)

3. Configure your trip:
   - Enter departure and destination cities (using IATA codes)
   - Select your travel theme
   - Specify your preferred activities
   - Set departure and return dates

4. Generate your travel plan:
   - Click "Generate Travel Plan" to create a comprehensive itinerary
   - Review flight options, accommodations, restaurants, and daily activities
   - All information will be displayed in your selected language

## Configuration Options

### Languages
The app supports 50+ languages including:
- English, Hindi, Gujarati, Bengali, Tamil
- Arabic, French, German, Spanish, Chinese
- Japanese, Korean, Russian, and many more

### Travel Themes
- Family Vacation
- Adventure Trip
- Solo Exploration

### Budget Preferences
- Economy
- Standard
- Luxury

### Flight Classes
- Economy
- Business
- First Class

### Hotel Ratings
- 3⭐
- 4⭐
- 5⭐

## AI Components

The app uses three specialized AI agents powered by Sutra LLM:

1. **Researcher Agent**: Gathers information about top attractions, safety, and local information for your destination
2. **Planner Agent**: Creates day-by-day itineraries with morning/afternoon/evening activity blocks
3. **Hotel & Restaurant Finder**: Discovers top accommodations and dining options based on your preferences

## Flight Search Integration

Real-time flight data is retrieved using SerpAPI's Google Flights integration, allowing the app to:
- Find the cheapest flights between your departure and destination cities
- Display key details like airline, price, and duration
- Provide direct booking links when available

## Translation System

All content can be automatically translated to your preferred language using Sutra LLM, including:
- Flight information and booking links
- Hotel and restaurant recommendations
- Daily itineraries and activity suggestions
- Destination research and local information

## Environment Variables

You can set the following environment variables instead of entering them in the UI:
- `SERPAPI_KEY`: Your SerpAPI key
- `SUTRA_API_KEY`: Your Sutra API key

## Data Privacy

- No user data is stored or shared
- API calls to SerpAPI and Sutra LLM are made only for generating travel plans
- All generated content remains within your local session

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [SerpAPI](https://serpapi.com/) for real-time flight and travel data
- [Two.AI](https://www.two.ai/) for the Sutra LLM API providing multilingual capabilities
- [Agno](https://docs.agno.com/introduction) for the agent framework
- [Streamlit](https://streamlit.io/) for the web application framework

---

Built with ❤️ using [Streamlit](https://streamlit.io), [Sutra LLM](https://docs.two.ai/), and [SerpAPI](https://serpapi.com/)