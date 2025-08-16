# langchain-chatbot-toeic-weather
## 📌 Table of Contents
- [About](#About)
- [Pipeline](#Pipeline)
- [Features](#Features)
- [Demo](#demo)
- [Installation & Usage](#installation)
- [Tech Stack](##tech-stack)

---

## 📖 About
**TOEIC & Weather Chatbot** is an intelligent virtual assistant built with **LangChain + RAG + Agent**.  
It can:
- 📝 **Answer questions about the TOEIC exam in Vietnam**  
  Including: test format, registration locations, services, promotions, etc.
- 🌦️ **Provide the current time & weather for cities around the world**  
  Just enter the city name (e.g., *Tokyo*, *New York*, *Hà Nội*) and the bot will respond with local time, weather conditions, temperature, and more.

> **Note:** Please ask your questions in **Vietnamese** for the best results.


|Example|
| --- | 
| Thời tiết Hà Nội lúc này?    | 
| Số điện thoại và email hỗ trợ khách hàng của kì thi TOEIC?|

---
## 💡 Pipeline

![Pipeline Diagram](assets/pipeline.png)

The system follows a **Retrieval-Augmented Generation (RAG) pipeline** combined with tool-augmented agents:
1. Data ingestion & vector DB creation.
2. User query through chat interface.
3. Agent decision: call API / retrieve documents / forward to LLM.
4. Final answer returned to the user.

## ✨ Features
1. **TOEIC Q&A**
   - Detailed explanation of the test structure
   - Listening and reading tips
   - Registration guidance in Vietnam

2. **Global Time & Weather Lookup**
   - View local time for any city worldwide
   - Real-time weather information: temperature, humidity, wind, clouds/rain conditions
   - Weather data retrieved from live APIs

3. **User-Friendly Interface**
   - Alternating chat bubbles for user and bot
   - **Clear** button to reset chat history
---

## 🎥 Demo
👉 Huggingface Space: [Live Demo Link](#)  
[]()
![demo-screenshot](assets/demo.png)
![demo-screenshot](assets/demo.png)
![demo-screenshot](assets/demo.png)

---

## ⚙️ Installation & Usage
Step 1: 
```bash
# Clone this repository
git clone https://github.com/huytrinh0911/langchain-chatbot-toeic-weather.git
cd langchain-chatbot-toeic-weather

# Install dependencies
pip install -r requirements.txt
```  

Step 2:
Get the API key and then put it in the **```.env```** file:

- [google api](https://aistudio.google.com/app/apikey): to use the model 'gemini-2.5-flash'.
- [weather api](https://www.weatherapi.com/): to use the weather tool.
![Pipeline Diagram](assets/pipeline.png)

Step 3: 
```bash
python GUI.py
```
Then open [http://localhost:7860](http://localhost:7860/) in your browser.

---

## 🛠 Tech Stack

- Language: Python 3.12
    
- Framework: LangChain / Gradio
    
- Vector DB: Chroma
    
- Deployment: HuggingFace Spaces
    

---


