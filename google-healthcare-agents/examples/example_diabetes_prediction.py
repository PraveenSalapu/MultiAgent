"""
Example: Diabetes Prediction with Health Features
Demonstrates how to use the diabetes prediction agent with health data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.diabetes_prediction_agent import DiabetesPredictionAgent


def main():
    """Demonstrate diabetes prediction"""
    print("\n" + "=" * 60)
    print("DIABETES PREDICTION EXAMPLE")
    print("=" * 60 + "\n")

    # Create diabetes prediction agent
    agent = DiabetesPredictionAgent()

    # Example 1: High Risk Patient
    print("Example 1: High Risk Patient")
    print("-" * 60)

    context1 = {
        'health_data': {
            'age': 55,
            'bmi': 32.0,
            'blood_glucose': 140,
            'blood_pressure': '145/92',
            'family_history': True,
            'physical_activity': 'sedentary'
        }
    }

    response1 = agent.process_request(
        "Predict my diabetes risk with these health features",
        context1
    )

    print(agent.format_report(response1))

    # Example 2: Moderate Risk Patient
    print("\n" + "=" * 60)
    print("Example 2: Moderate Risk Patient")
    print("-" * 60)

    context2 = {
        'health_data': {
            'age': 42,
            'bmi': 27.5,
            'blood_glucose': 110,
            'blood_pressure': '132/84',
            'family_history': True,
            'physical_activity': 'low'
        }
    }

    response2 = agent.process_request(
        "What's my diabetes risk?",
        context2
    )

    print(agent.format_report(response2))

    # Example 3: Low Risk Patient
    print("\n" + "=" * 60)
    print("Example 3: Low Risk Patient")
    print("-" * 60)

    context3 = {
        'health_data': {
            'age': 35,
            'bmi': 23.0,
            'blood_glucose': 88,
            'blood_pressure': '118/76',
            'family_history': False,
            'physical_activity': 'moderate'
        }
    }

    response3 = agent.process_request(
        "Check my diabetes risk",
        context3
    )

    print(agent.format_report(response3))


if __name__ == "__main__":
    main()
