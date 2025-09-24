import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load local .env file (only works when running locally)
load_dotenv()


# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
if not openai.api_key:
    st.error("⚠️ No API key found! Please set OPENAI_API_KEY in Streamlit Secrets or a local .env file.")


def generate_itinerary(city_name, days, interest_level):
    prompt_text = f"""
    You are a professional travel planner. Create a detailed {days}-day itinerary for a vacation in {city_name}
    for travelers interested in {interest_level}. The itinerary should be practical, enjoyable, and culturally enriching.

    For each day, provide:
    - Morning, Lunch, Afternoon, and Dinner plans with specific locations
    - Transport options (metro, taxi, bus, walking) between activities
    - Suggested timings (start and end times) for each activity
    - Estimated budget for meals and transport
    - Safety tips, local etiquette, and cultural highlights
    - Optional activities or recommendations for flexibility

    The itinerary should be easy to follow and suitable for both first-time visitors and experienced travelers.
    Include descriptions that make the experience immersive and exciting.

    Make sure the language is friendly and helpful.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and knowledgeable travel assistant."},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=800,
        temperature=0.7
    )

    itinerary = response.choices[0].message.content
    return itinerary


# Streamlit UI
st.title("🧳 Travel Itinerary Generator")
st.write("Enter your details below and get a personalized travel plan!")

city_name = st.text_input("City Name", "Varanasi")
days = st.number_input("Number of Days", min_value=1, max_value=10, value=3, step=1)
interest_level = st.text_area("Interests", "temples, spiritual sites, and local cuisine")

if st.button("Generate Itinerary"):
    with st.spinner("Planning your trip..."):
        result = generate_itinerary(city_name, days, interest_level)
        st.success("Here’s your travel itinerary:")
        st.write(result)
