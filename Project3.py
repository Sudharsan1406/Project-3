import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time
import base64


# Function to load and encode local jpg image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Local image filename (same folder)
image_file = 'ass.gif'

# Get base64 string
img_base64 = get_base64_of_bin_file(image_file)

# Inject HTML + CSS for background
page_bg_img = f"""
<style>
.stApp {{
  background-image: url("data:image/jpg;base64,{img_base64}");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}}
</style>
"""

# Load CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

model = pickle.load(open("model.pkl", "rb"))

# Define pages
def page1():
    st.markdown(""" \n \n""")
    if st.button("Go to Prediction Page"):
        return "page2"
    return "page1"

def page2():
    st.markdown(""" \n \n""")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            return "page1"
    with col2:
        if st.button("Go to Creator Info"):
            return "page3"
    return "page2"

def page3():
    st.markdown(""" \n \n""")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            return "page2"
    return "page3"

# Initialize page
if "current_page" not in st.session_state:
    st.session_state.current_page = "page1"

# Render pages
if st.session_state.current_page == "page1":
    
    st.title(' :car: TripFare : Predicting Urban Taxi Fare with Machine Learning')
  
    st.markdown(""" ##### As a Data Analyst at an urban mobility analytics firm, my mission is to unlock insights from real-world taxi trip data to enhance fare estimation 
    ##### systems and promote pricing transparency for passengers. This project focuses on analyzing historical taxi trip records collected from a
    ##### metropolitan transportation network. """)

    st.markdown(""" \n \n""")
    st.markdown(""" <style>.image-right { float : left; } </style> """, unsafe_allow_html = True, )
    st.markdown('<div class = "image-left">', unsafe_allow_html = True)
    st.image("c.jpg", width=265)
    st.markdown('</div>', unsafe_allow_html = True)
    st.markdown(""" \n \n""")
    
    st.markdown(""" \n 
    #### Skills Take Away From This Project \n
● Exploratory Data Analysis (EDA)\n  
● Data cleaning and preprocessing \n
● Data Visualization with Matplotlib & Seaborn \n
● Feature Engineering  \n
● Regression Model Building \n
● Model Evaluation & Comparison \n
● Hyperparameter Tuning \n
● Streamlit  \n""")

    next_page = page1()
    
    if next_page == "page2":
        st.session_state.current_page = "page2"
        
elif st.session_state.current_page == "page2":
    

    st.title(" Taxi Fare Prediction ")
    st.subheader("Please Provide Your Travel Details 👇 :")
    
    c1,c2,c3, c4, c5 = st.columns([1,1,1,1,1], gap = 'large')
    c6,c7,c8,c9,c10 = st.columns([1,1,1,1,1], gap = 'large')
    
    # ✅ User Input
    with c1 :
        pickup_longitude = st.slider("Pickup Longitude (-74.65 to 0) ", min_value=-74.65, max_value=0.00, step=0.01)
    with c2 :
        pickup_latitude = st.slider("Pickup Latitude (0 to 43) ", min_value=0.00, max_value=43.00, step=0.01)
    with c3 :
        dropoff_longitude = st.slider("Dropoff Longitude (-74.65 to 0) ", min_value=-74.65, max_value=0.00, step=0.01)
    with c4 :
        dropoff_latitude = st.slider("Dropoff Latitude (0 to 43) ", min_value=0.00, max_value=43.00, step=0.01)
    with c5 :
        fare_amount = st.slider("fare amount (max fare = 28) ", min_value=1.0, max_value=28.0, step=0.5)
    with c6 :
        passenger_count = st.number_input("Passenger Count ( max count = 6 )", min_value=1, max_value=6, step=1)
    with c7 :
        pickup_hour = st.slider("Pickup Time - Hour", 0, 23)
    with c8 :
        am_pm = st.selectbox("AM or PM?", options=['AM', 'PM'])
    with c9 :
        payment_type = st.selectbox("Pay Options", options=['Cash', 'Card', 'UPI', 'Wallet'])    
    with c10 :
        tip_amount = st.number_input("Tip fare", step=1)
        
        
    # ✅ map categorical input to number
    payment_map = {'Cash': 1, 'Card': 2,'UPI': 3,'Wallet': 4}
    am_pm_map = {'AM': 0, 'PM': 1}
    
    # ✅ Isert Datas
    input_data = np.array([[passenger_count, pickup_longitude, pickup_latitude,
                            dropoff_longitude, dropoff_latitude,
                            payment_map[payment_type],fare_amount, tip_amount,
                            am_pm_map[am_pm], pickup_hour]])
    
    # ✅ prediction
    if st.button("Predict the amount "):
        with st.spinner("Happy Journey Loading 😎 .."):
            time.sleep(2)
            st.markdown("##### Have a nice journey 😁 ...!")
            col1, col2 = st.columns([1,1],gap = "small") 
            
            col1.image("s.png",width = 120)
            prediction = model.predict(input_data)[0]
            total = prediction + 0.5 + 1 + 0.3 + 0.3
            col2.markdown(f"<h3>Your  Total Fare  Amount  🚕 : {total:.2f}</h3>", unsafe_allow_html = True)
            col2.markdown(" ###### (include : mta_tax,   extra_charges,   tolls_amount,   improvement_surcharge) " )
    
    next_page = page2()
    
    if next_page == "page1":
        st.session_state.current_page = "page1"
    elif next_page == "page3":
        st.session_state.current_page = "page3"

elif st.session_state.current_page == "page3":
    
    st.title("💻 Creator of this Project")
    st.markdown(""" \n \n""")
    st.write("""
#    **Developed by:** Sudharsan M S 👨‍💻 \n
##    **Skills:**      Python 🐍, Machine Learning 📈, Streamlit ⌛
    """)

    st.image('images.png', width=190)

    next_page = page3()
    if next_page == "page2":
        st.session_state.current_page = "page2"
        
    
