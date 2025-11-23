from agno.agent import Agent
from agno.models.groq import Groq
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os
from datetime import datetime, timedelta
import json
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import base64

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Get API key from environment variable or session state
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Initialize session state
if "session_history" not in st.session_state:
    st.session_state.session_history = []
if "mood_tracker" not in st.session_state:
    st.session_state.mood_tracker = []
if "recovery_day" not in st.session_state:
    st.session_state.recovery_day = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "current_agent" not in st.session_state:
    st.session_state.current_agent = "Therapist"

# Inspirational quotes
RECOVERY_QUOTES = [
    "Every ending is a new beginning. 🌅",
    "Healing is not linear, and that's okay. 💝",
    "The best revenge is becoming your best self. 💪",
    "This chapter closed so a better one could open. 📖",
    "You deserve someone who chooses you every day. 🌟",
    "Pain is temporary, but the lessons are forever. 🦋",
    "Your value doesn't decrease based on someone's inability to see your worth. 👑"
]

# Embedded music for playlists
PLAYLIST_MOODS = {
    "Sad & Reflective": {
        "description": "For when you need to feel your emotions and process the pain",
        "songs": [
            {
                "title": "Someone Like You - Adele",
                "spotify": "https://open.spotify.com/track/1zwMYTA5nlNjZxYrvBB2pV",
                "youtube": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"
            },
            {
                "title": "The Night We Met - Lord Huron",
                "spotify": "https://open.spotify.com/track/0NdAHF7HvOGZCeaKuJbK9d",
                "youtube": "https://www.youtube.com/watch?v=KtlgYxa6BMU"
            },
            {
                "title": "All Too Well - Taylor Swift",
                "spotify": "https://open.spotify.com/track/5enxwA8aAbwZbf5qCHORXi",
                "youtube": "https://www.youtube.com/watch?v=tollGa3S0o8"
            },
            {
                "title": "Drivers License - Olivia Rodrigo",
                "spotify": "https://open.spotify.com/track/7lPN2DXiMsVn7XUKtOW1CS",
                "youtube": "https://www.youtube.com/watch?v=ZmDBbnmKpqQ"
            },
            {
                "title": "When The Party's Over - Billie Eilish",
                "spotify": "https://open.spotify.com/track/43zdsphuZLzwA9k4DJhU0I",
                "youtube": "https://www.youtube.com/watch?v=pbMwTqkKSps"
            }
        ]
    },
    "Angry & Empowered": {
        "description": "Channel your anger into empowerment and strength",
        "songs": [
            {
                "title": "Since U Been Gone - Kelly Clarkson",
                "spotify": "https://open.spotify.com/track/4TQqhwM4XZfEYSRQOGV6oh",
                "youtube": "https://www.youtube.com/watch?v=R7UrFYvl5TE"
            },
            {
                "title": "Stronger - Kanye West",
                "spotify": "https://open.spotify.com/track/4fzsfWzRhPawzqhX8Qt9F3",
                "youtube": "https://www.youtube.com/watch?v=PsO6ZnUZI0g"
            },
            {
                "title": "We Are Never Getting Back Together - Taylor Swift",
                "spotify": "https://open.spotify.com/track/5YqltLsjdqFtvqE7Nrysvs",
                "youtube": "https://www.youtube.com/watch?v=WA4iX5D9Z64"
            },
            {
                "title": "Good As Hell - Lizzo",
                "spotify": "https://open.spotify.com/track/3HVWdVOQ0ZA45FuZGSfvns",
                "youtube": "https://www.youtube.com/watch?v=SmbmeOgWsqE"
            },
            {
                "title": "Truth Hurts - Lizzo",
                "spotify": "https://open.spotify.com/track/5qmq61PeM4Y5dSQiYn9l1p",
                "youtube": "https://www.youtube.com/watch?v=P00HMxdsVZI"
            }
        ]
    },
    "Healing & Moving On": {
        "description": "Songs for finding peace and moving forward with confidence",
        "songs": [
            {
                "title": "Flowers - Miley Cyrus",
                "spotify": "https://open.spotify.com/track/0yLdNVWF3Srea0uzk55zFn",
                "youtube": "https://www.youtube.com/watch?v=G7KNmW9a75Y"
            },
            {
                "title": "New Rules - Dua Lipa",
                "spotify": "https://open.spotify.com/track/2ekn2ttSfGqwhhate0LSR0",
                "youtube": "https://www.youtube.com/watch?v=k2qgadSvNyU"
            },
            {
                "title": "Survivor - Destiny's Child",
                "spotify": "https://open.spotify.com/track/7M9gKngVEKKoSjQS6OU5Ck",
                "youtube": "https://www.youtube.com/watch?v=Wmc8bQoL-J0"
            },
            {
                "title": "Unwritten - Natasha Bedingfield",
                "spotify": "https://open.spotify.com/track/6oSXNfHQgziUwfT7E25tBM",
                "youtube": "https://www.youtube.com/watch?v=b7k0a5hYnSI"
            },
            {
                "title": "Fight Song - Rachel Platten",
                "spotify": "https://open.spotify.com/track/5ykquqsGJaAO4uxLfRYPIk",
                "youtube": "https://www.youtube.com/watch?v=xo1VInw-SKc"
            }
        ]
    },
    "Self-Love Anthems": {
        "description": "Celebrate yourself and remember your worth",
        "songs": [
            {
                "title": "Love Myself - Hailee Steinfeld",
                "spotify": "https://open.spotify.com/track/6DK3kHsJMD3PpFg83dpm5B",
                "youtube": "https://www.youtube.com/watch?v=bMpFmHSgC4Q"
            },
            {
                "title": "Scars To Your Beautiful - Alessia Cara",
                "spotify": "https://open.spotify.com/track/0prNGof3XqfTvNDxHonvdK",
                "youtube": "https://www.youtube.com/watch?v=MWASeaYuHZo"
            },
            {
                "title": "Born This Way - Lady Gaga",
                "spotify": "https://open.spotify.com/track/0lPQA9gKoZFvdDHLt5a8LF",
                "youtube": "https://www.youtube.com/watch?v=wV1FrqwZyKw"
            },
            {
                "title": "Confident - Demi Lovato",
                "spotify": "https://open.spotify.com/track/1Irgqw8mSjHaEbIXi4nAhN",
                "youtube": "https://www.youtube.com/watch?v=cwKgxxYN-_U"
            },
            {
                "title": "Beautiful - Christina Aguilera",
                "spotify": "https://open.spotify.com/track/6bxhCLjZ5N1TLJ0aJesPPQ",
                "youtube": "https://www.youtube.com/watch?v=eAfyFTzZDMM"
            }
        ]
    }
}

# Available Groq models (Vision models can handle both text and images)
GROQ_MODELS = {
    "Llama 4 Maverick (Recommended)": "llama-4-maverick-17b-128e-instruct",
    "Llama 4 Scout": "llama-4-scout-17b-16e-instruct",
    "Llama 3.2 90B Vision": "llama-3.2-90b-vision-preview",
    "Llama 3.2 11B Vision": "llama-3.2-11b-vision-preview",
    "Qwen 2.5 72B": "qwen-2.5-72b-versatile",
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
}

AGENT_DESCRIPTIONS = {
    "Therapist": {
        "emoji": "🤗",
        "name": "Empathetic Therapist",
        "description": "Validates feelings and provides emotional support"
    },
    "Closure": {
        "emoji": "✍️",
        "name": "Closure Specialist",
        "description": "Helps with emotional release and moving forward"
    },
    "Coach": {
        "emoji": "📅",
        "name": "Recovery Coach",
        "description": "Creates actionable recovery plans and routines"
    },
    "Honest": {
        "emoji": "💪",
        "name": "Straight Talker",
        "description": "Provides direct, honest perspective"
    }
}

def initialize_agents(api_key: str, model_choice: str) -> dict:
    """Initialize AI agents with Groq models"""
    try:
        model = Groq(id=model_choice, api_key=api_key)
        
        agents = {
            "Therapist": Agent(
                model=model,
                name="Empathetic Therapist",
                instructions=[
                    "You are an empathetic therapist for breakup recovery.",
                    "Listen with empathy and validate feelings without judgment.",
                    "Use gentle humor when appropriate to lighten the mood.",
                    "Share relatable experiences and offer comforting words.",
                    "Analyze both text and images (if provided) for emotional context.",
                    "Keep responses conversational, warm, and supportive."
                ],
                markdown=True
            ),
            "Closure": Agent(
                model=model,
                name="Closure Specialist",
                instructions=[
                    "You help people find emotional closure after breakups.",
                    "Create templates for unsent messages to express feelings.",
                    "Guide users through emotional release exercises.",
                    "Suggest closure rituals and moving forward strategies.",
                    "Be heartfelt, authentic, and understanding.",
                    "Keep responses conversational and actionable."
                ],
                markdown=True
            ),
            "Coach": Agent(
                model=model,
                name="Recovery Coach",
                instructions=[
                    "You are a recovery coach focused on practical action.",
                    "Design daily recovery challenges and self-care routines.",
                    "Suggest social media detox strategies when needed.",
                    "Create empowering daily activities and habits.",
                    "Focus on actionable steps and positive momentum.",
                    "Keep responses practical, encouraging, and conversational."
                ],
                markdown=True
            ),
            "Honest": Agent(
                model=model,
                name="Straight Talker",
                tools=[DuckDuckGoTools()],
                instructions=[
                    "You provide honest, direct feedback about breakups.",
                    "Give objective analysis without sugar-coating.",
                    "Explain what went wrong clearly and factually.",
                    "Highlight growth opportunities and future potential.",
                    "Be blunt but constructive, never mean.",
                    "Keep responses conversational and empowering."
                ],
                markdown=True
            )
        }
        
        return agents
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None

def process_images_for_groq(files):
    """Process uploaded images for Groq vision models"""
    processed_images = []
    if not files:
        return processed_images
    
    for file in files:
        try:
            image_bytes = file.getvalue()
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"temp_{file.name}")
            
            with open(temp_path, "wb") as f:
                f.write(image_bytes)
            
            agno_image = AgnoImage(filepath=Path(temp_path))
            processed_images.append(agno_image)
        except Exception as e:
            logger.error(f"Error processing image {file.name}: {str(e)}")
            continue
    
    return processed_images

def create_pdf_report(chat_history: list, timestamp: str) -> BytesIO:
    """Generate a PDF report of the conversation"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='purple',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story = []
    story.append(Paragraph("💔 HeartMend AI Conversation", title_style))
    story.append(Paragraph(f"Generated on: {timestamp}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    for msg in chat_history:
        role = "You" if msg["role"] == "user" else msg.get("agent", "AI")
        story.append(Paragraph(f"<b>{role}:</b>", styles['Heading3']))
        clean_content = msg["content"].replace('**', '').replace('##', '').replace('*', '')
        story.append(Paragraph(clean_content, styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Made with ❤️ by HeartMend AI", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def add_mood_entry(mood: str, note: str = ""):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood,
        "note": note
    }
    st.session_state.mood_tracker.append(entry)

def get_mood_emoji(mood: str) -> str:
    mood_emojis = {
        "Great": "😄",
        "Good": "🙂",
        "Okay": "😐",
        "Sad": "😢",
        "Angry": "😠"
    }
    return mood_emojis.get(mood, "😐")

# Page config
st.set_page_config(
    page_title="💔 HeartMend AI",
    page_icon="💔",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .quote-box {
        padding: 25px;
        background: #ffffff;
        border-left: 5px solid #667eea;
        border-radius: 5px;
        margin: 20px 0;
        font-style: italic;
        color: #2c3e50;
        font-size: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .crisis-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .crisis-box h4 {
        color: white;
        margin-top: 0;
        font-size: 18px;
    }
    .crisis-box a {
        color: #fff3cd;
        text-decoration: underline;
    }
    .agent-card {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .agent-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
    }
    .agent-card.active {
        border-color: #667eea;
        background: #e8eaf6;
    }
    .chat-message {
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: #ffffff;
        border: 2px solid #667eea;
        margin-left: 15%;
        color: #2c3e50;
    }
    .ai-message {
        background: #ffffff;
        border: 2px solid #95a5a6;
        margin-right: 15%;
        color: #2c3e50;
    }
    .chat-message b {
        color: #667eea;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Configuration
    with st.expander("🔑 API Configuration", expanded=not GROQ_API_KEY):
        if GROQ_API_KEY:
            st.success("✅ API Key loaded from environment")
            api_key = GROQ_API_KEY
        else:
            api_key = st.text_input(
                "Groq API Key",
                type="password",
                help="Enter your Groq API key"
            )
            if api_key:
                st.success("✅ API Key provided")
            else:
                st.warning("⚠️ Please enter your API key")
                st.info("👉 [Get API Key](https://console.groq.com)")
        
        # Model selection
        selected_model_name = st.selectbox(
            "AI Model",
            options=list(GROQ_MODELS.keys()),
            index=0,
            help="All models support both text and images"
        )
        
        selected_model = GROQ_MODELS[selected_model_name]
    
    st.markdown("---")
    
    # Recovery Progress
    st.header("📊 Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Day", st.session_state.recovery_day)
    with col2:
        if st.button("➕", use_container_width=True):
            st.session_state.recovery_day += 1
            st.rerun()
    
    # Mood Tracker
    if st.session_state.mood_tracker:
        st.subheader("Recent Moods")
        for entry in st.session_state.mood_tracker[-3:]:
            st.caption(f"{get_mood_emoji(entry['mood'])} {entry['date'].split()[0]}")
    
    st.markdown("---")
    
    # Crisis Resources - Better Design
    st.markdown("""
        <div class="crisis-box">
            <h4>🆘 In Crisis? Get Help Now</h4>
            <p style="margin: 10px 0;"><b>🇺🇸 US Crisis Line:</b><br>Call/Text <b>988</b></p>
            <p style="margin: 10px 0;"><b>💬 Crisis Text Line:</b><br>Text <b>HOME</b> to <b>741741</b></p>
            <p style="margin: 10px 0;"><b>🌍 International:</b><br><a href="https://findahelpline.com" target="_blank">findahelpline.com</a></p>
        </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown("""
    <div class="main-header">
        <h1>💔 HeartMend AI</h1>
        <p>Your AI companion for healing and growth</p>
    </div>
""", unsafe_allow_html=True)

# Daily quote
st.markdown(f"""
    <div class="quote-box">
        {random.choice(RECOVERY_QUOTES)}
    </div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📈 Track Progress", "📚 History", "🎯 Daily Check-in", "🎵 Playlists"])

with tab1:
    # Agent selector
    st.subheader("Choose Your Support Companion")
    
    cols = st.columns(4)
    for idx, (agent_key, agent_info) in enumerate(AGENT_DESCRIPTIONS.items()):
        with cols[idx]:
            if st.button(
                f"{agent_info['emoji']} {agent_info['name']}",
                key=f"agent_{agent_key}",
                use_container_width=True,
                type="primary" if st.session_state.current_agent == agent_key else "secondary"
            ):
                st.session_state.current_agent = agent_key
                st.rerun()
            st.caption(agent_info['description'])
    
    st.markdown("---")
    
    # Display current agent
    current_agent_info = AGENT_DESCRIPTIONS[st.session_state.current_agent]
    st.info(f"💬 Chatting with **{current_agent_info['emoji']} {current_agent_info['name']}**")
    
    # Chat container
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.chat_messages:
            role = message["role"]
            content = message["content"]
            agent = message.get("agent", "")
            
            if role == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b><br>{content}</div>', unsafe_allow_html=True)
            else:
                agent_emoji = AGENT_DESCRIPTIONS.get(agent, {}).get("emoji", "🤖")
                agent_name = AGENT_DESCRIPTIONS.get(agent, {}).get("name", "AI")
                st.markdown(f'<div class="chat-message ai-message"><b>{agent_emoji} {agent_name}:</b><br>{content}</div>', unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    user_input = st.text_area(
        "Your message:",
        height=120,
        placeholder="Share what's on your mind...",
        key="chat_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        send_button = st.button("💬 Send Message", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    uploaded_files = None
    
    # Handle clear
    if clear_button:
        st.session_state.chat_messages = []
        st.rerun()
    
    # Handle send
    if send_button and user_input:
        if not api_key:
            st.error("⚠️ Please configure your API key in the sidebar")
        else:
            # Add user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # Initialize agents
            agents = initialize_agents(api_key, selected_model)
            
            if agents:
                try:
                    # Get current agent
                    current_agent = agents[st.session_state.current_agent]
                    
                    # Get response (no images)
                    with st.spinner(f"{current_agent_info['emoji']} Responding..."):
                        response = current_agent.run(user_input)
                        
                        # Add AI response
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": response.content,
                            "agent": st.session_state.current_agent,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Export conversation
    if st.session_state.chat_messages:
        st.markdown("---")
        if st.button("📥 Export Conversation as PDF"):
            pdf_buffer = create_pdf_report(
                st.session_state.chat_messages,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            st.download_button(
                label="💾 Download PDF",
                data=pdf_buffer,
                file_name=f"heartmend_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )

with tab2:
    st.header("📈 Track Your Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mood Tracker")
        
        mood = st.select_slider(
            "How are you feeling?",
            options=["Angry", "Sad", "Okay", "Good", "Great"],
            value="Okay"
        )
        
        mood_note = st.text_input("Quick note (optional)")
        
        if st.button("Log Mood", use_container_width=True):
            add_mood_entry(mood, mood_note)
            st.success(f"{get_mood_emoji(mood)} Mood logged!")
            st.rerun()
    
    with col2:
        st.subheader("Recovery Milestones")
        
        milestones = {
            1: "Started healing journey",
            3: "First full day without crying",
            7: "One week strong!",
            14: "Two weeks of growth",
            30: "One month milestone! 🎉",
            60: "Two months - you're amazing!",
            90: "Three months - unstoppable! 💪"
        }
        
        for day, description in milestones.items():
            if st.session_state.recovery_day >= day:
                st.success(f"✅ Day {day}: {description}")
            else:
                st.info(f"⏳ Day {day}: {description}")
    
    if st.session_state.mood_tracker:
        st.subheader("Mood History")
        for entry in st.session_state.mood_tracker[-10:]:
            st.write(f"{get_mood_emoji(entry['mood'])} **{entry['date']}** - {entry['note']}")

with tab3:
    st.header("📚 Conversation History")
    
    if st.session_state.chat_messages:
        st.info(f"💬 {len(st.session_state.chat_messages)} messages in current conversation")
        
        with st.expander("View Full Conversation"):
            for msg in st.session_state.chat_messages:
                role = "You" if msg["role"] == "user" else msg.get("agent", "AI")
                st.markdown(f"**{role}:** {msg['content']}")
                st.caption(msg.get('timestamp', ''))
                st.markdown("---")
    else:
        st.info("No conversation yet. Start chatting in the Chat tab!")

with tab4:
    st.header("🎯 Daily Check-in")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Today's Reflection")
        gratitude = st.text_area("Three things I'm grateful for:", height=100)
        accomplishment = st.text_area("One thing I accomplished today:", height=100)
        tomorrow = st.text_area("Tomorrow I will focus on:", height=100)
    
    with col2:
        st.subheader("Self-Care Checklist")
        drank_water = st.checkbox("💧 Drank enough water")
        exercised = st.checkbox("🏃 Moved my body")
        ate_well = st.checkbox("🥗 Ate nutritious food")
        slept_well = st.checkbox("😴 Got good sleep")
        social = st.checkbox("👥 Connected with someone")
        hobby = st.checkbox("🎨 Did something I enjoy")
    
    if st.button("Complete Check-in", use_container_width=True):
        checkin_score = sum([drank_water, exercised, ate_well, slept_well, social, hobby])
        st.balloons()
        st.success(f"✅ Check-in complete! Self-care score: {checkin_score}/6")

with tab5:
    st.header("🎵 Your Healing Playlists")
    
    st.info("🎧 Click any song link below to listen on Spotify or YouTube!")
    
    for mood_name, playlist_data in PLAYLIST_MOODS.items():
        with st.expander(f"🎵 {mood_name}", expanded=False):
            st.markdown(f"*{playlist_data['description']}*")
            st.markdown("---")
            
            for idx, song in enumerate(playlist_data["songs"], 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{idx}. {song['title']}**")
                
                with col2:
                    st.markdown(f"[🎵 Spotify]({song['spotify']})")
                
                with col3:
                    st.markdown(f"[▶️ YouTube]({song['youtube']})")
                
                st.markdown("")
    
    st.markdown("---")
    st.info("💡 **Healing Tip:** Match your playlist to your current mood, then gradually shift to more uplifting music as you feel ready!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ by HeartMend AI</p>
        <p>Remember: Healing isn't linear, but you're making progress! 🌱</p>
    </div>
""", unsafe_allow_html=True)