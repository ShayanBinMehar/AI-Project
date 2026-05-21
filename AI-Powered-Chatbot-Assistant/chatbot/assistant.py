"""Primary chatbot orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .intent_classifier import IntentClassifier, IntentResult
from .memory import ConversationMemory
from .response_generator import ResponseGenerator


@dataclass
class ChatbotReply:
    """Response payload for UI display."""

    response: str
    intent: str
    confidence: float
    keywords: list[str]


class ChatbotAssistant:
    """Interactive conversational assistant."""

    def __init__(self, response_generator: ResponseGenerator) -> None:
        self.classifier = IntentClassifier()
        self.memory = ConversationMemory()
        self.generator = response_generator

    def process(self, message: str) -> ChatbotReply:
        intent_result: IntentResult = self.classifier.classify(message)
        confidence_boost = self.memory.feedback_weights.get(intent_result.intent, 0.0)
        adjusted_confidence = max(0.05, min(0.99, intent_result.confidence + confidence_boost))

        response = self.generator.generate(
            intent=intent_result.intent,
            message=message,
            keywords=intent_result.keywords,
            context=self.memory.get_recent_context(),
        )
        self.memory.remember_exchange(message, response)
        return ChatbotReply(
            response=response,
            intent=intent_result.intent,
            confidence=round(adjusted_confidence, 3),
            keywords=intent_result.keywords,
        )

    def submit_feedback(self, intent: str, helpful: bool) -> None:
        self.memory.apply_feedback(intent, helpful)

    def history_summary(self) -> str:
        return self.memory.get_recent_context()

