import streamlit as st
import json
import os
from serpapi import GoogleSearch 
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai.like import OpenAILike
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


# Set up Streamlit UI with a travel-friendly theme
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# Define supported languages - MOVED TO THE TOP
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", 
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", 
    "Tagalog", "Swahili"
]

# Sidebar Setup - API Keys at Top
st.sidebar.title("🌎 Travel Assistant")

# Sutra API Key
st.sidebar.markdown("1. *🌐 Sutra API Key*")
st.sidebar.markdown("Get your free key from [Sutra API](https://www.two.ai/sutra/api)")
sutra_api_key = st.sidebar.text_input("Enter your Sutra API Key:", type="password", key="sutra_key")

# SerpAPI Key 
st.sidebar.markdown("2. *🔍 SerpAPI Key*")
st.sidebar.markdown("Get your key from [SerpAPI](https://serpapi.com/)")
serpapi_key_input = st.sidebar.text_input("Enter your SerpAPI Key:", type="password", key="serpapi_key")

# Language selector in sidebar only
st.sidebar.subheader("🌐 Language Settings")
output_language = st.sidebar.selectbox("Select language for your travel plan:", languages, key="sidebar_language_selector")


# Travel Preferences
st.sidebar.subheader("✈️ Travel Preferences")
budget = st.sidebar.selectbox("💰 Budget Preference:", ["Economy", "Standard", "Luxury"])
flight_class = st.sidebar.selectbox("✈️ Flight Class:", ["Economy", "Business", "First Class"])
hotel_rating = st.sidebar.selectbox("🏨 Preferred Hotel Rating:", ["3⭐", "4⭐", "5⭐"])

# Travel Essentials
st.sidebar.subheader("🛂 Travel Essentials")
visa_required = st.sidebar.checkbox("🛃 Check Visa Requirements")
travel_insurance = st.sidebar.checkbox("🛡️ Get Travel Insurance")
currency_converter = st.sidebar.checkbox("💱 Currency Exchange Rates")

st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ff5733;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
        }
        .stSlider > div {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
        }
        .translation-box {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            background-color: #f9f9f9;
        }
        .expander-header {
            color: #0066cc;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and subtitle
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="63"/>  AI-Powered Travel Planner ✈️</h1>', unsafe_allow_html=True)

# User Inputs Section
st.markdown("### 🌍 Where are you headed?")
source = st.text_input("🛫 Departure City (IATA Code):", "BOM")  # Example: BOM for Mumbai
destination = st.text_input("🛬 Destination (IATA Code):", "DEL")  # Example: DEL for Delhi  

st.markdown("### 🎭 Select Your Travel Theme")
travel_theme = st.selectbox(
    "🎭 Select Your Travel Theme:",
    ["👨‍👩‍👧‍👦 Family Vacation", "🏔️ Adventure Trip", "🧳 Solo Exploration"],
    index=0  # Set Family Vacation as default
)

# Divider for aesthetics
st.markdown("---")

st.markdown(
    f"""
    <div style="
        text-align: center; 
        padding: 15px; 
        background-color: #d2d2d4; 
        border-radius: 10px;
        color: black; 
        margin-top: 20px;
    ">
        <h3>🌟 Your {travel_theme} to {destination} is about to begin! 🌟</h3>
        <p>Let's find the best flights, stays, and experiences for your unforgettable journey.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

def format_datetime(iso_string):
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%b-%d, %Y | %I:%M %p")  # Example: Mar-06, 2025 | 6:20 PM
    except:
        return "N/A"

activity_preferences = st.text_area(
    "🌍 What activities do you enjoy? (e.g., relaxing on the beach, exploring historical sites, nightlife, adventure)",
    "Relaxing on the beach, exploring historical sites"
)

departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")

# Get API keys from environment variables or UI inputs
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or serpapi_key_input
SUTRA_API_KEY = os.getenv("SUTRA_API_KEY") or sutra_api_key

# Validate API keys
if not SERPAPI_KEY:
    st.sidebar.error("⚠️ SerpAPI key is required.")

if not SUTRA_API_KEY:
    st.sidebar.error("⚠️ Sutra API key is required.")

# Initialize Sutra model for translations
@st.cache_resource
def get_sutra_model(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
    )

# Function to translate text using Sutra LLM
def translate_text(text, target_language, sutra_api_key):
    if not sutra_api_key or target_language == "English":
        return text
    
    try:
        sutra = get_sutra_model(sutra_api_key)
        translation_prompt = f"Translate the following text to {target_language}. Keep all formatting including bullet points, numbers, and emojis intact. Here's the text:\n\n{text}"
        
        messages = [HumanMessage(content=translation_prompt)]
        response = sutra.invoke(messages)
        
        return response.content
    except Exception as e:
        st.warning(f"Translation error: {str(e)}. Showing original text.")
        return text

# Function to fetch flight data
def fetch_flights(source, destination, departure_date, return_date):
    params = {
        "engine": "google_flights",
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": str(departure_date),
        "return_date": str(return_date),
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results

# Function to extract top 3 cheapest flights
def extract_cheapest_flights(flight_data):
    best_flights = flight_data.get("best_flights", [])
    sorted_flights = sorted(best_flights, key=lambda x: x.get("price", float("inf")))[:3]  # Get top 3 cheapest
    return sorted_flights

# Function to create optimized prompts for Sutra
def create_optimized_prompt(action, destination, preferences, constraints):
    """
    Creates a token-efficient prompt for Sutra by focusing on essential information
    
    Args:
        action (str): What the agent needs to do (research, plan, find)
        destination (str): The travel destination
        preferences (str): User preferences and interests
        constraints (str): Budget, time, and other constraints
        
    Returns:
        str: An optimized prompt
    """
    # Create a focused prompt that emphasizes what's most important
    return f"{action} for {destination}. Preferences: {preferences}. Constraints: {constraints}. BE CONCISE."

# AI Agents with Sutra model
def create_sutra_agent(name, instructions):
    # Check if API key is available
    if not SUTRA_API_KEY:
        st.sidebar.error(f"⚠️ Can't initialize {name} agent: No Sutra API key provided.")
        return None
        
    # Create agent with Sutra model via OpenAILike wrapper
    return Agent(
        name=name,
        instructions=instructions,
        model=OpenAILike(
            id="sutra-v2",
            api_key=SUTRA_API_KEY,
            base_url="https://api.two.ai/v2"
        ),
        tools=[SerpApiTools(api_key=SERPAPI_KEY)] if name != "Planner" else None,
        add_datetime_to_instructions=True,
        markdown=True
    )

# Function to display content with optional translation expander
# This function is no longer needed since we're showing directly in preferred language
# Removing this function as it's not needed anymore

# Initialize agents
researcher_instructions = [
    "FOCUS on key attractions, safety, and local information.",
    "PRIORITIZE reliable sources and official travel guides.",
    "BE CONCISE - focus on must-know facts only.",
    "LIMIT output to 5-7 key attractions or activities."
]

planner_instructions = [
    "CREATE brief day-by-day itinerary with morning/afternoon/evening blocks.",
    "INCLUDE only 2-3 activities per time block.",
    "FOCUS on logistics, timing, and estimated costs.",
    "KEEP descriptions brief but informative."
]

hotel_restaurant_instructions = [
    "FIND 3-5 top hotels and restaurants near popular attractions.",
    "INCLUDE price range, rating, and 1-2 key features for each.",
    "PRIORITIZE results matching user preferences.",
    "FORMAT as concise bullet points."
]

# Generate Travel Plan
if st.button("🚀 Generate Travel Plan"):
    # Check API keys first
    if not SERPAPI_KEY or not SUTRA_API_KEY:
        st.error("⚠️ Both SerpAPI and Sutra API keys are required to generate a travel plan.")
        st.stop()
    
    # Calculate number of days
    num_days = (return_date - departure_date).days + 1  # Add 1 to include both departure and return days
    
    # Create agents with Sutra model
    researcher = create_sutra_agent("Researcher", researcher_instructions)
    planner = create_sutra_agent("Planner", planner_instructions) 
    hotel_restaurant_finder = create_sutra_agent("Hotel & Restaurant Finder", hotel_restaurant_instructions)
    
    if not researcher or not planner or not hotel_restaurant_finder:
        st.error("⚠️ Failed to initialize AI agents. Please check your API keys.")
        st.stop()
    
    with st.spinner("✈️ Fetching best flight options..."):
        flight_data = fetch_flights(source, destination, departure_date, return_date)
        cheapest_flights = extract_cheapest_flights(flight_data)

    # Hide intermediate processing and only show final results
    with st.spinner("🔍 Processing your travel plan..."):
        # Research attractions & activities
        research_prompt = create_optimized_prompt(
            action="Research top attractions and activities",
            destination=destination,
            preferences=f"Trip type: {travel_theme}. Activities: {activity_preferences}.",
            constraints=f"Budget: {budget}. Duration: {num_days} days."
        )
        
        # Get research output without streaming
        research_response = researcher.run(research_prompt, stream=False)
        research_output = research_response.content if hasattr(research_response, 'content') else str(research_response)
        
        # Hotels & restaurants
        hotel_restaurant_prompt = create_optimized_prompt(
            action="Find top hotels and restaurants",
            destination=destination,
            preferences=f"Trip type: {travel_theme}. Hotel rating: {hotel_rating}.",
            constraints=f"Budget: {budget}. Activities nearby: {activity_preferences}."
        )
        
        # Get hotel output without streaming
        hotel_response = hotel_restaurant_finder.run(hotel_restaurant_prompt, stream=False)
        hotel_output = hotel_response.content if hasattr(hotel_response, 'content') else str(hotel_response)
        
        # Simplified flight data for token efficiency
        simplified_flights = []
        for flight in cheapest_flights:
            simplified_flights.append({
                "airline": flight.get("airline", "Unknown"),
                "price": flight.get("price", "N/A"),
                "duration": flight.get("total_duration", "N/A")
            })
        
        # Create itinerary
        planning_prompt = create_optimized_prompt(
            action=f"Create {num_days}-day itinerary",
            destination=destination,
            preferences=f"Trip type: {travel_theme}. Activities: {activity_preferences}.",
            constraints=f"Budget: {budget}. Class: {flight_class}. Hotel: {hotel_rating}."
        )
        
        # Add research data but keep it brief
        planning_prompt += f" Based on: {research_output[:500]}... {hotel_output[:500]}..."
        
        # Get itinerary output without streaming
        itinerary_response = planner.run(planning_prompt, stream=False)
        itinerary_output = itinerary_response.content if hasattr(itinerary_response, 'content') else str(itinerary_response)
        
        # Translate all content to preferred language if not English
        if output_language != "English":
            research_output = translate_text(research_output, output_language, SUTRA_API_KEY)
            hotel_output = translate_text(hotel_output, output_language, SUTRA_API_KEY)
            itinerary_output = translate_text(itinerary_output, output_language, SUTRA_API_KEY)

    # Display Results - directly in preferred language, no expandable sections
    st.subheader("✈️ Cheapest Flight Options")
    if cheapest_flights:
        cols = st.columns(len(cheapest_flights))
        for idx, flight in enumerate(cheapest_flights):
            with cols[idx]:
                airline_logo = flight.get("airline_logo", "")
                airline_name = flight.get("airline", "Unknown Airline")
                price = flight.get("price", "Not Available")
                total_duration = flight.get("total_duration", "N/A")
                
                flights_info = flight.get("flights", [{}])
                departure = flights_info[0].get("departure_airport", {})
                arrival = flights_info[-1].get("arrival_airport", {})
                airline_name = flights_info[0].get("airline", "Unknown Airline") 
                
                departure_time = format_datetime(departure.get("time", "N/A"))
                arrival_time = format_datetime(arrival.get("time", "N/A"))
                
                departure_token = flight.get("departure_token", "")

                # Use translated labels based on selected language
                if output_language != "English":
                    departure_label = translate_text("Departure:", output_language, SUTRA_API_KEY)
                    arrival_label = translate_text("Arrival:", output_language, SUTRA_API_KEY)
                    duration_label = translate_text("Duration:", output_language, SUTRA_API_KEY)
                    book_now = translate_text("Book Now", output_language, SUTRA_API_KEY)
                else:
                    departure_label = "Departure:"
                    arrival_label = "Arrival:"
                    duration_label = "Duration:"
                    book_now = "Book Now"

                booking_link = "#"  # Default value
                if departure_token:
                    try:
                        params = {
                            "engine": "google_flights",
                            "departure_id": source,
                            "arrival_id": destination,
                            "outbound_date": str(departure_date),
                            "return_date": str(return_date),
                            "currency": "INR",
                            "hl": "en",
                            "departure_token": departure_token,
                            "api_key": SERPAPI_KEY
                        }
                        search_with_token = GoogleSearch(params)
                        results_with_booking = search_with_token.get_dict()
                        
                        # Check if we have valid booking data
                        if 'best_flights' in results_with_booking and len(results_with_booking['best_flights']) > idx:
                            booking_token = results_with_booking['best_flights'][idx].get('booking_token')
                            if booking_token:
                                booking_link = f"https://www.google.com/travel/flights?tfs={booking_token}"
                    except Exception as e:
                        st.warning(f"Could not fetch booking link: {str(e)}")
                        booking_link = "#"

                # Flight card layout with improved visibility for dark mode
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #ddd; 
                        border-radius: 10px; 
                        padding: 15px; 
                        text-align: center;
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                        background-color: rgba(249, 249, 249, 0.9);
                        margin-bottom: 20px;
                    ">
                        <img src="{airline_logo}" width="100" alt="Flight Logo" style="background-color: white; padding: 5px; border-radius: 5px;" />
                        <h3 style="margin: 10px 0; color: #333;">{airline_name}</h3>
                        <p style="color: #333;"><strong>{departure_label}</strong> {departure_time}</p>
                        <p style="color: #333;"><strong>{arrival_label}</strong> {arrival_time}</p>
                        <p style="color: #333;"><strong>{duration_label}</strong> {total_duration} min</p>
                        <h2 style="color: #008000;">💰 {price}</h2>
                        <a href="{booking_link}" target="_blank" style="
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            font-weight: bold;
                            color: #fff;
                            background-color: #007bff;
                            text-decoration: none;
                            border-radius: 5px;
                            margin-top: 10px;
                        ">🔗 {book_now}</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        no_flights_message = "⚠️ No flight data available."
        if output_language != "English":
            no_flights_message = translate_text(no_flights_message, output_language, SUTRA_API_KEY)
        st.warning(no_flights_message)

    # Display content directly in preferred language
    st.subheader("🏨 Hotels & Restaurants")
    st.markdown(hotel_output)
    
    st.subheader("🗺️ Your Personalized Itinerary")
    st.markdown(itinerary_output)
    
    st.subheader("🔍 Destination Research")
    st.markdown(research_output)

    success_message = "✅ Travel plan generated successfully!"
    if output_language != "English":
        success_message = translate_text(success_message, output_language, SUTRA_API_KEY)
    st.success(success_message)