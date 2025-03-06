import streamlit as st
from pymongo import MongoClient
from streamlit_option_menu import option_menu
import pandas as pd
from bson.objectid import ObjectId 
import cv2
import tempfile
import numpy as np
from PIL import Image
import subprocess
import time
import threading

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['AcciRescueDB']
camera_collection = db['cameras']
hospital_collection = db['hospitals']
police_collection = db['police_stations']
response_collection = db['responses']

# Function to initialize session state
def initialize_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "edit_id" not in st.session_state:  # Initialize edit_id
        st.session_state.edit_id = None
    if "accepted" not in st.session_state:
        st.session_state.accepted = False 


# Sidebar Menu (renders only when logged in)
def sidebar_menu():
    with st.sidebar:
        st.sidebar.title("Accident Detection System")
        selected = option_menu(
            menu_title="Main Menu",
            options=["Dashboard", "Camera", "Hospital", "Police", "Detection System"],
            icons=["house", "camera", "hospital", "shield"],
            menu_icon="menu",
            default_index=0,
        )
        st.session_state.page = selected

        # Logout button in the sidebar
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

# "Go Back" Button
def go_back():
    if st.button("Go Back"):
        st.session_state.page = "Dashboard"
        st.rerun()

# Login Page
def login():
    st.title("Welcome to ACCIRESCUE")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Accirescue" and password == "Accirescue":
            st.session_state.logged_in = True
            st.session_state.user = {"username": username}
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# Dashboard Page
def dashboard_page():
    st.title("ACCIRESCUE Dashboard")
    st.write("Welcome to the ACCIRESCUE Dashboard!")
    
    tabs = st.tabs(["What We Offer", "Why ACCIRESCUE?", "How It Works", "Features", "FAQs", "Contact Us", "About Us"])

    with tabs[0]:
        st.header("What We Offer")
        st.subheader("**Instant Accident Alerts**")
        st.write("""
        - Instantly notify emergency responders of an accident.  
        - Provide real-time accident location and critical details for immediate action.  
        - Automatically notify nearby hospitals within a defined radius.  
        """)
        
        st.subheader("**Emergency Routing**")
        st.write("""
        - Provide **shortest-route navigation** for ambulances and responders.  
        - Dynamically update routes based on real-time traffic and road conditions.  
        - Notify hospitals of incoming emergencies with an estimated time of arrival.  
        """)
        
        st.subheader("**Hospital Response System**")
        st.write("""
        - Nearby hospitals within a **5 km radius** receive **Accept/Decline** alerts for accident cases.  
        - If no response is received within **2 minutes**, hospitals within a **10 km radius** are notified.  
        - Accepted cases show the hospital's location and estimated time of arrival.  
        """)

    # Why ACCIRESCUE Tab
    with tabs[1]:
        st.header("Why ACCIRESCUE?")
        st.write("""
        - **Precision Alerts**: Notifications are sent instantly to first responders, ensuring no time is wasted.  
        - **Real-Time Data**: Updates routes and alerts dynamically based on evolving road and traffic conditions.  
        - **Localized Assistance**: Support in regional languages for clarity and accuracy during critical moments.  
        - **Automated Communication**: Hospitals and responders are seamlessly notified with relevant details.  
        """)

    # How It Works Tab
    with tabs[2]:
        st.header("How It Works")
        st.write("""
        1. **Accident Detection**  
        Using advanced algorithms and IoT sensors (if connected), accidents are detected automatically.  

        2. **Immediate Alerts**  
        Victim’s location and accident details are sent to responders, nearby hospitals, and registered emergency contacts.  

        3. **Hospital Coordination**  
        - Hospitals within **5 km** are notified first.  
        - If no hospital responds within **2 minutes**, hospitals within a **10 km radius** are contacted.  
        - Accepted cases display hospital details and estimated time of arrival.  

        4. **Shortest Route Navigation**  
        Ambulances are guided through the **quickest and safest route** to the accident site and hospital.  
        """)

    # Features Tab
    with tabs[3]:
        st.header("Features")
        st.write("""
        - **Smart Radius Notifications**: Automatically contacts hospitals and emergency services based on location proximity.  
        - **Real-Time Tracking**: Monitor the ambulance’s progress and estimated time of arrival.  
        - **Two-Way Communication**:  
            - Hospitals can **accept/decline** emergency cases with a single click.  
            - Victims’ families receive updates on hospital responses and status.  
        - **Multilingual Support**: Ensure accurate communication in the victim’s preferred language.  
        - **Traffic-Aware Routing**: Avoid congested routes with real-time traffic analysis.  
        """)

    # FAQs Tab
    with tabs[4]:
        st.header("FAQs")
        st.subheader("**What happens if no hospital accepts within the radius?**")
        st.write("If hospitals within a **5 km radius** decline or don’t respond, hospitals in the **next radius (10 km)** are notified automatically.")
        
        st.subheader("**How are accidents detected?**")
        st.write("Accidents can be reported manually or detected via integrated sensors or connected devices.")
        
        st.subheader("**Does this work across India?**")
        st.write("Yes, ACCIRESCUE is built to function nationwide with hyper-localized mapping and routing.")
        
        st.subheader("**How do hospitals receive alerts?**")
        st.write("Hospitals are notified through our app/web platform, where they can instantly **accept or decline** cases.")

    # Contact Us Tab
    with tabs[5]:
        st.header("Contact Us")
        st.write("""
        **📧 Email**: support@accirescue.com  
        **📍 Headquarters**: #77, Heggodu, Sagara, Shivamogga, Karnataka, India - 577417  
        **📍 City Office**: C4, Majesty Block, Santara Magan Place 2, Hulimavu, Bengaluru, India - 560076  
        """)
    # about us tab
    with tabs[6]:
        st.header("About Us")
        st.write("""
    At ACCIRESCUE, we are on a relentless mission to revolutionize emergency response systems and save lives at lightning speed. Our cutting-edge technology ensures instant, life-saving accident alerts that accelerate help like never before. Whether it’s notifying first responders in real-time, routing victims to the nearest hospital with unparalleled precision, or providing critical, game-changing information when every second counts, we are at the forefront of transforming emergency care. With ACCIRESCUE, we are not just a service; we are a beacon of hope—ensuring that in the darkest moments, help arrives faster than ever. Join us as we make every second count and reshape the future of emergency response!
    """)



def detection_system():
    # Columns for better layout
    col1, col2 = st.columns(2)

    # Left Column: Go Live Camera Feed
    with col1:
        st.subheader("Live Camera Feed")
        if st.button("Go Live"):
            st.warning("Accessing live camera...")
            cap = cv2.VideoCapture(0)  # Access default webcam
            if not cap.isOpened():
                st.error("Unable to access the camera.")
            else:
                accident_detected = False
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to read from camera.")
                        break

                    # Convert frame to RGB for Streamlit
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.image(frame_rgb, caption="Live Camera Feed", use_column_width=True)

                    # Accident Detection Logic
                    if detect_accident(frame):
                        accident_detected = True
                        st.toast("Accident Detected!", icon="🚨")
                        send_notification()
                        break
                cap.release()

    # Right Column: Drag and Upload Section
    with col2:
        st.subheader("Upload Video or Image")
        uploaded_file = st.file_uploader("Drag and drop a video or image for accident detection:", type=["jpg", "jpeg", "png", "mp4", "avi"])
        if uploaded_file is not None:
            # Process the uploaded file
            file_bytes = uploaded_file.read()

            # Check file type and handle accordingly
            if uploaded_file.type.startswith("image"):
                # For images
                image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                if detect_accident(image):
                    st.toast("Accident Detected in the uploaded image!", icon="🚨")
                    send_notification()
            elif uploaded_file.type.startswith("video"):
                # For videos
                st.video(BytesIO(file_bytes))
                st.info("Video uploaded successfully. Accident detection is not implemented for videos in this example.")

                
# Simulated accident detection function
def detect_accident(frame):
    return np.random.choice([True, False])  # Replace with your ML model

# Function to trigger the SMS notification
def send_notification():
    try:
        subprocess.run(["python", "sms.py"], check=True)
        st.toast("Notification sent to the nearby hospital and police!", icon="✅")
    except Exception as e:
        st.toast(f"Failed to send notification: {e}", icon="⚠️")

# Process uploaded file
def process_file(uploaded_file):
    st.info("Processing file...")
    accident_detected = False

    if uploaded_file.type.startswith("image/"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        accident_detected = detect_accident(np.array(image))
    elif uploaded_file.type.startswith("video/"):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        cap = cv2.VideoCapture(temp_file.name)

        st.text("Processing video... Hold on!")
        progress_bar = st.progress(0)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            if i % 10 == 0:  # Display every 10th frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, caption=f"Processing Frame {i}", use_container_width=True)
            if detect_accident(frame):
                accident_detected = True
                break
            progress_bar.progress((i + 1) / frame_count)
        cap.release()

    if accident_detected:
        st.toast("Accident Detected!", icon="🚨")
        send_notification()
    else:
        st.toast("No Accident Detected.", icon="✔️")

# Function to display a table with Edit and Remove buttons
def display_table(data, collection, key_prefix):
    """
    Display data in a table format with Edit and Remove buttons aligned in a single row for each entry.

    :param data: List of MongoDB documents (as dictionaries).
    :param collection: MongoDB collection to apply updates/deletions.
    :param key_prefix: Unique prefix for buttons to prevent conflicts.
    """
    if data:
        # Iterate through data and display rows with three columns
        for item in data:
            col1, col2, col3 = st.columns([3, 1, 1])  # Adjust column width ratios as needed
            with col1:
                st.write(item["name"])  # Display the Name
            with col2:
                if st.button("Edit", key=f"{key_prefix}_edit_{item['_id']}"):
                    st.session_state.edit_id = str(item["_id"])
                    st.rerun()
            with col3:
                if st.button("Remove", key=f"{key_prefix}_remove_{item['_id']}"):
                    collection.delete_one({"_id": ObjectId(item["_id"])})
                    st.success(f"Deleted {item['name']} successfully!")
                    st.rerun()
    else:
        st.write("No data available.")


# Camera Management Page with Table
# Function to check connected cameras
def get_connected_cameras(max_cameras=10):
    available_cameras = []
    for camera_id in range(max_cameras):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            available_cameras.append(camera_id)
            cap.release()
    return available_cameras

# Function to start camera streams
def start_cameras(camera_ids):
    def show_camera(camera_id):
        cap = cv2.VideoCapture(camera_id)
        placeholder = st.empty()  # Placeholder for displaying the camera stream
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                placeholder.image(frame, channels="BGR", caption=f"Camera {camera_id}", use_column_width=True)
            else:
                break
        cap.release()

    threads = []
    for cam_id in camera_ids:
        thread = threading.Thread(target=show_camera, args=(cam_id,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

# Camera Page Function
def camera_page():
    st.title("Camera Management")
    st.write("Manage cameras here.")

    # Step 1: Detect connected cameras
    st.subheader("Connected Cameras")
    connected_cameras = get_connected_cameras()
    if not connected_cameras:
        st.warning("No cameras detected.")
    else:
        st.success(f"Detected {len(connected_cameras)} cameras: {connected_cameras}")

        # Step 2: Configure cameras
        st.subheader("Configure Cameras")
        camera_data = []
        for cam_id in connected_cameras:
            with st.expander(f"Camera {cam_id}"):
                camera_name = st.text_input(f"Camera Name for Camera {cam_id}", key=f"camera_name_{cam_id}")
                lat = st.text_input(f"Latitude for Camera {cam_id}", key=f"lat_{cam_id}")
                lon = st.text_input(f"Longitude for Camera {cam_id}", key=f"lon_{cam_id}")
                address = st.text_area(f"Address for Camera {cam_id}", key=f"address_{cam_id}")
                camera_data.append({"id": cam_id, "name": camera_name, "latitude": lat, "longitude": lon, "address": address})

        # Step 3: Save Configuration
        if st.button("Save Camera Configuration"):
            all_filled = all(cam["name"] and cam["latitude"] and cam["longitude"] for cam in camera_data)
            if all_filled:
                for cam in camera_data:
                    camera_collection.update_one(
                        {"id": cam["id"]},
                        {"$set": cam},
                        upsert=True
                    )
                st.success("Camera configuration saved successfully!")
            else:
                st.error("Please fill out all fields before saving.")

        # Step 4: Start camera streams
        if st.button("Start Camera Streams"):
            st.info("Starting live streams for all connected cameras...")
            start_cameras(connected_cameras)

    # Additional: Add and Manage Cameras (Database Integration)
    st.subheader("Add or Manage Cameras")
    camera_name = st.text_input("Add Camera Name", key="new_camera_name")
    lat = st.number_input("Latitude", format="%.6f", key="new_camera_lat")
    lon = st.number_input("Longitude", format="%.6f", key="new_camera_lon")
    address = st.text_area("Address", key="new_camera_address")

    if st.session_state.get("edit_id"):
        if st.button("Update Camera"):
            camera_collection.update_one(
                {"_id": ObjectId(st.session_state["edit_id"])},
                {"$set": {"name": camera_name, "latitude": lat, "longitude": lon, "address": address}}
            )
            st.success("Camera updated successfully!")
            st.session_state["edit_id"] = None
            st.rerun()
    else:
        if st.button("Add Camera"):
            camera_collection.insert_one({"name": camera_name, "latitude": lat, "longitude": lon, "address": address})
            st.success("Camera added successfully!")
            st.rerun()

    # Step 5: Display Existing Cameras
    st.subheader("Camera List")
    cameras = list(camera_collection.find())
    for cam in cameras:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{cam['name']}**")
        with col2:
            if st.button("Edit", key=f"edit_{cam['_id']}"):
                st.session_state["edit_id"] = str(cam["_id"])
                st.rerun()
        with col3:
            if st.button("Remove", key=f"remove_{cam['_id']}"):
                camera_collection.delete_one({"_id": ObjectId(cam["_id"])})
                st.success(f"Camera {cam['name']} removed successfully!")
                st.rerun()


# Hospital Management Page with Table
def hospital_page():
    st.title("Hospital Management")
    st.write("Manage hospitals here.")
    
    st.title("Add/Edit Hospital")
    
    # Hospital Details
    hospital_name = st.text_input("Hospital Name", key="hospital_name")
    hospital_phone = st.text_input("Hospital Phone Number", key="hospital_phone")
    lat = st.number_input("Latitude", format="%.6f", key="hospital_lat")
    long = st.number_input("Longitude", format="%.6f", key="hospital_long")
    address = st.text_area("Address", key="hospital_address")
    
    # Ambulance Details
    st.subheader("Add Ambulances")
    if "ambulances" not in st.session_state:
        st.session_state.ambulances = [{"name": "", "phone": ""}]
    
    for idx, ambulance in enumerate(st.session_state.ambulances):
        st.text_input(
            f"Ambulance {idx+1} Name",
            key=f"ambulance_name_{idx}",
            value=ambulance["name"],
            on_change=lambda idx=idx: update_ambulance(idx, "name", st.session_state[f"ambulance_name_{idx}"]),
        )
        st.text_input(
            f"Ambulance {idx+1} Phone Number",
            key=f"ambulance_phone_{idx}",
            value=ambulance["phone"],
            on_change=lambda idx=idx: update_ambulance(idx, "phone", st.session_state[f"ambulance_phone_{idx}"]),
        )
        if st.button(f"Remove Ambulance {idx+1}", key=f"remove_ambulance_{idx}"):
            st.session_state.ambulances.pop(idx)
            st.rerun()
    
    if st.button("Add Another Ambulance"):
        st.session_state.ambulances.append({"name": "", "phone": ""})
    
    # Submit or Update Hospital
    if st.session_state.edit_id:
        if st.button("Update Hospital"):
            hospital_collection.update_one(
                {"_id": ObjectId(st.session_state.edit_id)},
                {
                    "$set": {
                        "name": hospital_name,
                        "phone": hospital_phone,
                        "lat": lat,
                        "long": long,
                        "address": address,
                        "ambulances": st.session_state.ambulances,
                    }
                }
            )
            st.success("Hospital updated successfully!")
            st.session_state.edit_id = None
            st.rerun()
    else:
        if st.button("Add Hospital"):
            hospital_collection.insert_one({
                "name": hospital_name,
                "phone": hospital_phone,
                "lat": lat,
                "long": long,
                "address": address,
                "ambulances": st.session_state.ambulances,
            })
            st.success("Hospital added successfully!")
            st.rerun()

    # Hospital List
    st.subheader("Hospital List")
    hospitals = list(hospital_collection.find())
    display_table(hospitals, hospital_collection, "hospital")


# Helper Function to Update Ambulance Details
def update_ambulance(idx, key, value):
    st.session_state.ambulances[idx][key] = value

# Police Management Page with Table
def police_page():
    st.title("Police Station Management")
    st.write("Manage police stations here.")
    st.title("Add Police Station")
    police_name = st.text_input("Police Station Name", key="police_name")
    phone = st.text_input("Phone Number", key="police_phone")
    lat = st.number_input("Latitude", format="%.6f", key="police_lat")
    long = st.number_input("Longitude", format="%.6f", key="police_long")
    address = st.text_area("Address", key="police_address")

    if st.session_state.edit_id:
        if st.button("Update Police Station"):
            police_collection.update_one(
                {"_id": ObjectId(st.session_state.edit_id)},
                {"$set": {"name": police_name, "phone": phone, "lat": lat, "long": long, "address": address}}
            )
            st.success("Police Station updated successfully!")
            st.session_state.edit_id = None
            st.rerun()
    else:
        if st.button("Add Police Station"):
            police_collection.insert_one({"name": police_name, "phone": phone, "lat": lat, "long": long, "address": address})
            st.success("Police Station added successfully!")
            st.rerun()

    st.subheader("Police Station List")
    police_stations = list(police_collection.find())
    display_table(police_stations, police_collection, "police")

    
# Model Testing Page

# Main App
def main():
    initialize_session()

    if not st.session_state.logged_in:
        login()
    else:
        sidebar_menu()
        if st.session_state.page == "Dashboard":
            dashboard_page()
        elif st.session_state.page == "Camera":
            camera_page()
        elif st.session_state.page == "Hospital":
            hospital_page()
        elif st.session_state.page == "Police":
            police_page()
        elif st.session_state.page == "Detection System":
            detection_system()
        

if __name__ == "__main__":
    main()
