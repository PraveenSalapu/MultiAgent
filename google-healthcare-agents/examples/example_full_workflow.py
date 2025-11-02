"""
Example: Complete Healthcare Workflow
Demonstrates a full patient journey through the multi-agent system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.coordinator_agent import HealthcareCoordinator
from agents.diabetes_prediction_agent import DiabetesPredictionAgent
from agents.appointment_scheduler_agent import AppointmentSchedulerAgent
from agents.provider_locator_agent import HealthcareProviderLocator
from agents.dietician_agent import DieticianAgent
from agents.diabetes_care_agent import DiabetesCareSpecialist
from agents.general_health_agent import GeneralHealthAssistant


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    """Demonstrate complete healthcare workflow"""
    print("\n" + "=" * 70)
    print("  COMPLETE HEALTHCARE WORKFLOW EXAMPLE")
    print("=" * 70)

    # Initialize coordinator and register agents
    coordinator = HealthcareCoordinator()

    print("\nInitializing agents...")
    agents = [
        DiabetesPredictionAgent(),
        AppointmentSchedulerAgent(),
        HealthcareProviderLocator(),
        DieticianAgent(),
        DiabetesCareSpecialist(),
        GeneralHealthAssistant()
    ]

    for agent in agents:
        coordinator.register_agent(agent)

    print(f"\n✓ System ready with {len(coordinator.list_available_agents())} agents\n")

    # Patient context
    patient_context = {
        'name': 'Sarah Johnson',
        'age': 48,
        'health_data': {
            'age': 48,
            'bmi': 29.0,
            'blood_glucose': 125,
            'blood_pressure': '138/88',
            'family_history': True,
            'physical_activity': 'low'
        },
        'user_location': {
            'lat': 40.7128,
            'lon': -74.0060
        }
    }

    # Step 1: Health Assessment and Diabetes Prediction
    print_section("STEP 1: Health Assessment & Diabetes Risk Prediction")

    query1 = "I'm concerned about diabetes. Can you assess my risk?"
    response1 = coordinator.process_request(query1, patient_context)

    print(f"Query: {query1}")
    print(f"Routed to: {response1['routed_to']}")
    print(f"Risk Assessment: {response1['prediction']['risk_level']}")
    print(f"Risk Score: {response1['prediction']['risk_score']}/100")
    print(f"\nRisk Factors:")
    for factor in response1['prediction']['risk_factors']:
        print(f"  • {factor}")
    print(f"\nRecommendation: {response1['prediction']['recommendation']}")

    # Update context with risk level
    patient_context['diabetes_risk'] = response1['prediction']['risk_level']

    # Step 2: Find Healthcare Providers
    print_section("STEP 2: Find Nearby Diabetes Specialists")

    query2 = "Find nearby diabetologists or diabetes care centers"
    response2 = coordinator.process_request(query2, patient_context)

    print(f"Query: {query2}")
    print(f"Routed to: {response2['routed_to']}")
    print(f"Found {len(response2['facilities'])} facilities")
    print(f"\nTop 3 Recommendations:")
    for i, facility in enumerate(response2['facilities'][:3], 1):
        print(f"\n  {i}. {facility['name']}")
        print(f"     Type: {facility['type']}")
        print(f"     Distance: {facility['distance']} miles")
        print(f"     Rating: {facility['rating']}/5.0")
        print(f"     Phone: {facility['phone']}")

    # Step 3: Schedule Appointment
    print_section("STEP 3: Schedule Appointment with Specialist")

    query3 = "Schedule an appointment with a diabetologist"
    response3 = coordinator.process_request(query3, patient_context)

    print(f"Query: {query3}")
    print(f"Routed to: {response3['routed_to']}")
    print(f"\nAvailable Appointment Slots:")
    for i, slot in enumerate(response3['available_slots'][:3], 1):
        print(f"\n  {i}. Dr. {slot['provider']}")
        print(f"     Specialization: {slot['specialization']}")
        print(f"     Date & Time: {slot['date']} at {slot['time']}")
        print(f"     Location: {slot['location']}")

    # Step 4: Get Dietary Recommendations
    print_section("STEP 4: Personalized Diet Plan")

    query4 = "I need a diet plan to help manage my diabetes risk"
    response4 = coordinator.process_request(query4, patient_context)

    print(f"Query: {query4}")
    print(f"Routed to: {response4['routed_to']}")
    print(f"\nMeal Plan: {response4['meal_plan']['name']}")
    print(f"Description: {response4['meal_plan']['description']}")
    print(f"Daily Calories: {response4['meal_plan']['daily_calories']} kcal")
    print(f"\nSample Daily Menu:")
    print(f"  🍳 Breakfast: {response4['daily_menu']['breakfast']}")
    print(f"  🥗 Lunch: {response4['daily_menu']['lunch']}")
    print(f"  🍽️  Dinner: {response4['daily_menu']['dinner']}")
    print(f"  🍎 Snacks: {', '.join(response4['daily_menu']['snacks'])}")

    print(f"\nTop Recommendations:")
    for i, rec in enumerate(response4['recommendations'][:5], 1):
        print(f"  {i}. {rec}")

    # Step 5: Diabetes Management Plan
    print_section("STEP 5: Comprehensive Diabetes Management Plan")

    query5 = "What should be my diabetes management plan?"
    response5 = coordinator.process_request(query5, patient_context)

    print(f"Query: {query5}")
    print(f"Routed to: {response5['routed_to']}")

    plan = response5['management_plan']
    print(f"\nManagement Protocol: {plan['protocol_name']}")
    print(f"\nTarget Goals:")
    for goal, target in plan['target_goals'].items():
        print(f"  • {goal}: {target}")

    print(f"\nMonitoring Plan:")
    for item in plan['monitoring_plan'][:3]:
        print(f"  • {item}")

    print(f"\nLifestyle Recommendations:")
    for item in plan['lifestyle_recommendations'][:3]:
        print(f"  • {item}")

    # Summary
    print_section("WORKFLOW SUMMARY")

    print("Patient Journey Complete!")
    print(f"\nPatient: {patient_context['name']}, Age {patient_context['age']}")
    print(f"Diabetes Risk: {patient_context['diabetes_risk']}")
    print(f"\nActions Taken:")
    print(f"  ✓ Health assessment and risk prediction")
    print(f"  ✓ Located nearby diabetes specialists")
    print(f"  ✓ Identified available appointment slots")
    print(f"  ✓ Generated personalized meal plan")
    print(f"  ✓ Created comprehensive management plan")

    print(f"\nNext Steps:")
    print(f"  1. Book appointment with selected specialist")
    print(f"  2. Begin following dietary recommendations")
    print(f"  3. Start monitoring blood glucose regularly")
    print(f"  4. Schedule follow-up assessments")

    print("\n" + "=" * 70)
    print("  End of Workflow Example")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
