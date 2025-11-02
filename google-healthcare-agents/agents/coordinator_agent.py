"""
Main Healthcare Coordinator Agent
Routes requests to appropriate specialized agents
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent
import re


class HealthcareCoordinator(BaseHealthcareAgent):
    """
    Main coordinator that manages and routes requests to specialized healthcare agents
    """

    def __init__(self):
        super().__init__(
            agent_name="Healthcare Coordinator",
            capabilities=["routing", "orchestration", "general_inquiry"]
        )
        self.registered_agents = {}

    def register_agent(self, agent: BaseHealthcareAgent):
        """Register a specialized agent with the coordinator"""
        self.registered_agents[agent.agent_name] = agent
        print(f"✓ Registered agent: {agent.agent_name}")

    def identify_intent(self, user_input: str) -> str:
        """Identify user intent from input"""
        user_input_lower = user_input.lower()

        # Intent patterns
        intent_patterns = {
            'diabetes_prediction': ['diabetes', 'blood sugar', 'glucose', 'a1c', 'predict diabetes', 'diabetes risk'],
            'appointment': ['appointment', 'schedule', 'book', 'doctor visit', 'consultation'],
            'find_provider': ['find doctor', 'find hospital', 'nearby clinic', 'healthcare provider', 'medical center', 'nearest'],
            'diet': ['diet', 'nutrition', 'meal plan', 'food', 'eat', 'dietician', 'nutritionist'],
            'diabetes_care': ['manage diabetes', 'diabetes care', 'insulin', 'diabetic', 'diabetes treatment'],
            'general_health': ['symptoms', 'health', 'feel', 'medication', 'advice']
        }

        # Check each pattern
        for intent, patterns in intent_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return intent

        return 'general_health'

    def route_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route request to appropriate agent"""
        intent = self.identify_intent(user_input)

        # Agent mapping
        agent_mapping = {
            'diabetes_prediction': 'Diabetes Prediction Agent',
            'appointment': 'Appointment Scheduler',
            'find_provider': 'Healthcare Provider Locator',
            'diet': 'Dietician Agent',
            'diabetes_care': 'Diabetes Care Specialist',
            'general_health': 'General Health Assistant'
        }

        target_agent_name = agent_mapping.get(intent, 'General Health Assistant')

        if target_agent_name in self.registered_agents:
            agent = self.registered_agents[target_agent_name]
            response = agent.process_request(user_input, context)
            response['routed_to'] = target_agent_name
            response['intent'] = intent
            return response
        else:
            return {
                'status': 'error',
                'message': f'Agent {target_agent_name} not available',
                'intent': intent
            }

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process incoming healthcare request"""
        if context is None:
            context = {}

        response = self.route_request(user_input, context)
        self.log_interaction(user_input, response)

        return response

    def list_available_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.registered_agents.keys())
