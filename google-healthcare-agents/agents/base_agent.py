"""
Base Agent Class for Healthcare Multi-Agent System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
from datetime import datetime


class BaseHealthcareAgent(ABC):
    """Base class for all healthcare agents"""

    def __init__(self, agent_name: str, capabilities: List[str]):
        self.agent_name = agent_name
        self.capabilities = capabilities
        self.conversation_history = []

    @abstractmethod
    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user request and return response"""
        pass

    def log_interaction(self, user_input: str, response: Dict[str, Any]):
        """Log agent interactions"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'agent': self.agent_name
        })

    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        return self.capabilities

    def can_handle(self, intent: str) -> bool:
        """Check if agent can handle the given intent"""
        return intent.lower() in [cap.lower() for cap in self.capabilities]
