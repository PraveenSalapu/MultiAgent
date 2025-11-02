"""
General Health Assistant Agent
Handles general health queries and provides basic health information
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent


class GeneralHealthAssistant(BaseHealthcareAgent):
    """
    Agent for general health queries and guidance
    """

    def __init__(self):
        super().__init__(
            agent_name="General Health Assistant",
            capabilities=["general_health", "health_education", "symptom_assessment"]
        )
        self.health_topics = self._load_health_topics()

    def _load_health_topics(self) -> Dict[str, Any]:
        """Load general health information database"""
        return {
            'exercise': {
                'guidelines': [
                    'Adults: 150 minutes moderate-intensity aerobic activity per week',
                    'Or 75 minutes vigorous-intensity aerobic activity per week',
                    'Muscle-strengthening activities 2+ days per week',
                    'Include flexibility and balance exercises'
                ],
                'benefits': [
                    'Reduces risk of chronic diseases',
                    'Improves mental health and mood',
                    'Helps maintain healthy weight',
                    'Strengthens bones and muscles',
                    'Improves sleep quality'
                ]
            },
            'sleep': {
                'recommendations': [
                    'Adults: 7-9 hours per night',
                    'Maintain consistent sleep schedule',
                    'Create relaxing bedtime routine',
                    'Keep bedroom cool, dark, and quiet',
                    'Avoid screens 1 hour before bed',
                    'Limit caffeine after 2 PM'
                ],
                'importance': [
                    'Supports immune function',
                    'Aids memory and learning',
                    'Regulates mood and emotions',
                    'Helps maintain healthy weight',
                    'Reduces disease risk'
                ]
            },
            'hydration': {
                'guidelines': [
                    'Men: ~15.5 cups (3.7 liters) of fluids daily',
                    'Women: ~11.5 cups (2.7 liters) of fluids daily',
                    'Increase with exercise and hot weather',
                    'Monitor urine color (pale yellow is ideal)'
                ],
                'tips': [
                    'Drink water throughout the day',
                    'Eat water-rich fruits and vegetables',
                    'Carry a reusable water bottle',
                    'Set hydration reminders'
                ]
            },
            'stress_management': {
                'techniques': [
                    'Deep breathing exercises',
                    'Regular physical activity',
                    'Meditation and mindfulness',
                    'Adequate sleep',
                    'Social connections',
                    'Time management',
                    'Hobbies and relaxation activities'
                ],
                'warning_signs': [
                    'Persistent anxiety or worry',
                    'Sleep disturbances',
                    'Changes in appetite',
                    'Difficulty concentrating',
                    'Physical symptoms (headaches, tension)',
                    'Irritability or mood changes'
                ]
            },
            'preventive_care': {
                'annual_checkup': [
                    'Blood pressure screening',
                    'Cholesterol check (every 4-6 years)',
                    'Diabetes screening (if risk factors present)',
                    'BMI and weight assessment',
                    'Cancer screenings (age-appropriate)',
                    'Immunization updates',
                    'Vision and dental exams'
                ],
                'lifestyle_factors': [
                    'Don\'t smoke or use tobacco',
                    'Limit alcohol consumption',
                    'Maintain healthy weight',
                    'Eat balanced diet',
                    'Regular physical activity',
                    'Manage stress',
                    'Practice good hygiene'
                ]
            }
        }

    def get_health_topic_info(self, topic: str) -> Dict[str, Any]:
        """Get information about a health topic"""
        topic_lower = topic.lower()

        for key, info in self.health_topics.items():
            if key in topic_lower or topic_lower in key:
                return {'topic': key, 'information': info}

        return None

    def assess_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """Provide basic symptom assessment (educational only, not diagnostic)"""
        # This is a simplified example - real system would be more sophisticated
        symptom_keywords = {
            'emergency': ['chest pain', 'difficulty breathing', 'severe bleeding', 'loss of consciousness',
                         'severe headache', 'sudden weakness', 'stroke symptoms'],
            'urgent': ['high fever', 'persistent vomiting', 'severe pain', 'signs of infection',
                      'unusual bleeding', 'severe allergic reaction'],
            'routine': ['mild headache', 'minor cold', 'slight cough', 'minor ache']
        }

        severity = 'routine'
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            if any(emergency in symptom_lower for emergency in symptom_keywords['emergency']):
                severity = 'emergency'
                break
            elif any(urgent in symptom_lower for urgent in symptom_keywords['urgent']):
                severity = 'urgent'

        recommendations = {
            'emergency': {
                'action': 'SEEK IMMEDIATE EMERGENCY CARE',
                'details': 'Call 911 or go to the nearest emergency room',
                'urgency': 'IMMEDIATE'
            },
            'urgent': {
                'action': 'Contact healthcare provider soon',
                'details': 'Schedule appointment within 24-48 hours or visit urgent care',
                'urgency': 'WITHIN 24-48 HOURS'
            },
            'routine': {
                'action': 'Monitor symptoms and practice self-care',
                'details': 'Schedule routine appointment if symptoms persist or worsen',
                'urgency': 'AS NEEDED'
            }
        }

        return {
            'severity': severity,
            'recommendation': recommendations[severity],
            'disclaimer': 'This is not a medical diagnosis. Consult healthcare professional for proper evaluation.'
        }

    def get_wellness_tips(self, focus_area: str = 'general') -> List[str]:
        """Get wellness tips for specific focus area"""
        wellness_tips = {
            'general': [
                'Stay physically active most days of the week',
                'Eat a balanced diet rich in fruits and vegetables',
                'Get adequate sleep (7-9 hours for adults)',
                'Stay hydrated throughout the day',
                'Manage stress through healthy coping mechanisms',
                'Maintain social connections',
                'Practice good hygiene',
                'Schedule regular health checkups',
                'Limit alcohol and avoid tobacco',
                'Protect yourself from excessive sun exposure'
            ],
            'mental_health': [
                'Practice mindfulness and meditation',
                'Stay connected with friends and family',
                'Engage in activities you enjoy',
                'Seek help when needed - therapy is beneficial',
                'Maintain work-life balance',
                'Limit social media use',
                'Practice gratitude',
                'Set realistic goals'
            ],
            'nutrition': [
                'Follow the plate method: 1/2 vegetables, 1/4 protein, 1/4 whole grains',
                'Eat a variety of colorful fruits and vegetables',
                'Choose whole grains over refined grains',
                'Include lean proteins',
                'Limit added sugars and sodium',
                'Read nutrition labels',
                'Practice portion control',
                'Plan and prepare meals in advance'
            ]
        }

        return wellness_tips.get(focus_area, wellness_tips['general'])

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process general health query"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Check for health topic queries
        topic_info = None
        for topic in self.health_topics.keys():
            if topic in user_lower:
                topic_info = self.get_health_topic_info(topic)
                break

        # Check for wellness tips request
        wellness_focus = 'general'
        if 'mental' in user_lower or 'mood' in user_lower:
            wellness_focus = 'mental_health'
        elif 'nutrition' in user_lower or 'food' in user_lower or 'diet' in user_lower:
            wellness_focus = 'nutrition'

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'message': 'General health information and guidance',
            'wellness_tips': self.get_wellness_tips(wellness_focus),
            'next_steps': [
                'Consult healthcare provider for personalized advice',
                'Schedule regular checkups',
                'Maintain healthy lifestyle habits',
                'Seek specialist care for specific concerns'
            ]
        }

        if topic_info:
            response['topic_information'] = topic_info
            response['message'] = f"Information about {topic_info['topic']}"

        # Check if user is describing symptoms
        if any(word in user_lower for word in ['symptom', 'feel', 'pain', 'ache', 'sick', 'hurt']):
            # Extract potential symptoms from input
            symptoms = [user_input]  # Simplified - would need better extraction
            assessment = self.assess_symptoms(symptoms)
            response['symptom_assessment'] = assessment
            if assessment['severity'] == 'emergency':
                response['urgent'] = True

        self.log_interaction(user_input, response)

        return response
