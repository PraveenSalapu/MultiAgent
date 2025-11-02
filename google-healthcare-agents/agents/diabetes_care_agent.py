"""
Diabetes Care Specialist Agent
Provides specialized care and management guidance for diabetes patients
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent


class DiabetesCareSpecialist(BaseHealthcareAgent):
    """
    Agent specialized in diabetes management and care
    """

    def __init__(self):
        super().__init__(
            agent_name="Diabetes Care Specialist",
            capabilities=["diabetes_management", "insulin_guidance", "complication_prevention"]
        )
        self.care_protocols = self._load_care_protocols()

    def _load_care_protocols(self) -> Dict[str, Any]:
        """Load diabetes care protocols"""
        return {
            'type1': {
                'name': 'Type 1 Diabetes Management',
                'monitoring': [
                    'Check blood glucose 4-10 times per day',
                    'Monitor ketones when blood sugar is high',
                    'Track carbohydrate intake carefully',
                    'Record insulin doses and timing'
                ],
                'medication': [
                    'Multiple daily insulin injections or insulin pump',
                    'Rapid-acting insulin before meals',
                    'Long-acting basal insulin once or twice daily',
                    'Adjust doses based on blood sugar readings'
                ],
                'lifestyle': [
                    'Count carbohydrates for insulin dosing',
                    'Exercise with caution and monitor glucose',
                    'Carry fast-acting sugar for hypoglycemia',
                    'Wear medical ID at all times'
                ]
            },
            'type2': {
                'name': 'Type 2 Diabetes Management',
                'monitoring': [
                    'Check blood glucose 1-3 times per day',
                    'Regular A1C testing every 3 months',
                    'Monitor blood pressure and cholesterol',
                    'Track weight and BMI'
                ],
                'medication': [
                    'Metformin as first-line medication',
                    'Additional oral medications as needed',
                    'GLP-1 agonists or SGLT2 inhibitors',
                    'Insulin if other medications insufficient'
                ],
                'lifestyle': [
                    'Follow diabetic meal plan',
                    'Regular physical activity (150 min/week)',
                    'Weight loss if overweight',
                    'Stress management'
                ]
            },
            'prediabetes': {
                'name': 'Prediabetes Management',
                'monitoring': [
                    'A1C testing every 6 months',
                    'Periodic fasting glucose checks',
                    'Monitor weight and BMI',
                    'Regular health checkups'
                ],
                'lifestyle': [
                    'Lose 5-7% of body weight if overweight',
                    'Exercise 30 minutes, 5 days per week',
                    'Follow Mediterranean or DASH diet',
                    'Limit refined carbohydrates and sugars',
                    'Increase fiber intake',
                    'Reduce stress'
                ],
                'prevention': [
                    'Regular screening for progression',
                    'Address other risk factors (BP, cholesterol)',
                    'Consider metformin if high risk',
                    'Annual comprehensive health assessment'
                ]
            }
        }

    def assess_diabetes_type(self, context: Dict[str, Any]) -> str:
        """Determine diabetes type based on context"""
        risk_level = context.get('diabetes_risk', '').upper()
        blood_glucose = context.get('health_data', {}).get('blood_glucose', 0)
        has_diabetes = context.get('has_diabetes', False)

        if has_diabetes:
            # Could add more sophisticated typing logic here
            diabetes_type = context.get('diabetes_type', 'type2')
            return diabetes_type
        elif risk_level == 'HIGH' or (100 <= blood_glucose < 126):
            return 'prediabetes'
        elif blood_glucose >= 126:
            return 'type2'  # Default assumption, would need more data for type 1
        else:
            return 'prediabetes'  # Preventive care

    def get_blood_sugar_guidance(self, blood_glucose: float) -> Dict[str, Any]:
        """Provide guidance based on blood sugar levels"""
        if blood_glucose < 70:
            return {
                'status': 'HYPOGLYCEMIA',
                'severity': 'URGENT',
                'action': 'Treat immediately with 15g fast-acting carbs',
                'examples': ['3-4 glucose tablets', '4 oz fruit juice', '1 tbsp honey'],
                'follow_up': 'Recheck in 15 minutes, repeat if still low'
            }
        elif blood_glucose < 100:
            return {
                'status': 'NORMAL',
                'severity': 'GOOD',
                'action': 'Maintain current management',
                'advice': 'Continue healthy lifestyle and monitoring'
            }
        elif blood_glucose < 126:
            return {
                'status': 'PREDIABETIC',
                'severity': 'CAUTION',
                'action': 'Lifestyle modifications recommended',
                'advice': 'Reduce carbohydrate intake, increase exercise'
            }
        elif blood_glucose < 180:
            return {
                'status': 'DIABETIC',
                'severity': 'ELEVATED',
                'action': 'Medication may be needed',
                'advice': 'Consult healthcare provider, follow diabetic meal plan'
            }
        else:
            return {
                'status': 'HYPERGLYCEMIA',
                'severity': 'HIGH',
                'action': 'Immediate medical attention recommended',
                'advice': 'Contact healthcare provider, check for ketones if type 1'
            }

    def get_complication_screening(self) -> List[Dict[str, Any]]:
        """Recommended screening for diabetes complications"""
        return [
            {
                'complication': 'Retinopathy (Eye Damage)',
                'screening': 'Dilated eye exam',
                'frequency': 'Annually',
                'specialist': 'Ophthalmologist'
            },
            {
                'complication': 'Nephropathy (Kidney Damage)',
                'screening': 'Urine albumin and kidney function tests',
                'frequency': 'Annually',
                'specialist': 'Nephrologist if abnormal'
            },
            {
                'complication': 'Neuropathy (Nerve Damage)',
                'screening': 'Foot examination, sensory testing',
                'frequency': 'Annually',
                'specialist': 'Podiatrist'
            },
            {
                'complication': 'Cardiovascular Disease',
                'screening': 'Blood pressure, lipid panel, EKG',
                'frequency': 'Every 3-6 months',
                'specialist': 'Cardiologist if indicated'
            },
            {
                'complication': 'Foot Problems',
                'screening': 'Comprehensive foot exam',
                'frequency': 'Every visit',
                'specialist': 'Podiatrist'
            }
        ]

    def get_management_plan(self, diabetes_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive diabetes management plan"""
        protocol = self.care_protocols.get(diabetes_type, self.care_protocols['type2'])

        blood_glucose = context.get('health_data', {}).get('blood_glucose', 0)
        blood_sugar_guidance = None
        if blood_glucose > 0:
            blood_sugar_guidance = self.get_blood_sugar_guidance(blood_glucose)

        plan = {
            'diabetes_type': diabetes_type,
            'protocol_name': protocol['name'],
            'monitoring_plan': protocol['monitoring'],
            'medication_guidance': protocol.get('medication', []),
            'lifestyle_recommendations': protocol.get('lifestyle', []),
            'prevention_measures': protocol.get('prevention', []),
            'complication_screening': self.get_complication_screening(),
            'blood_sugar_assessment': blood_sugar_guidance,
            'target_goals': {
                'A1C': '< 7% (individualized)',
                'Fasting Glucose': '80-130 mg/dL',
                'Post-meal Glucose': '< 180 mg/dL',
                'Blood Pressure': '< 140/90 mmHg',
                'LDL Cholesterol': '< 100 mg/dL'
            }
        }

        return plan

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process diabetes care request"""
        if context is None:
            context = {}

        # Assess diabetes type
        diabetes_type = self.assess_diabetes_type(context)

        # Generate management plan
        management_plan = self.get_management_plan(diabetes_type, context)

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'management_plan': management_plan,
            'message': f"Generated comprehensive {management_plan['protocol_name']} plan",
            'next_steps': [
                'Review management plan with your healthcare provider',
                'Schedule recommended screenings',
                'Follow dietary recommendations',
                'Maintain regular monitoring schedule',
                'Keep emergency contact information readily available'
            ]
        }

        # Add urgent flag if blood sugar is critically high or low
        if management_plan.get('blood_sugar_assessment'):
            severity = management_plan['blood_sugar_assessment'].get('severity')
            if severity in ['URGENT', 'HIGH']:
                response['urgent'] = True
                response['urgent_message'] = management_plan['blood_sugar_assessment']['action']

        self.log_interaction(user_input, response)

        return response

    def format_management_plan(self, plan: Dict[str, Any]) -> str:
        """Format management plan for display"""
        output = f"""
╔══════════════════════════════════════════════════════════╗
║         DIABETES MANAGEMENT PLAN                         ║
╚══════════════════════════════════════════════════════════╝

Type: {plan['protocol_name']}

📊 TARGET GOALS:
"""
        for goal, target in plan['target_goals'].items():
            output += f"   • {goal}: {target}\n"

        if plan.get('blood_sugar_assessment'):
            bsa = plan['blood_sugar_assessment']
            output += f"\n🩸 BLOOD SUGAR ASSESSMENT:\n"
            output += f"   Status: {bsa['status']} ({bsa['severity']})\n"
            output += f"   Action: {bsa['action']}\n"

        output += "\n📋 MONITORING PLAN:\n"
        for item in plan['monitoring_plan']:
            output += f"   • {item}\n"

        if plan.get('medication_guidance'):
            output += "\n💊 MEDICATION GUIDANCE:\n"
            for item in plan['medication_guidance']:
                output += f"   • {item}\n"

        output += "\n🏃 LIFESTYLE RECOMMENDATIONS:\n"
        for item in plan['lifestyle_recommendations']:
            output += f"   • {item}\n"

        output += "\n🔍 COMPLICATION SCREENING SCHEDULE:\n"
        for screening in plan['complication_screening'][:3]:
            output += f"   • {screening['complication']}: {screening['frequency']}\n"

        return output
