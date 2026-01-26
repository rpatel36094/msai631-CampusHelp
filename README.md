MSAI-631 AI-Integrated Chatbot

Rule-Based Campus Assistant + Azure AI Sentiment Analysis

This project extends a traditional rule-based chatbot by integrating Azure AI Language Services to perform sentiment analysis. 
The chatbot was originally built using the Microsoft Bot Framework Echo Bot sample and enhanced to combine structured rule-based responses with AI-powered emotional interpretation.

Project Overview

1) Rule-Based Campus Assistant
The bot responds to predefined commands:
- menu – shows available commands
- office – displays office hours
- course – shows course information
- contact – provides support contact
- reverse <text> – reverses text
- bye / exit – ends conversation

2) AI Sentiment Analysis (Azure)
- sentiment <text> → Uses Azure AI Language to detect if the text is positive, neutral, or negative.

Starting Code Source

This project is based on Microsoft’s official Bot Framework sample:
BotBuilder-Samples → Python → 02.echo-bot

Setup Instructions

Step 1 — Open Anaconda Prompt
conda activate MSAI631_MBF

Step 2 — Navigate to Project Folder
cd C:\Users\ronak\Downloads\msai631-traditional-chatbot-main\msai631-traditional-chatbot-main

Step 3 — Install Required Packages
python -m pip install -r requirements.txt

Azure AI Language Setup
Create an Azure AI Language resource in Azure Portal and copy the Endpoint URL and API Key.

Set Environment Variables
SET MicrosoftAIServiceEndpoint=https://your-resource-name.cognitiveservices.azure.com/
SET MicrosoftAPIKey=your_key_here

Run the Bot
python app.py

Test Using Bot Framework Emulator
Connect to:
http://localhost:3978/api/messages

Test Commands:
menu, office, course, contact, reverse hello, bye
Sentiment: sentiment I love this project

Security Note
Azure keys are stored using environment variables and are not included in the code or repository.

GitHub Repository
https://github.com/rpatel36094/msai631-ai-chatbot