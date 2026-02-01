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
                await turn_context.send_activity(
                    "Hello! I’m CampusHelp 🤖. I can help with deadlines, tutoring, or registration. Type 'menu' to see options."
                )

    def _safe_analyze_sentiment(self, text: str):
        """Returns 'positive'|'neutral'|'negative' or None if unavailable/error."""
        if not self.text_analytics_client:
            return None
        try:
            result = self.text_analytics_client.analyze_sentiment(documents=[text])[0]
            return getattr(result, "sentiment", None)
        except Exception:
            return None

    async def on_message_activity(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip()
        user_input = text.lower()

        # 1) Malformed / empty input
        if user_input == "":
            return await turn_context.send_activity(
                MessageFactory.text("I didn’t receive any text. Try typing 'menu'.")
            )

        # OPTIONAL: sentiment on every message (AI enhancement)
        sentiment = self._safe_analyze_sentiment(text)
        supportive_prefix = ""
        if sentiment == "negative":
            supportive_prefix = "I’m sorry you’re feeling frustrated. "

        # 2) Greeting
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return await turn_context.send_activity(
                MessageFactory.text(
                    "Hi! I’m CampusHelp 🤖. I can help with deadlines, tutoring, or registration. Type 'menu' to see options."
                )
            )

        # 3) Menu
        if "menu" in user_input or user_input == "help":
            menu_text = (
                "Here’s what I can do:\n"
                "1) Type 'deadlines' to get help finding assignment due dates\n"
                "2) Type 'tutoring' to find tutoring resources\n"
                "3) Type 'registration' for course registration help\n"
                "4) Tell me: 'I am struggling with calculus' (I’ll guide you)\n"
                "5) Type 'reverse <text>' to reverse text\n"
                "6) Type 'sentiment <text>' for sentiment analysis (Azure)\n"
                "7) Type 'bye' to exit"
            )
            return await turn_context.send_activity(MessageFactory.text(menu_text))

        # 4) Reverse command
        if user_input.startswith("reverse "):
            to_reverse = text[8:]
            return await turn_context.send_activity(MessageFactory.text(to_reverse[::-1]))

        # 5) Sentiment command (kept from your original)
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
                return await turn_context.send_activity(
                    MessageFactory.text(f"Sentiment analysis result: {result.sentiment}")
                )
            except Exception:
                return await turn_context.send_activity(
                    MessageFactory.text("Sentiment service error (check endpoint/key).")
                )

        # ------------------------------------------------------------
        # CAMPUSHELP SCENARIOS (your assignment design)
        # ------------------------------------------------------------

        # A) Intent recognition + disambiguation example:
        # User: "I am struggling with calculus"
        if "calculus" in user_input and any(k in user_input for k in ["struggling", "struggle", "hard", "help", "confused", "stressed"]):
            return await turn_context.send_activity(
                MessageFactory.text(
                    supportive_prefix
                    + "I can help you find tutoring sessions or study materials. Which would you like?"
                    + "\n\nType: 'tutoring' or 'study materials'."
                )
            )

        # B) Tutoring branch
        if user_input == "tutoring" or "tutoring" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text(
                    supportive_prefix
                    + "Tutoring resources:\n"
                    "- Math Tutoring Center (Mon–Fri)\n"
                    "- Peer tutoring appointments\n"
                    "- Online tutoring options\n\n"
                    "Do you prefer *online* or *in-person* tutoring?"
                )
            )

        # C) Study materials branch
        if "study materials" in user_input or ("study" in user_input and "material" in user_input) or ("resources" in user_input):
            return await turn_context.send_activity(
                MessageFactory.text(
                    supportive_prefix
                    + "Study materials options:\n"
                    "- Practice problem sets\n"
                    "- Recommended notes/videos\n"
                    "- Review topics (limits, derivatives, integrals)\n\n"
                    "Which topic do you want help with: *limits*, *derivatives*, or *integrals*?"
                )
            )

        # D) Deadlines scenario
        if "deadline" in user_input or "deadlines" in user_input or "due" in user_input or "assignment" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text(
                    "Deadlines help: Tell me the course name and assignment name, "
                    "and I’ll guide you to where to check the due date (syllabus/LMS)."
                )
            )

        # E) Registration scenario
        if "registration" in user_input or "register" in user_input or "enroll" in user_input or "add class" in user_input or "drop" in user_input:
            return await turn_context.send_activity(
                MessageFactory.text(
                    "Registration help: Are you trying to *add a class*, *drop a class*, or fix a *registration hold*?"
                )
            )

        # 6) Exit
        if "bye" in user_input or "exit" in user_input:
            return await turn_context.send_activity(MessageFactory.text("Goodbye! Thanks for chatting."))

        # 7) Fallback (matches your design)
        return await turn_context.send_activity(
            MessageFactory.text(
                "I may not have understood. Are you asking about deadlines, tutoring, or registration?"
            )
        )
