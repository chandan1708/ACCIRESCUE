
# ACCIRESCUE
INSTANT ACCIDENT
ALERTS AND SMOOTH EMERGENCY
ROUTING

The rising rate of road accidents highlights the urgent need for improved emergency
response systems to save lives and minimize traffic disruptions. AcciRescue leverages
these existing technologies to enhance emergency coordination. By harnessing live feeds
from CC cameras, the system monitors vehicle movements in real time, instantly detecting
accidents. Upon identifying an incident, it notifies the nearest ambulance service with
precise location details and offers optimal routing assistance based on current traffic
conditions. Simultaneously, nearby traffic police are alerted to clear paths for emergency
vehicles, while ambulance drivers are provided with details of the hospital to ensure timely
medical care.
This system reimagines the application of AI infrastructure in critical accident response,
enabling swift and efficient collaboration among emergency responders, traffic authorities,
and healthcare facilities. Future iterations aim to include features such as real-time
notifications for family members, keeping them informed about the status and location of
their loved ones, further enhancing its impact.

## Acknowledgements

[1] G. Venkat and P. Sriramya, “Ola Data Analysis for Dynamic Price Prediction Using
Multiple Linear Regression and Random Forest Regression,” Advances in parallel
computing, Nov. 2022, doi: https://doi.org/10.3233/apc220071.

[2]G. Qin, Q. Luo, Y. Yin, J. Sun, and J. Ye, “Optimizing matching time intervals for ride-
hailing services using reinforcement learning,” Transportation Research Part C: Emerging
Technologies, vol. 129, p. 103239, Aug. 2021, doi:
https://doi.org/10.1016/j.trc.2021.103239.

[3] J. Chakraborty, D. Pandit, F. Chan, and J. (Cecilia) Xia, “A review of Ride-Matching
strategies for Ridesourcing and other similar services,” Transport Reviews, vol. 41, no. 5,
pp. 578–599, Dec. 2020, doi: https://doi.org/10.1080/01441647.2020.1866096.

[4] V. Ganapathy, “Urban mobility in the era of sharing economy: an empirical study of
smartphone app based ridesourcing services,” Journal of Global Economy, vol. 13, no. 4,
pp. 268–289, Jan. 2018, doi: https://doi.org/10.1956/jge.v13i4.476.

[5] Y. Fu and C. Soman, “Real-time Data Infrastructure at Uber,” Proceedings of the 2021
International Conference on Management of Data, 2021.
https://www.semanticscholar.org/paper/Real-time-Data-Infrastructure-at-Uber-Fu-
Soman/dae231d3f58c7237f56a4ff5dc889d4c86d81880 (accessed Oct. 04, 2024).

[6] J.-S. Kim, H.-J. Lee, and R.-D. Oh, “Smart Integrated Multiple Tracking System
development for IOT based Target-oriented Logistics Location and Resource Service,”
International Journal of Smart Home, vol. 9, no. 5, pp. 195–204, May 2015, doi:
https://doi.org/10.14257/ijsh.2015.9.5.19.

[7] Amreen Ayesha and Komalavalli Chakravarthi, “Smart Ambulances for IoT Based
Accident Detection, Tracking and Response,” Journal of computer sciences/Journal of
computer science, vol. 19, no. 6, pp. 677–685, Jun. 2023, doi:
https://doi.org/10.3844/jcssp.2023.677.685.

[8] S. Thiede, B. Sullivan, R. Damgrave, and E. Lutters, “Real-time locating systems
(RTLS) in future factories: technology review, morphology and application potentials,”
Procedia CIRP, vol. 104, pp. 671–676, 2021, doi:
https://doi.org/10.1016/j.procir.2021.11.113.

[9] S. K. R. Mallidi, “IOT BASED SMART VEHICLE MONITORING SYSTEM,”
International Journal of Advanced Research in Computer Science, vol. 9, no. 2, pp. 738–
741, Feb. 2018, doi: https://doi.org/10.26483/ijarcs.v9i2.5870.

[10] Mohd Hakimi Zohari, Bin Zohari, Mohd Fiqri Bin, and Mohd Nazri, “GPS Based35
Vehicle Tracking System,” International Journal of Scientific & Technology Research, vol.
10, no. 04, pp. 278–282, Jun. 2021, Accessed: Oct. 04, 2024. [Online]. Available:
https://www.researchgate.net/publication/352559892_GPS_Based_Vehicle_Tracking_Sy
stem.

## Tech Stack


**Programming Language:** Python

**Computer Vision and Deep Learning Frameworks:** OpenCV, YOLOv11


**TensorFlow
Model Architectures:** CNN (Ultralytics)

**Version Control:** GitHub

**Web app:** Streamlit

**Deployment:** Shell Scripts

**Development Tools:**
VS Code,
Jupyter Notebook,
Pycharm
## Installation and Deployment

Follow these steps to set up and run the ACCIRESCUE system on your local machine.

### 1. Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8+**

### 2. Clone the Repository

Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/chandan1708/ACCI-RESCUE
cd ALP-Intelligence-Surveillance
```
### 3. Set Up a Virtual Environment

It’s recommended to create a virtual environment to manage your dependencies:

```bash
# Create a virtual environment
python -m venv ACCI.venv

# Activate the virtual environment
# On Windows:
ACCI.venv\Scripts\activate
# On macOS/Linux:
source ACCI.venv/bin/activate
```

### 4. Install Dependencies
With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries, including OpenCV, Pytorch, Ultralytics and others required for the project.

### 6. Running the Application

- To run the System admin Page
  ```bash
  streamlit run app.py
  ```
- To run the Hospital or Police station page
    ```bash
    streamlit run main.py
    ```

### 7. Verifying the Installation

Check that everything is set up correctly:

- Ensure the camera is capturing images and the models are processing them correctly.

### 8. Troubleshooting

If you encounter issues:

- Ensure all dependencies are correctly installed.
- Verify that model paths are correctly set and files are accessible.
- Check that the camera is functioning properly.
- Review the logs for any errors.

## Features

1. Automated Accident Detection
2. Real-Time Notifications
3. Optimized Emergency Routing
4. Centralized Monitoring Dashboard for both System Admin and Hospital/Police Station

## Contributing



Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeatureName`).
6. Open a pull request.

Please ensure that your code adheres to the project's coding standards and passes all tests. For more detailed information, see the `CONTRIBUTING.md` file.