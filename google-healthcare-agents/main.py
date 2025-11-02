"""
Healthcare Multi-Agent System - Main Entry Point
A comprehensive healthcare assistance system with specialized agents
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator_agent import HealthcareCoordinator
from agents.diabetes_prediction_agent import DiabetesPredictionAgent
from agents.appointment_scheduler_agent import AppointmentSchedulerAgent
from agents.provider_locator_agent import HealthcareProviderLocator
from agents.dietician_agent import DieticianAgent
from agents.diabetes_care_agent import DiabetesCareSpecialist
from agents.general_health_agent import GeneralHealthAssistant
from utils.helpers import load_patient_data, format_response
import json


class HealthcareAssistantSystem:
    """Main Healthcare Assistant System"""

    def __init__(self):
        self.coordinator = HealthcareCoordinator()
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize and register all specialized agents"""
        print("\n🏥 Initializing Healthcare Multi-Agent System...")
        print("=" * 60)

        # Create all specialized agents
        agents = [
            DiabetesPredictionAgent(),
            AppointmentSchedulerAgent(),
            HealthcareProviderLocator(),
            DieticianAgent(),
            DiabetesCareSpecialist(),
            GeneralHealthAssistant()
        ]

        # Register agents with coordinator
        for agent in agents:
            self.coordinator.register_agent(agent)

        print("=" * 60)
        print(f"✓ System initialized with {len(agents)} specialized agents\n")

    def process_query(self, user_input: str, context: dict = None):
        """Process user query through the system"""
        if context is None:
            context = {}

        print(f"\n📝 Processing: \"{user_input}\"\n")

        # Route through coordinator
        response = self.coordinator.process_request(user_input, context)

        return response

    def display_response(self, response: dict):
        """Display formatted response"""
        print("\n" + "=" * 60)
        print(f"🤖 Agent: {response.get('routed_to', 'System')}")
        print(f"📊 Status: {response.get('status', 'unknown').upper()}")
        print("=" * 60)

        if response.get('urgent'):
            print("\n⚠️  ⚠️  ⚠️  URGENT ATTENTION REQUIRED ⚠️  ⚠️  ⚠️")
            if response.get('urgent_message'):
                print(f"   {response['urgent_message']}")
            print()

        print(f"\n💬 {response.get('message', '')}\n")

        # Display specific content based on agent type
        if 'prediction' in response:
            self._display_prediction(response['prediction'])

        if 'available_slots' in response:
            self._display_appointments(response['available_slots'])

        if 'facilities' in response:
            self._display_facilities(response['facilities'])

        if 'daily_menu' in response:
            self._display_meal_plan(response)

        if 'management_plan' in response:
            self._display_management_plan(response['management_plan'])

        if 'next_steps' in response:
            print("📋 NEXT STEPS:")
            for i, step in enumerate(response['next_steps'], 1):
                print(f"   {i}. {step}")
            print()

    def _display_prediction(self, prediction: dict):
        """Display diabetes prediction results"""
        print("🔍 DIABETES RISK ASSESSMENT:")
        print(f"   Risk Level: {prediction['risk_level']}")
        print(f"   Risk Score: {prediction['risk_score']}/100")
        print(f"   Confidence: {prediction['confidence']}%")
        print(f"\n   Risk Factors:")
        for factor in prediction['risk_factors']:
            print(f"      • {factor}")
        print(f"\n   Recommendation: {prediction['recommendation']}\n")

    def _display_appointments(self, slots: list):
        """Display available appointment slots"""
        print("📅 AVAILABLE APPOINTMENT SLOTS:")
        for i, slot in enumerate(slots[:5], 1):
            print(f"   {i}. {slot['provider']} ({slot['specialization']})")
            print(f"      📍 {slot['location']}")
            print(f"      📆 {slot['date']} at {slot['time']}")
            print()

    def _display_facilities(self, facilities: list):
        """Display healthcare facilities"""
        print("🏥 NEARBY HEALTHCARE FACILITIES:")
        for i, facility in enumerate(facilities[:5], 1):
            print(f"   {i}. {facility['name']} ({facility['type']})")
            print(f"      📍 {facility['address']} - {facility.get('distance', 'N/A')} miles")
            print(f"      ⭐ Rating: {facility['rating']}/5.0")
            print(f"      📞 {facility['phone']}")
            print()

    def _display_meal_plan(self, response: dict):
        """Display meal plan"""
        meal_plan = response['meal_plan']
        daily_menu = response['daily_menu']

        print(f"🥗 {meal_plan['name'].upper()}")
        print(f"   {meal_plan['description']}")
        print(f"   Daily Calories: {meal_plan['daily_calories']} kcal")
        print(f"\n   TODAY'S MENU:")
        print(f"      🍳 Breakfast: {daily_menu['breakfast']}")
        print(f"      🥗 Lunch: {daily_menu['lunch']}")
        print(f"      🍽️  Dinner: {daily_menu['dinner']}")
        print(f"      🍎 Snacks: {', '.join(daily_menu['snacks'])}")
        print()

    def _display_management_plan(self, plan: dict):
        """Display diabetes management plan"""
        print(f"💊 {plan['protocol_name'].upper()}")
        print(f"\n   Target Goals:")
        for goal, target in plan['target_goals'].items():
            print(f"      • {goal}: {target}")
        print()

    def run_interactive_mode(self):
        """Run interactive mode for user queries"""
        print("\n" + "=" * 60)
        print("  HEALTHCARE MULTI-AGENT ASSISTANT - INTERACTIVE MODE")
        print("=" * 60)
        print("\nType 'help' for commands, 'quit' to exit\n")

        context = {}

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using Healthcare Assistant. Stay healthy!\n")
                    break

                if user_input.lower() == 'help':
                    self._show_help()
                    continue

                if user_input.lower().startswith('load patient'):
                    # Load patient context
                    parts = user_input.split()
                    if len(parts) >= 3:
                        patient_id = parts[2]
                        patient_data = load_patient_data(patient_id)
                        if patient_data:
                            context = patient_data
                            print(f"✓ Loaded patient: {patient_data['name']}")
                        else:
                            print(f"✗ Patient {patient_id} not found")
                    continue

                # Process query
                response = self.process_query(user_input, context)
                self.display_response(response)

                # Update context with response data
                if 'prediction' in response:
                    context['diabetes_risk'] = response['prediction']['risk_level']

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    def _show_help(self):
        """Show help information"""
        print("\n" + "=" * 60)
        print("AVAILABLE COMMANDS:")
        print("=" * 60)
        print("  help                 - Show this help message")
        print("  quit/exit            - Exit the system")
        print("  load patient <ID>    - Load patient context (e.g., P001)")
        print("\nEXAMPLE QUERIES:")
        print("  • Predict my diabetes risk")
        print("  • Schedule an appointment with diabetologist")
        print("  • Find nearby diabetes care centers")
        print("  • Suggest a diet plan for diabetes")
        print("  • How do I manage diabetes?")
        print("  • What are healthy eating tips?")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    # Create system instance
    system = HealthcareAssistantSystem()

    # Check if running with arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            # Run demo mode
            run_demo(system)
        else:
            # Process single query
            query = ' '.join(sys.argv[1:])
            response = system.process_query(query)
            system.display_response(response)
    else:
        # Run interactive mode
        system.run_interactive_mode()


def run_demo(system: HealthcareAssistantSystem):
    """Run demonstration of the system"""
    print("\n" + "=" * 60)
    print("  HEALTHCARE MULTI-AGENT SYSTEM - DEMO MODE")
    print("=" * 60 + "\n")

    # Load sample patient
    patient_data = load_patient_data('P002')

    demo_queries = [
        ("Diabetes Risk Prediction", "I'm 52 years old with BMI 32, blood glucose 145, what's my diabetes risk?", patient_data),
        ("Appointment Scheduling", "Schedule an appointment with a diabetologist", patient_data),
        ("Healthcare Provider Location", "Find nearby diabetes care centers", patient_data),
        ("Diet Recommendations", "Suggest a diet plan for diabetes", patient_data),
        ("Diabetes Care Management", "How should I manage my diabetes?", patient_data),
    ]

    for i, (title, query, context) in enumerate(demo_queries, 1):
        print(f"\n{'='*60}")
        print(f"DEMO {i}: {title}")
        print(f"{'='*60}")

        response = system.process_query(query, context)
        system.display_response(response)

        if i < len(demo_queries):
            input("\nPress Enter to continue to next demo...")


if __name__ == "__main__":
    main()
