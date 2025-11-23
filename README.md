# 💔 HeartMend AI

> Your AI-powered companion for healing and growth after a breakup

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

HeartMend AI is an empathetic AI application designed to help people navigate the emotional journey of breakup recovery. Using advanced AI models from Groq, it provides personalized support through four specialized AI companions, mood tracking, recovery plans, and curated healing playlists.

---

## ✨ Features

### 🤖 Four AI Companions
- **🤗 Empathetic Therapist** - Validates feelings and provides emotional support
- **✍️ Closure Specialist** - Helps with emotional release and moving forward
- **📅 Recovery Coach** - Creates actionable recovery plans and routines
- **💪 Straight Talker** - Provides direct, honest perspective

### 💬 Interactive Chat Interface
- Real-time conversation with AI companions
- Switch between different support styles
- Export conversations to PDF
- Clear, readable chat interface

### 📊 Progress Tracking
- Track recovery days and milestones
- Daily mood logging with history
- Visual progress indicators
- Celebrate achievements at key milestones

### 🎯 Daily Check-ins
- Gratitude journaling
- Self-care checklist
- Daily reflection prompts
- Track personal accomplishments

### 🎵 Curated Healing Playlists
- **Sad & Reflective** - Process emotions and pain
- **Angry & Empowered** - Channel anger into strength
- **Healing & Moving On** - Find peace and confidence
- **Self-Love Anthems** - Celebrate your worth

Direct links to Spotify and YouTube for immediate listening.

### 🆘 Crisis Support
- Quick access to crisis hotlines
- National and international resources
- Prominent, easy-to-find help section

---

## 🚀 Live Demo

Try the live application: [HeartMend AI on Streamlit](https://heartmendai.streamlit.app)

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Models**: Groq (Llama, Qwen)
- **AI Framework**: Agno
- **PDF Generation**: ReportLab
- **Python**: 3.8+

---

## 📋 Prerequisites

- Python 3.8 or higher
- A Groq API key (free at [console.groq.com](https://console.groq.com))
- pip (Python package installer)

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/heartmend-ai.git
cd heartmend-ai
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Get your free Groq API key:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste it into your `.env` file

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Click "Advanced settings"
   - Add your secret:
     ```toml
     GROQ_API_KEY = "your_groq_api_key_here"
     ```
   - Click "Deploy"

3. **Your app will be live at:**
   ```
   https://your-username-heartmend-ai-main-xxxxx.streamlit.app
   ```

---

## 📁 Project Structure

```
heartmend-ai/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore file
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # Streamlit Cloud secrets (not in repo)
```

---

## 🎯 Usage Guide

### Getting Started

1. **Launch the app** and select your preferred AI model in the sidebar
2. **Choose a companion** - Pick from Therapist, Closure Specialist, Coach, or Straight Talker
3. **Start chatting** - Share your feelings and thoughts
4. **Track your progress** - Log moods and check daily milestones
5. **Listen to music** - Access curated playlists for emotional support

### Switching Companions

Each AI companion offers a different support style:
- Use **Therapist** for emotional validation
- Use **Closure Specialist** for help with moving on
- Use **Recovery Coach** for practical action plans
- Use **Straight Talker** for honest, direct feedback

### Exporting Conversations

Click "Export Conversation as PDF" at the bottom of the chat to save your session for future reflection.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more AI companions with different support styles
- Integrate additional music streaming services
- Add data visualization for mood tracking
- Implement user authentication for saving progress
- Add multilingual support
- Create mobile-responsive improvements

---

## 🐛 Known Issues

- PDF export may have formatting limitations with very long conversations
- Playlist links require external internet connection
- Session data is cleared when browser is refreshed (use anonymous mode is temporary)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for providing free, fast AI model access
- **Streamlit** for the amazing web framework
- **Agno** for the AI agent framework
- All the artists whose music helps people heal

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/IdajiliJohnOjochegbe/heartmend-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/IdajiliJohnOjochegbe/heartmend-ai/discussions)

---

## 🌟 Star This Project

If HeartMend AI helped you or someone you know, please consider giving it a ⭐ on GitHub!

---

## ⚠️ Disclaimer

HeartMend AI is designed to provide emotional support and guidance, but it is **not a substitute for professional mental health care**. If you're experiencing severe emotional distress, depression, or having thoughts of self-harm, please reach out to a licensed mental health professional or contact a crisis helpline immediately.

### Crisis Resources:
- **US**: National Suicide Prevention Lifeline: 988
- **US**: Crisis Text Line: Text HOME to 741741
- **International**: [Find A Helpline](https://findahelpline.com)

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/IdajiliJohnOjochegbe/heartmend-ai?style=social)
![GitHub forks](https://img.shields.io/github/forks/IdajiliJohnOjochegbe/heartmend-ai?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/IdajiliJohnOjochegbe/heartmend-ai?style=social)

---

<div align="center">
  <p>Made with ❤️ for everyone navigating the journey of healing</p>
  <p><strong>Remember: Healing isn't linear, but you're making progress! 🌱</strong></p>
</div>
