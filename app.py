import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

# Database Setup
DB_NAME = "concierge.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  room_number TEXT,
                  service_type TEXT,
                  notes TEXT,
                  timestamp TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def add_request(room_number, service_type, notes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO requests (room_number, service_type, notes, timestamp, status) VALUES (?, ?, ?, ?, ?)",
              (room_number, service_type, notes, timestamp, 'Pending'))
    conn.commit()
    conn.close()

def get_pending_requests():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM requests WHERE status = 'Pending'", conn)
    conn.close()
    return df

def mark_as_done(request_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE requests SET status = 'Done' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

# --- Nandi Persona Logic ---
def nandi_brain(user_input):
    user_input = user_input.lower()
    
    # Greetings
    current_hour = datetime.now().hour
    greeting = "Jai Mahakal" if 4 <= current_hour < 12 else "Namaste"

    # 1. Critical Rule: Complaints (Priority)
    complaint_keywords = ["angry", "bad", "complaint", "dirty", "late", "worst", "broken", "smell", "noisy"]
    if any(word in user_input for word in complaint_keywords):
        return "I apologize sincerely. I have alerted the Manager immediately."

    # 2. Pilgrim Knowledge Base (Dictionary Lookup)
    # Format: keyword_list -> short_response
    knowledge_base = {
        # Temples & Darshan
        ("bhasma", "aarti", "morning"): "**Bhasma Aarti** is at 4:00 AM. Booking required 30 days in advance.",
        ("timing", "open", "close", "darshan"): "**General Darshan**: 4 AM - 11 PM. **Bhasma Aarti**: 4 AM.",
        ("mahakal lok", "corridor", "statue"): "**Mahakal Lok**: Entrance near Bada Ganesh. It's a 900m spiritual corridor.",
        ("kal bhairav", "liquor", "alcohol"): "**Kal Bhairav**: 5km away. Liquor is offered as Prasad here.",
        ("harsiddhi", "shakti", "peeth"): "**Harsiddhi Mata**: Near Mahakal. One of the 51 Shakti Peeths.",
        ("mangalnath", "mangal", "mars"): "**Mangalnath Temple**: Birthplace of Mars (Mangal Graha). 6km away.",
        ("sandipani", "ashram", "krishna"): "**Sandipani Ashram**: Where Lord Krishna studied. 4km away.",
        ("chintaman", "ganesh"): "**Chintaman Ganesh**: Ancient Ganesh temple. 6km away.",
        ("iskcon", "hare krishna"): "**ISKCON Ujjain**: beautiful marble temple. 3km away.",
        
        # Logistics
        ("shipra", "river", "ghat", "ram ghat"): "**Ram Ghat**: Best for evening Aarti and holy dip. 1km away.",
        ("food", "poha", "eat", "restaurant", "thali"): "**Food**: Best Poha at *Railway Station Square*. Thali at *Hotel Rajkumar*.",
        ("wifi", "internet"): "**WiFi Password**: `OmNamahShivay`",
        ("checkout", "check out", "leaving"): "**Checkout Time**: 11:00 AM.",
        ("distance", "station", "train"): "**Railway Station**: 1.5km away. Auto fare approx ₹50.",
        ("auto", "taxi", "cab", "transport"): "**Transport**: Autos are best. Standard fare ₹20-50 for nearby locations.",
        ("shopping", "market", "buy"): "**Shopping**: Buy *Batik prints* and *Stone crafts* at Gopal Mandir market.",
        
        # Spiritual
        ("mantra", "chant", "peace", "blessing"): "**Mantra**: *Om Namah Shivaya*. May Lord Shiva bless you with peace.",
        ("thank", "thanks"): "Jai Mahakal. Safe travels.",
        ("hello", "hi", "namaste"): f"{greeting}. Ask me about **Temples**, **Food**, or **Timings**."
    }

    # Search for matches
    for keywords, response in knowledge_base.items():
        if any(k in user_input for k in keywords):
            return f"{greeting}. {response}"

    # Default fallback
    return f"""{greeting}. I can help with:
    - **Temples**: Mahakal, Kal Bhairav, Harsiddhi, Mangalnath
    - **Logistics**: Timings, Auto fares, Food, WiFi
    - **Spiritual**: Ghats, Mantras
    
    Please ask specifically."""

# --- Custom CSS Injection ---
def add_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@400;700&display=swap');

        /* Main Background */
        .stApp {
            background-color: #FFFBF0;
        }

        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #FFF5E1;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Cinzel', serif !important;
            color: #800000 !important;
        }
        
        /* Specific Text Elements - Less Aggressive */
        p, label, span, input, textarea, select, button {
            font-family: 'Lato', sans-serif !important;
            color: #333333;
        }

        /* Buttons */
        .stButton > button {
            background-color: #FF9933 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-family: 'Cinzel', serif !important;
            font-weight: bold !important;
            padding: 0.5rem 1rem !important;
        }
        .stButton > button:hover {
            background-color: #E68A00 !important;
            color: white !important;
        }

        /* Input Shadows */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stTextArea > div > div > textarea {
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
            border-radius: 8px !important;
            border: 1px solid #DDD !important;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* header {visibility: hidden;}  <-- Removed to ensure Sidebar toggle is visible */
        
        /* Header Styling & Text Injection */
        header[data-testid="stHeader"] {
            background-color: #FFFBF0 !important;
            box-shadow: none !important;
        }
        
        header[data-testid="stHeader"]::after {
            content: "🕉️ Hotel Ujjain Concierge";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Cinzel', serif;
            color: #800000;
            font-size: 1.5rem;
            font-weight: bold;
            pointer-events: none;
        }

        /* Sidebar Toggle Button Styling - Force Visibility */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="stSidebarExpandButton"] {
            position: fixed !important;
            top: 15px !important;
            left: 15px !important;
            z-index: 1000002 !important;
            background-color: #FFFBF0 !important;
            border: 2px solid #800000 !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            color: #800000 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }

        [data-testid="stSidebarCollapseButton"]:hover, 
        [data-testid="stSidebarExpandButton"]:hover {
            background-color: #FFE5B4 !important;
            transform: scale(1.1) !important;
            border-color: #600000 !important;
        }

        /* Hide the default SVG which might be causing issues */
        [data-testid="stSidebarCollapseButton"] > svg, 
        [data-testid="stSidebarExpandButton"] > svg {
            display: none !important;
        }
        
        /* Force our own icon */
        [data-testid="stSidebarCollapseButton"]::after, 
        [data-testid="stSidebarExpandButton"]::after {
            content: "☰"; 
            font-size: 24px;
            color: #800000;
            font-weight: bold;
            line-height: 1;
        }
        
        </style>
        """, unsafe_allow_html=True)

# App Configuration
st.set_page_config(page_title="Hotel Ujjain Concierge", page_icon="🕉️", initial_sidebar_state="expanded")
add_custom_css()
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

# Database Setup
DB_NAME = "concierge.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  room_number TEXT,
                  service_type TEXT,
                  notes TEXT,
                  timestamp TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def add_request(room_number, service_type, notes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO requests (room_number, service_type, notes, timestamp, status) VALUES (?, ?, ?, ?, ?)",
              (room_number, service_type, notes, timestamp, 'Pending'))
    conn.commit()
    conn.close()

def get_pending_requests():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM requests WHERE status = 'Pending'", conn)
    conn.close()
    return df

def mark_as_done(request_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE requests SET status = 'Done' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

# --- Nandi Persona Logic ---
def nandi_brain(user_input):
    user_input = user_input.lower()
    
    # Greetings
    current_hour = datetime.now().hour
    greeting = "Jai Mahakal" if 4 <= current_hour < 12 else "Namaste"

    # 1. Critical Rule: Complaints (Priority)
    complaint_keywords = ["angry", "bad", "complaint", "dirty", "late", "worst", "broken", "smell", "noisy"]
    if any(word in user_input for word in complaint_keywords):
        return "I apologize sincerely. I have alerted the Manager immediately."

    # 2. Pilgrim Knowledge Base (Dictionary Lookup)
    # Format: keyword_list -> short_response
    knowledge_base = {
        # Temples & Darshan
        ("bhasma", "aarti", "morning"): "**Bhasma Aarti** is at 4:00 AM. Booking required 30 days in advance.",
        ("timing", "open", "close", "darshan"): "**General Darshan**: 4 AM - 11 PM. **Bhasma Aarti**: 4 AM.",
        ("mahakal lok", "corridor", "statue"): "**Mahakal Lok**: Entrance near Bada Ganesh. It's a 900m spiritual corridor.",
        ("kal bhairav", "liquor", "alcohol"): "**Kal Bhairav**: 5km away. Liquor is offered as Prasad here.",
        ("harsiddhi", "shakti", "peeth"): "**Harsiddhi Mata**: Near Mahakal. One of the 51 Shakti Peeths.",
        ("mangalnath", "mangal", "mars"): "**Mangalnath Temple**: Birthplace of Mars (Mangal Graha). 6km away.",
        ("sandipani", "ashram", "krishna"): "**Sandipani Ashram**: Where Lord Krishna studied. 4km away.",
        ("chintaman", "ganesh"): "**Chintaman Ganesh**: Ancient Ganesh temple. 6km away.",
        ("iskcon", "hare krishna"): "**ISKCON Ujjain**: beautiful marble temple. 3km away.",
        
        # Logistics
        ("shipra", "river", "ghat", "ram ghat"): "**Ram Ghat**: Best for evening Aarti and holy dip. 1km away.",
        ("food", "poha", "eat", "restaurant", "thali"): "**Food**: Best Poha at *Railway Station Square*. Thali at *Hotel Rajkumar*.",
        ("wifi", "internet"): "**WiFi Password**: `OmNamahShivay`",
        ("checkout", "check out", "leaving"): "**Checkout Time**: 11:00 AM.",
        ("distance", "station", "train"): "**Railway Station**: 1.5km away. Auto fare approx ₹50.",
        ("auto", "taxi", "cab", "transport"): "**Transport**: Autos are best. Standard fare ₹20-50 for nearby locations.",
        ("shopping", "market", "buy"): "**Shopping**: Buy *Batik prints* and *Stone crafts* at Gopal Mandir market.",
        
        # Spiritual
        ("mantra", "chant", "peace", "blessing"): "**Mantra**: *Om Namah Shivaya*. May Lord Shiva bless you with peace.",
        ("thank", "thanks"): "Jai Mahakal. Safe travels.",
        ("hello", "hi", "namaste"): f"{greeting}. Ask me about **Temples**, **Food**, or **Timings**."
    }

    # Search for matches
    for keywords, response in knowledge_base.items():
        if any(k in user_input for k in keywords):
            return f"{greeting}. {response}"

    # Default fallback
    return f"""{greeting}. I can help with:
    - **Temples**: Mahakal, Kal Bhairav, Harsiddhi, Mangalnath
    - **Logistics**: Timings, Auto fares, Food, WiFi
    - **Spiritual**: Ghats, Mantras
    
    Please ask specifically."""

# --- Custom CSS Injection ---
def add_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@400;700&display=swap');

        /* Main Background */
        .stApp {
            background-color: #FFFBF0;
        }

        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #FFF5E1;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Cinzel', serif !important;
            color: #800000 !important;
        }
        
        /* Specific Text Elements - Less Aggressive */
        p, label, span, input, textarea, select, button {
            font-family: 'Lato', sans-serif !important;
            color: #333333;
        }

        /* Buttons */
        .stButton > button {
            background-color: #FF9933 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-family: 'Cinzel', serif !important;
            font-weight: bold !important;
            padding: 0.5rem 1rem !important;
        }
        .stButton > button:hover {
            background-color: #E68A00 !important;
            color: white !important;
        }

        /* Input Shadows */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stTextArea > div > div > textarea {
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
            border-radius: 8px !important;
            border: 1px solid #DDD !important;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* header {visibility: hidden;}  <-- Removed to ensure Sidebar toggle is visible */
        
        </style>
        """, unsafe_allow_html=True)

# App Configuration
st.set_page_config(page_title="Hotel Ujjain Concierge", page_icon="🕉️", initial_sidebar_state="expanded")
add_custom_css()
init_db()

# Sidebar - Mode Selection
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Go to", ["Guest Mode", "Manager Mode"])

if mode == "Guest Mode":
    st.title("🕉️ Hotel Ujjain Concierge")
    st.subheader("🙏 Namaste! Welcome")
    
    # Tabs for cleaner UI
    tab1, tab2 = st.tabs(["🗣️ Chat with Nandi", "🛎️ Service Request"])
    
    with tab1:
        st.markdown("### Ask Nandi (Virtual Concierge)")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Ask about Mahakal, Food, or Services..."):
            # Display user message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get Nandi's response
            response = nandi_brain(prompt)
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with tab2:
        st.markdown("### Service Request")
        with st.form("request_form"):
            room_number = st.selectbox("Room Number", [str(i) for i in range(101, 506)])
            service_type = st.selectbox("Service Type", ["Towels", "Water", "Cleaning", "Room Service", "Other"])
            notes = st.text_area("Additional Notes (Optional)")
            submitted = st.form_submit_button("🙏 Submit Request")

            if submitted:
                add_request(room_number, service_type, notes)
                st.success(f"Request for Room {room_number} submitted successfully! We will be with you shortly.")

elif mode == "Manager Mode":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Manager Login")
    password = st.sidebar.text_input("Enter Password", type="password", help="Ask General Manager for access")

    if password == "MahakalAdmin":
        st.title("Manager Admin Panel")
        st.subheader("Pending Requests")

        df = get_pending_requests()

        if not df.empty:
            # Display as a dataframe first
            st.dataframe(df)

            st.markdown("### Action Items")
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 2])
                with col1:
                    st.write(f"**#{row['id']}**")
                with col2:
                    st.write(f"Room {row['room_number']}")
                with col3:
                    st.write(row['service_type'])
                with col4:
                    st.write(row['notes'])
                with col5:
                    if st.button("Mark as Done", key=f"done_{row['id']}"):
                        mark_as_done(row['id'])
                        st.rerun()
        else:
            st.info("No pending requests. Good job!")
    elif password:
        st.sidebar.error("Incorrect Password")

# Sidebar - Hotel Info (Moved to Bottom)
st.sidebar.markdown("---")
st.sidebar.subheader("📍 Hotel Info")
st.sidebar.info(
    """
    **Hotel Ujjain Residency**
    Mahakal Marg, Ujjain
    📞 +91 98765 43210
    """
)
st.sidebar.caption("🙏 May Mahakal Bless You")
