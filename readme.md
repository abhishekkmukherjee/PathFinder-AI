# PathFinder AI

PathFinder AI is an AI-powered chatbot that provides career advice using Hugging Face models. It helps users with job market insights, professional development, and industry-specific recommendations. Built with Streamlit, it offers a simple and interactive chat experience. 🚀

## Features
- 💼 **AI-Powered Career Advice**: Get guidance based on industry trends.
- 🧠 **Uses GPT-2 & DistilGPT-2**: Generates career-related responses.
- 🎨 **User-Friendly UI**: Built with Streamlit for an interactive chat experience.
- 🔄 **Session Memory**: Keeps track of past interactions for smooth conversations.
- ⚙️ **Fallback Mechanism**: Uses a backup model if the primary one fails.

## Project Structure
```
PathFinder/
│── venv/                 # Virtual environment (not included in GitHub)
│── .env                  # Environment variables (API keys)
│── .gitignore            # Git ignore file
│── app.py                # Main application script
│── requirements.txt      # Dependencies
```

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PathFinder-AI.git
cd PathFinder-AI
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key
Create a `.env` file in the root directory and add your Hugging Face API key:
```
HF_API_TOKEN=your_huggingface_api_key
```

### 5. Run the Application
```bash
streamlit run app.py
```

## How It Works
1. Users enter career-related questions.
2. The chatbot sends the query to Hugging Face's GPT-2 model.
3. The AI generates a response and displays it in the chat interface.
4. If GPT-2 fails, it falls back to DistilGPT-2.

## Future Improvements
- 🔥 Upgrade to a more advanced model (GPT-4, Mistral-7B, or fine-tuned AI).
- 📚 Train a custom model on career-specific data.
- 🔍 Integrate real-time job market trends using APIs.

## License
This project is open-source under the MIT License.

## Contributions
Feel free to contribute! Open an issue or submit a pull request.

---

🚀 Built with ❤️ using Streamlit and Hugging Face!

