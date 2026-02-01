MSAI-631 CampusHelp chatbot
CampusHelp is a conversational chatbot built to help students quickly access academic support information using natural language.
It extends a traditional rule-based chatbot by integrating AI-powered sentiment analysis to make interactions more supportive and context-aware.

Starting Code Source
This project is based on Microsoft’s official Bot Framework sample: BotBuilder-Samples → Python → 02.echo-bot

Setup Instructions
Step 1 — Open Anaconda Prompt conda activate MSAI631_MBF

Step 2 — Navigate to Project Folder cd C:\Users\ronak\Downloads\msai631-CampusHelp-main\msai631-CampusHelp-main

Step 3 — Install Required Packages python -m pip install -r requirements.txt

Azure AI Language Setup Create an Azure AI Language resource in Azure Portal and copy the Endpoint URL and API Key.

Set Environment Variables SET MicrosoftAIServiceEndpoint=https://your-resource-name.cognitiveservices.azure.com/ SET MicrosoftAPIKey=your_key_here

Run the Bot python app.py

Test Using Bot Framework Emulator Connect to: http://localhost:3978/api/messages

Security Note Azure keys are stored using environment variables and are not included in the code or repository.

GitHub Repository - https://github.com/rpatel36094/msai631-CampusHelp
