import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
from streamlit_option_menu import option_menu
import time
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import plotly.express as px
from twilio.rest import Client
import math

load_dotenv()
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- MongoDB Setup ---
MONGO_URI = "mongodb://localhost:27017"  # Update as needed
client = MongoClient(MONGO_URI)
db = client["AcciRescueDB"]
ambulance_collection = db['ambulances']
accident_collection = db['accidents']
hospital_users = db["hospital_users"]
police_users = db["police_users"]

# --- Utility Functions ---
def hash_password(password):
    """Hash a password for secure storage."""
    return sha256(password.encode()).hexdigest()

def authenticate_user(collection, username, password):
    """Authenticate a user by checking credentials in the MongoDB collection."""
    hashed_password = hash_password(password)
    return collection.find_one({"username": username, "password": hashed_password})

def initialize_data():
    if ambulance_collection.count_documents({}) == 0:
        ambulance_collection.insert_many([
            {"name": "Ambulance A", "status": "Available", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
            {"name": "Ambulance B", "status": "Available", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
            {"name": "Ambulance C", "status": "On Call", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
            {"name": "Ambulance D", "status": "Available", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
            {"name": "Ambulance E", "status": "Available", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
            {"name": "Ambulance F", "status": "Available", "phone": "+919141137749", "lat": 12.9946955, "lon": 75.3297192},
        ])
    if accident_collection.count_documents({}) == 0:
        accident_collection.insert_one({
            "location": {"lat": 12.9902055, "lon": 75.3385524},  # Default accident location (Bangalore)
            "assigned_ambulance": None
        })

def add_user(collection, username, password):
    """Add a new user to the specified MongoDB collection."""
    try:
        hashed_password = hash_password(password)
        collection.insert_one({"username": username, "password": hashed_password})
        st.success(f"User {username} registered successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    :param lat1: Latitude of point 1
    :param lon1: Longitude of point 1
    :param lat2: Latitude of point 2
    :param lon2: Longitude of point 2
    :return: Distance in kilometers
    """
    R = 6371  # Earth's radius in km
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def generate_mock_data():
    # Patients
    patients_data = {
        "Patient ID": range(1, 101),
        "Name": [f"Patient {i}" for i in range(1, 101)],
        "Age": np.random.randint(1, 100, size=100),
        "Department": np.random.choice(["Cardiology", "Neurology", "Orthopedics", "Pediatrics"], 100),
        "Admission Date": pd.date_range("2023-01-01", periods=100).tolist(),
        "Discharge Date": [
            pd.NaT if np.random.rand() > 0.7 else pd.Timestamp("2023-01-01") + pd.to_timedelta(i, unit='d') 
            for i in range(100)
        ],
    }
    patients_df = pd.DataFrame(patients_data)

    # Staff
    staff_data = {
        "Staff ID": range(1, 51),
        "Name": [f"Staff {i}" for i in range(1, 51)],
        "Role": np.random.choice(["Doctor", "Nurse", "Technician", "Admin"], 50),
        "Department": np.random.choice(["Cardiology", "Neurology", "Orthopedics", "Pediatrics"], 50),
        "Years of Experience": np.random.randint(1, 30, size=50),
    }
    staff_df = pd.DataFrame(staff_data)

    return patients_df, staff_df

# Generate mock data
patients_df, staff_df = generate_mock_data()

# --- Dashboard Functions ---
def hospital_dashboard(username):
    """Dashboard for Hospital users."""
    with st.sidebar:
        selected = option_menu(
            menu_title=f"Welcome, {username}!",
            options=["Dashboard Home", "View Alerts","Add Ambulance","Assign Ambulance"],
            icons=["house", "bell","truck"],
            menu_icon="hospital",
            default_index=0,
        )

    # Dynamic content based on menu selection
    if selected == "Dashboard Home":
        st.title(f"Welcome to {username}'s Dashboard")
        # Tabs for Navigation
        tabs = st.tabs(["Overview", "Patient Data", "Staff Overview", "Bed Occupancy"])

        # Overview Tab
        with tabs[0]:
            st.title("Overview")
            st.markdown("### Hospital Key Metrics")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Patients", len(patients_df))
            col2.metric("Staff Members", len(staff_df))
            col3.metric("Current Occupancy (%)", np.random.randint(50, 100))

            # Admissions Over Time
            st.markdown("### Admissions Over Time")
            admissions_by_date = patients_df.groupby("Admission Date").size().reset_index(name="Admissions")
            fig = px.line(admissions_by_date, x="Admission Date", y="Admissions", title="Daily Admissions Trend")
            st.plotly_chart(fig, use_container_width=True)

        # Patient Data Tab
        with tabs[1]:
            st.title("Patient Data")
            st.markdown("### Explore Patient Records")

            # Patient Table
            st.dataframe(patients_df)

            # Filter by Department
            st.markdown("### Filter by Department")
            dept = st.selectbox("Select a Department:", patients_df["Department"].unique())
            filtered_df = patients_df[patients_df["Department"] == dept]
            st.dataframe(filtered_df)

        # Staff Overview Tab
        with tabs[2]:
            st.title("Staff Overview")
            st.markdown("### Explore Staff Records")

            # Staff Table
            st.dataframe(staff_df)

            # Role Distribution
            st.markdown("### Role Distribution")
            role_counts = staff_df["Role"].value_counts().reset_index(name="Count")  # Reset index
            role_counts.rename(columns={"index": "Role"}, inplace=True)  # Rename the index column to 'Role'

            role_fig = px.pie(
                role_counts,
                names="Role",  # Use the renamed column
                values="Count",
                title="Staff Role Distribution"
            )
            st.plotly_chart(role_fig, use_container_width=True)

        # Bed Occupancy Tab
        with tabs[3]:
            st.title("Bed Occupancy")
            st.markdown("### Current Bed Occupancy")

            # Mock Bed Occupancy Data
            bed_data = {
                "Ward": ["General", "ICU", "Emergency", "Pediatrics"],
                "Total Beds": [100, 50, 30, 20],
                "Occupied Beds": [
                    np.random.randint(50, 100),
                    np.random.randint(20, 50),
                    np.random.randint(10, 30),
                    np.random.randint(5, 20),
                ],
            }
            bed_df = pd.DataFrame(bed_data)
            bed_df["Occupancy Rate (%)"] = (bed_df["Occupied Beds"] / bed_df["Total Beds"]) * 100
            st.dataframe(bed_df)

            # Visualize Bed Occupancy
            bed_fig = px.bar(
                bed_df,
                x="Ward",
                y="Occupancy Rate (%)",
                title="Bed Occupancy Rates",
                color="Ward",
                text="Occupancy Rate (%)",
            )
            st.plotly_chart(bed_fig, use_container_width=True)


    elif selected == "View Alerts":
        st.title("View Accident Alerts accepted by the hospital here..")
        st.write("""
        - Total number of alerts received by the hospital: 10
        - Number of alerts accepted: 8
        """)

    elif selected == "Add Ambulance":
        st.subheader("Add New Ambulance")
        with st.form("add_ambulance_form"):
            name = st.text_input("Ambulance Name")
            phone = st.text_input("Driver Phone Number")
            lat = st.number_input("Latitude", format="%.6f", key="new_ambulance_lat")
            lon = st.number_input("Longitude", format="%.6f", key="new_ambulance_lon")
            status = st.selectbox("Status", ["Available", "On Call", "Departed"])
            submitted = st.form_submit_button("Add Ambulance")

            if submitted:
                if name and phone:
                    ambulance_collection.insert_one({
                        "name": name,
                        "status": status,
                        "phone": phone,
                        "lat": lat,
                        "lon": lon
                    })
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")

    elif selected == "Assign Ambulance":
        st.title("Assign Ambulance to Accident Location")
        accident = accident_collection.find_one()
        accident_lat = accident["location"]["lat"]
        accident_lon = accident["location"]["lon"]
        # Notify Police Button
        if st.button("Notify Police"):
            try:
                # Replace with actual police contact numbers
                police_contact = "+919141137749"
                message = twilio_client.messages.create(
                    body=f"Accident accepted by {st.session_state['username']}. Ambulance is departing to the accident location.",
                    from_=TWILIO_PHONE_NUMBER,
                    to=police_contact
                )
                st.toast(f"Police notified successfully!", icon="🚓")
            except Exception as e:
                st.error(f"Failed to notify police: {e}")

        # Display list of ambulances and Assign buttons
        st.subheader("Ambulance List")
        ambulances = list(ambulance_collection.find())
        for ambulance in ambulances:
            col1, col2, col3 = st.columns([1, 2, 1])  # Three columns: Name, Status, Button
            with col1:
                st.write(f"🚑 {ambulance['name']}")
            with col2:
                st.write(f"**Status**: {ambulance['status']}")
            with col3:
                # Show Assign button only for available ambulances
                if ambulance["status"] == "Available":
                    if st.button(f"Assign", key=str(ambulance["_id"])):
                        ambulance_collection.update_one({"_id": ambulance["_id"]}, {"$set": {"status": "Departed"}})
                        # Update ambulance status
                        ambulance_name = ambulance["name"]
                        driver_phone = ambulance["phone"]
                        ambulance_lat = ambulance["lat"]
                        ambulance_lon = ambulance["lon"]
                        accident_location = f"https://www.google.com/maps?q={accident_lat},{accident_lon}"

                        # Send SMS to the assigned ambulance driver
                        try:
                            message = twilio_client.messages.create(
                                body=f"Accident detected, depart immediately. Location: {accident_location}.",
                                from_=TWILIO_PHONE_NUMBER,
                                to=driver_phone
                            )
                            st.toast(f"{ambulance_name} assigned. Driver notified successfully!", icon="🚑")
                        except Exception as e:
                            st.error(f"Failed to notify the driver: {e}")

                        time.sleep(3)
                        distance = haversine_distance(accident_lat, accident_lon, ambulance_lat, ambulance_lon)
                        distance = round(distance, 2)

                        # Calculate ETA (assuming an average speed of 40 km/h)
                        avg_speed_kmh = 40
                        eta_minutes = round((distance / avg_speed_kmh) * 60)
                        st.toast(f"🚑 {ambulance['name']} is {distance} km away. Estimated time of arrival: {eta_minutes} minutes.", icon="⏱️")
                        time.sleep(4)
                        st.rerun()  # Refresh to reflect updated status
                        

        


def police_dashboard(username):
    """Dashboard for Police users."""
    with st.sidebar:
        selected = option_menu(
            menu_title=f"Welcome, {username}!",
            options=["Dashboard Home", "View Alerts"],
            icons=["house", "bell"],
            menu_icon="shield",
            default_index=0,
        )

    if selected == "Dashboard Home":
        st.title(f"Welcome to {username}'s Dashboard")
        st.write("""
        - 
        """)

    elif selected == "View Alerts":
        st.title("View Accident Alerts accepted by the police here..")
        st.write("""
        - Total number of alerts accepted by the police: 10
        """)
    


# --- Streamlit App ---
st.set_page_config(page_title="ACCIRESCUE", page_icon="🚑", layout="wide")

# --- Session State ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_type"] = None
    st.session_state["username"] = None

# --- Main App ---
if not st.session_state["authenticated"]:
    # Header Section
    st.markdown("<h1 style='text-align: center; color:black;'>ACCIRESCUE</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color:black;'>Saving Lives Through Instant Accident Alerts and Emergency Response Systems</h2>", unsafe_allow_html=True)
    
    # User Type Selection
    user_type = st.radio("Select User Type:", ["Hospital", "Police Station"], horizontal=True)
    
    # Action Selection
    action = st.selectbox("Select Action:", ["Sign In", "Sign Up"])

    # Determine Collection
    collection = hospital_users if user_type == "Hospital" else police_users

    if action == "Sign Up":
        st.subheader(f"{user_type} - Sign Up")
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if password == confirm_password:
                add_user(collection, username, password)
            else:
                st.error("Passwords do not match!")

    elif action == "Sign In":
        st.subheader(f"{user_type} - Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In"):
            user = authenticate_user(collection, username, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user_type"] = user_type
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials!")

    # Initialize Data
    #initialize_data()
    

else:
    # Redirect to the appropriate dashboard with username
    if st.session_state["user_type"] == "Hospital":
        hospital_dashboard(st.session_state["username"])
    elif st.session_state["user_type"] == "Police Station":
        police_dashboard(st.session_state["username"])
