# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):

    def __init__(self, text_analytics_client=None):
        # Azure Text Analytics client (Sentiment)
        self.text_analytics_client = text_analytics_client

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip()
        user_input = text.lower()

        # 1) Malformed / empty input
        if user_input == "":
            return await turn_context.send_activity(
                MessageFactory.text("I didn’t receive any text. Try typing 'menu'.")
            )

        # NEW: Sentiment command (Azure AI Service)
        # Usage: sentiment I love this bot
        if user_input.startswith("sentiment "):
            to_analyze = text[len("sentiment "):].strip()

            if not to_analyze:
                return await turn_context.send_activity(
                    MessageFactory.text("Please provide text. Example: sentiment I love this bot")
                )

            if not self.text_analytics_client:
                return await turn_context.send_activity(
                    MessageFactory.text(
                        "Sentiment service is not configured. Make sure your Azure endpoint/key environment variables are set."
                    )
                )

            try:
                result = self.text_analytics_client.analyze_sentiment(documents=[to_analyze])[0]
                sentiment = result.sentiment
                return await turn_context.send_activity(
                    MessageFactory.text(f"Sentiment analysis result: {sentiment}")
                )
            except Exception:
                return await turn_context.send_activity(
                    MessageFactory.text("Sentiment service error (check endpoint/key).")
                )

        # 2) Greeting
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return await turn_context.send_activity(
                MessageFactory.text(
                    "Hello! I’m the Campus Assistant Bot 🤖. Type 'menu' to see what I can do."
                )
            )

        # 3) Capabilities menu
        if "menu" in user_input or "help" in user_input:
            menu_text = (
                "Here’s what I can do:\n"
                "1) Type 'office' for office hours\n"
                "2) Type 'course' for course info\n"
                "3) Type 'contact' for support contact\n"
                "4) Type 'reverse <text>' to reverse text\n"
                "5) Type 'sentiment <text>' for sentiment analysis (Azure)\n"
                "6) Type 'bye' to exit"
            )
            return await turn_context.send_activity(MessageFactory.text(menu_text))

        # 4) Reverse command
        if user_input.startswith("reverse "):
            to_reverse = text[8:]
            return await turn_context.send_activity(
                MessageFactory.text(to_reverse[::-1])
            )

        # 5) Information responses
        if "office" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text("Office hours are Monday–Friday, 9 AM–5 PM.")
            )

        if "course" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text(
                    "Course info: This class covers AI fundamentals, NLP basics, and chatbot development."
                )
            )

        if "contact" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text("Support contact: support@university.edu")
            )

        # 6) Exit
        if "bye" in user_input or "exit" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text("Goodbye! Thanks for chatting.")
            )

        # 7) Fallback
        return await turn_context.send_activity(
            MessageFactory.text("Sorry, I don’t understand. Type 'menu' to see options.")
        )
