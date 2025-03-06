from twilio.rest import Client
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import streamlit as st
from pymongo import MongoClient
import subprocess

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['AcciRescueDB']
response_collection = db['responses']
accident_collection = db['accidents']

# Initialize Twilio client
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms_notification(accident_location, recipients):
    """
    Sends SMS notifications to recipients with a link to respond to the accident.
    
    Args:
    - accident_location (str): The location of the accident.
    - recipients (dict): A dictionary of recipient roles and their phone numbers.
    """
    
    # Base URL for the response page
    base_response_url = "https://274b-36-255-85-218.ngrok-free.app"

    for role, phone_number in recipients.items():
        # Generate response link with query parameters
        response_link = base_response_url
        message_body = (
            f"Accident Alert! An accident has occurred at: {accident_location}. "
            f"Click here to respond: {response_link}"
        )

        try:
            # Send SMS
            message = twilio_client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"Notification sent to {role}: Message SID {message.sid}")

            # Log the notification in MongoDB
            response_collection.insert_one({
                "role": role,
                "phone_number": phone_number,
                "accident_location": accident_location,
                "response_link": response_link,
                "status": "Sent",
                "message_sid": message.sid,
                "accepted": False  
            })

        except Exception as e:
            print(f"Failed to send notification to {role}: {e}")
            # Log the failure in MongoDB
            response_collection.insert_one({
                "role": role,
                "phone_number": phone_number,
                "accident_location": accident_location,
                "response_link": response_link,
                "status": f"Failed: {e}",
                "accepted": False
            })

def detect_accident_and_notify(location, is_accident_detected, recipient_phone_numbers):
    """
    Detects an accident and triggers SMS notifications if confirmed.
    
    Args:
    - location (str): The location where the accident occurred.
    - is_accident_detected (bool): Whether the accident has been detected.
    - recipient_phone_numbers (dict): Dictionary of recipient roles and their phone numbers.
    """
    if is_accident_detected:
        print(f"Accident detected at {location}. Sending notifications...")
        send_sms_notification(location, recipient_phone_numbers)

    else:
        print("No accident detected. No notifications sent.")

if __name__ == "__main__":
    # Simulate accident detection
    accident = accident_collection.find_one()
    accident_lat = accident["location"]["lat"]
    accident_lon = accident["location"]["lon"]
    accident_location = f"https://www.google.com/maps?q={accident_lat},{accident_lon}"
    is_accident_detected = True

    # Phone numbers for recipients
    recipient_phone_numbers = {
        "Hospital": "+919141137749",
        "Police": "+919141137749",
    }

    detect_accident_and_notify(accident_location, is_accident_detected, recipient_phone_numbers)
