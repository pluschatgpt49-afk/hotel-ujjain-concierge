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
def add_custom_css(kid_mode=False):
    base_css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Lato:wght@400;700&display=swap');
    """
    
    if kid_mode:
        css = base_css + """
        /* KID MODE - SUPER FUN DESIGN! */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFD93D 0%, #FFA500 100%) !important;
        }

        /* Typography - Fun fonts! */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Fredoka', sans-serif !important;
            color: #FFFFFF !important;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        }
        
        p, label, span, input, textarea, select, button {
            font-family: 'Fredoka', sans-serif !important;
            font-size: 1.3rem !important;
        }

        /* SUPER BIG BUTTONS */
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
            color: white !important;
            border-radius: 25px !important;
            border: 4px solid #FFDD00 !important;
            font-family: 'Fredoka', sans-serif !important;
            font-weight: bold !important;
            font-size: 1.5rem !important;
            padding: 1.5rem 2rem !important;
            min-height: 80px !important;
            box-shadow: 0 8px 15px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: scale(1.1) rotate(-2deg) !important;
            box-shadow: 0 12px 20px rgba(0,0,0,0.4) !important;
            background: linear-gradient(135deg, #FF8E53 0%, #FF6B6B 100%) !important;
        }
        .stButton > button:active {
            transform: scale(0.95) !important;
        }

        /* Service Cards */
        .service-card {
            background: white;
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            border: 5px solid transparent;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .service-card:hover {
            transform: scale(1.15) rotate(5deg);
            border-color: #FFD93D;
            box-shadow: 0 15px 30px rgba(255,217,61,0.5);
        }
        .service-icon {
            font-size: 5rem;
            margin-bottom: 15px;
        }
        .service-text {
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
        }

        /* Number Pad */
        .number-btn {
            background: linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%);
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            border-radius: 20px;
            border: none;
            padding: 25px;
            margin: 5px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: all 0.2s ease;
            min-width: 80px;
            min-height: 80px;
        }
        .number-btn:hover {
            transform: scale(1.2);
            box-shadow: 0 8px 20px rgba(0,242,254,0.5);
        }
        .number-btn:active {
            transform: scale(0.95);
        }

        /* Input Fields */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stTextArea > div > div > textarea {
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2) !important;
            border-radius: 15px !important;
            border: 3px solid #FFD93D !important;
            font-size: 1.5rem !important;
            padding: 15px !important;
        }

        /* Success Message */
        .success-celebration {
            background: linear-gradient(135deg, #00F260 0%, #0575E6 100%);
            color: white;
            font-size: 2rem;
            padding: 30px;
            border-radius: 25px;
            text-align: center;
            animation: bounce 0.5s ease;
            box-shadow: 0 10px 30px rgba(0,242,96,0.5);
        }

        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        /* Chat Bubbles */
        .stChatMessage {
            font-size: 1.3rem !important;
            padding: 20px !important;
            border-radius: 25px !important;
            margin: 15px 0 !important;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Confetti Animation */
        @keyframes confetti-fall {
            0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
        
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background: #FFD93D;
            animation: confetti-fall 3s linear;
            pointer-events: none;
        }
        </style>
        """
    else:
        css = base_css + """
        /* NORMAL MODE */
        .stApp {
            background-color: #FFFBF0;
        }

        [data-testid="stSidebar"] {
            background-color: #FFF5E1;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Fredoka', serif !important;
            color: #800000 !important;
        }
        
        p, label, span, input, textarea, select, button {
            font-family: 'Lato', sans-serif !important;
            color: #333333;
        }

        .stButton > button {
            background-color: #FF9933 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-family: 'Fredoka', serif !important;
            font-weight: bold !important;
            padding: 0.5rem 1rem !important;
        }
        .stButton > button:hover {
            background-color: #E68A00 !important;
            color: white !important;
        }

        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stTextArea > div > div > textarea {
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
            border-radius: 8px !important;
            border: 1px solid #DDD !important;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

# App Configuration
st.set_page_config(page_title="Hotel Ujjain Concierge", page_icon="🕉️", initial_sidebar_state="expanded", layout="wide")
init_db()

# Initialize session state
if "kid_mode" not in st.session_state:
    st.session_state.kid_mode = False
if "room_number" not in st.session_state:
    st.session_state.room_number = ""
if "selected_service" not in st.session_state:
    st.session_state.selected_service = None
if "show_celebration" not in st.session_state:
    st.session_state.show_celebration = False

# Sidebar - Kid Mode Toggle
st.sidebar.markdown("# 🎈 Mode Selection")
kid_mode_toggle = st.sidebar.checkbox("🎨 Kid Mode (Super Easy!)", value=st.session_state.kid_mode)
if kid_mode_toggle != st.session_state.kid_mode:
    st.session_state.kid_mode = kid_mode_toggle
    st.rerun()

add_custom_css(st.session_state.kid_mode)

# Sidebar - Mode Selection
st.sidebar.markdown("---")
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Go to", ["Guest Mode", "Manager Mode"])

# Helper functions for kid mode
def create_service_card(icon, text, service_name):
    """Create a visual service card for kid mode"""
    card_html = f"""
    <div class="service-card" onclick="this.style.borderColor='#4FACFE'">
        <div class="service-icon">{icon}</div>
        <div class="service-text">{text}</div>
    </div>
    """
    return card_html

def show_confetti():
    """Show celebration confetti"""
    st.markdown("""
    <div class="success-celebration">
        🎉 YAY! Request Sent! 🎉<br>
        <span style="font-size: 1.5rem;">Someone will help you soon!</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Add balloons
    st.balloons()

if mode == "Guest Mode":
    if st.session_state.kid_mode:
        # KID MODE INTERFACE
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🏨 Need Help? 🎈</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Tap what you need!</h3>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show selected service view OR selection menu
        if st.session_state.selected_service:
            # Back Button
            if st.button("⬅️ Go Back", key="back_btn"):
                st.session_state.selected_service = None
                st.rerun()

            if st.session_state.selected_service == "Chat":
                st.markdown("<h2 style='color: white;'>🗣️ Talk to Nandi!</h2>", unsafe_allow_html=True)
                
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Quick Reply Buttons
                st.markdown("<h3 style='color: white;'>Quick Questions:</h3>", unsafe_allow_html=True)
                qcol1, qcol2, qcol3 = st.columns(3)
                
                with qcol1:
                    if st.button("🕉️ Temple Timings", use_container_width=True):
                        prompt = "What are the temple timings?"
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        response = nandi_brain(prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                with qcol2:
                    if st.button("🍜 Where to Eat", use_container_width=True):
                        prompt = "Where can I eat good food?"
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        response = nandi_brain(prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                
                with qcol3:
                    if st.button("📶 WiFi Password", use_container_width=True):
                        prompt = "What is the WiFi password?"
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        response = nandi_brain(prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

                # Display chat messages
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Chat input
                if prompt := st.chat_input("Type your question here..."):
                    st.chat_message("user").markdown(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    response = nandi_brain(prompt)
                    
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            
            else:
                # Number Pad View for Service Requests
                st.markdown(f"<h2 style='color: white;'>✅ You picked: {st.session_state.selected_service}</h2>", unsafe_allow_html=True)
                
                # Room Number Input - Big Number Pad
                st.markdown("<h3 style='color: white;'>What's your room number?</h3>", unsafe_allow_html=True)
                
                # Display current number
                st.markdown(f"<div style='background: white; padding: 30px; border-radius: 20px; text-align: center; font-size: 3rem; font-weight: bold; color: #333; margin: 20px 0;'>{st.session_state.room_number if st.session_state.room_number else '___'}</div>", unsafe_allow_html=True)
                
                # Number Pad
                num_cols = st.columns(3)
                numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓']
                
                for i, num in enumerate(numbers):
                    col_idx = i % 3
                    with num_cols[col_idx]:
                        if st.button(num, key=f"num_{num}", use_container_width=True):
                            if num == '⌫':
                                st.session_state.room_number = st.session_state.room_number[:-1]
                            elif num == '✓':
                                if st.session_state.room_number:
                                    # Submit request
                                    add_request(st.session_state.room_number, st.session_state.selected_service, "")
                                    st.session_state.show_celebration = True
                                    st.session_state.room_number = ""
                                    st.session_state.selected_service = None
                                    st.rerun()
                            else:
                                if len(st.session_state.room_number) < 4:
                                    st.session_state.room_number += num
                            st.rerun()
                
                st.markdown("<p style='color: white; text-align: center; font-size: 1.2rem;'>Tap ⌫ to delete, ✓ to send!</p>", unsafe_allow_html=True)
                
                # Add a text note (optional)
                notes = st.text_area("Want to tell us anything? (Optional)", height=100)
                
                if st.button("🎉 Send My Request!", use_container_width=True) and st.session_state.room_number:
                    add_request(st.session_state.room_number, st.session_state.selected_service, notes)
                    st.session_state.show_celebration = True
                    st.session_state.room_number = ""
                    st.session_state.selected_service = None
                    st.rerun()

        else:
            # Service Selection Menu
            st.markdown("<h2 style='color: white;'>What do you need?</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🧻\n\nTowels", key="towels", use_container_width=True):
                    st.session_state.selected_service = "Towels"
                    st.rerun()
            with col2:
                if st.button("💧\n\nWater", key="water", use_container_width=True):
                    st.session_state.selected_service = "Water"
                    st.rerun()
            with col3:
                if st.button("🧹\n\nCleaning", key="cleaning", use_container_width=True):
                    st.session_state.selected_service = "Cleaning"
                    st.rerun()
            
            col4, col5, col6 = st.columns(3)
            
            with col4:
                if st.button("🍽️\n\nFood", key="food", use_container_width=True):
                    st.session_state.selected_service = "Room Service"
                    st.rerun()
            with col5:
                if st.button("🔧\n\nOther Help", key="other", use_container_width=True):
                    st.session_state.selected_service = "Other"
                    st.rerun()
            with col6:
                if st.button("💬\n\nChat", key="chat", use_container_width=True):
                    st.session_state.selected_service = "Chat"
                    st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color: white;'>✅ You picked: {st.session_state.selected_service}</h2>", unsafe_allow_html=True)
            
            # Room Number Input - Big Number Pad
            st.markdown("<h3 style='color: white;'>What's your room number?</h3>", unsafe_allow_html=True)
            
            # Display current number
            st.markdown(f"<div style='background: white; padding: 30px; border-radius: 20px; text-align: center; font-size: 3rem; font-weight: bold; color: #333; margin: 20px 0;'>{st.session_state.room_number if st.session_state.room_number else '___'}</div>", unsafe_allow_html=True)
            
            # Number Pad
            num_cols = st.columns(3)
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓']
            
            for i, num in enumerate(numbers):
                col_idx = i % 3
                with num_cols[col_idx]:
                    if st.button(num, key=f"num_{num}", use_container_width=True):
                        if num == '⌫':
                            st.session_state.room_number = st.session_state.room_number[:-1]
                        elif num == '✓':
                            if st.session_state.room_number:
                                # Submit request
                                add_request(st.session_state.room_number, st.session_state.selected_service, "")
                                st.session_state.show_celebration = True
                                st.session_state.room_number = ""
                                st.session_state.selected_service = None
                                st.rerun()
                        else:
                            if len(st.session_state.room_number) < 4:
                                st.session_state.room_number += num
                        st.rerun()
            
            st.markdown("<p style='color: white; text-align: center; font-size: 1.2rem;'>Tap ⌫ to delete, ✓ to send!</p>", unsafe_allow_html=True)
            
            # Add a text note (optional)
            notes = st.text_area("Want to tell us anything? (Optional)", height=100)
            
            if st.button("🎉 Send My Request!", use_container_width=True) and st.session_state.room_number:
                add_request(st.session_state.room_number, st.session_state.selected_service, notes)
                st.session_state.show_celebration = True
                st.session_state.room_number = ""
                st.session_state.selected_service = None
                st.rerun()
        
        # Show celebration if needed
        if st.session_state.show_celebration:
            show_confetti()
            st.session_state.show_celebration = False
    
    else:
        # NORMAL MODE INTERFACE
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
                    st.balloons()

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
            st.dataframe(df, use_container_width=True)

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
                    if st.button("✅ Mark as Done", key=f"done_{row['id']}"):
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
