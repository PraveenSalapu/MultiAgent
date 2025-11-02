"""
Diabetes Prediction Agent
Analyzes health features and predicts diabetes risk
"""

from typing import Dict, Any
from .base_agent import BaseHealthcareAgent
import json


class DiabetesPredictionAgent(BaseHealthcareAgent):
    """
    Agent specialized in predicting diabetes risk based on health features
    """

    def __init__(self):
        super().__init__(
            agent_name="Diabetes Prediction Agent",
            capabilities=["diabetes_prediction", "risk_assessment", "health_analysis"]
        )
        self.required_features = [
            'age', 'bmi', 'blood_glucose', 'blood_pressure',
            'family_history', 'physical_activity'
        ]

    def extract_health_features(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract health features from user input and context"""
        features = {}

        # Try to extract from context first
        if 'health_data' in context:
            features.update(context['health_data'])

        # Parse from user input (simple extraction)
        user_lower = user_input.lower()

        # Age extraction
        if 'age' not in features:
            import re
            age_match = re.search(r'age[:\s]+(\d+)|(\d+)\s*years?\s*old', user_lower)
            if age_match:
                features['age'] = int(age_match.group(1) or age_match.group(2))

        # BMI extraction
        if 'bmi' not in features:
            bmi_match = re.search(r'bmi[:\s]+(\d+\.?\d*)', user_lower)
            if bmi_match:
                features['bmi'] = float(bmi_match.group(1))

        # Blood glucose extraction
        if 'blood_glucose' not in features:
            glucose_match = re.search(r'glucose[:\s]+(\d+\.?\d*)|blood sugar[:\s]+(\d+\.?\d*)', user_lower)
            if glucose_match:
                features['blood_glucose'] = float(glucose_match.group(1) or glucose_match.group(2))

        return features

    def predict_diabetes_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate diabetes risk prediction based on health features
        In a real system, this would use a trained ML model
        """
        risk_score = 0
        risk_factors = []

        # Age factor
        age = features.get('age', 0)
        if age > 45:
            risk_score += 20
            risk_factors.append("Age over 45")
        elif age > 35:
            risk_score += 10

        # BMI factor
        bmi = features.get('bmi', 0)
        if bmi >= 30:
            risk_score += 25
            risk_factors.append("BMI indicates obesity (≥30)")
        elif bmi >= 25:
            risk_score += 15
            risk_factors.append("BMI indicates overweight (25-29.9)")

        # Blood glucose factor
        blood_glucose = features.get('blood_glucose', 0)
        if blood_glucose >= 126:
            risk_score += 40
            risk_factors.append("Fasting blood glucose ≥126 mg/dL (diabetic range)")
        elif blood_glucose >= 100:
            risk_score += 20
            risk_factors.append("Fasting blood glucose 100-125 mg/dL (prediabetic range)")

        # Blood pressure factor
        bp = features.get('blood_pressure', '')
        if bp:
            if isinstance(bp, str) and '/' in bp:
                systolic = int(bp.split('/')[0])
                if systolic >= 140:
                    risk_score += 15
                    risk_factors.append("High blood pressure")

        # Family history factor
        if features.get('family_history', False) or features.get('family_history') == 'yes':
            risk_score += 20
            risk_factors.append("Family history of diabetes")

        # Physical activity factor
        activity = features.get('physical_activity', 'moderate')
        if activity in ['low', 'sedentary', 'none']:
            risk_score += 15
            risk_factors.append("Low physical activity")

        # Determine risk level
        if risk_score >= 70:
            risk_level = "HIGH"
            recommendation = "Immediate consultation with healthcare provider recommended"
        elif risk_score >= 40:
            risk_level = "MODERATE"
            recommendation = "Schedule appointment for diabetes screening"
        else:
            risk_level = "LOW"
            recommendation = "Maintain healthy lifestyle, regular checkups"

        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'recommendation': recommendation,
            'confidence': min(100, len(risk_factors) * 20)  # Confidence based on data completeness
        }

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process diabetes prediction request"""
        if context is None:
            context = {}

        # Extract health features
        features = self.extract_health_features(user_input, context)

        # Check if we have enough data
        missing_features = [f for f in self.required_features if f not in features or features[f] == 0]

        if len(missing_features) > 3:
            return {
                'status': 'incomplete_data',
                'message': 'Insufficient health data for accurate prediction',
                'required_features': self.required_features,
                'missing_features': missing_features,
                'provided_features': features,
                'suggestion': 'Please provide: age, BMI, blood glucose level, blood pressure, family history, and physical activity level'
            }

        # Perform prediction
        prediction = self.predict_diabetes_risk(features)

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'prediction': prediction,
            'analyzed_features': features,
            'message': f"Diabetes Risk Assessment: {prediction['risk_level']}",
            'next_steps': [
                prediction['recommendation'],
                "Consider scheduling appointment if risk is moderate or high",
                "Consult with dietician for meal planning"
            ]
        }

        # If high risk, automatically suggest routing to diabetes care specialist
        if prediction['risk_level'] in ['HIGH', 'MODERATE']:
            response['suggested_agent'] = 'Diabetes Care Specialist'
            response['urgent'] = prediction['risk_level'] == 'HIGH'

        self.log_interaction(user_input, response)

        return response

    def format_report(self, prediction_result: Dict[str, Any]) -> str:
        """Format prediction result as a readable report"""
        pred = prediction_result['prediction']

        report = f"""
╔══════════════════════════════════════════════════════════╗
║         DIABETES RISK ASSESSMENT REPORT                  ║
╚══════════════════════════════════════════════════════════╝

Risk Level: {pred['risk_level']}
Risk Score: {pred['risk_score']}/100
Confidence: {pred['confidence']}%

Risk Factors Identified:
"""
        for i, factor in enumerate(pred['risk_factors'], 1):
            report += f"  {i}. {factor}\n"

        report += f"\nRecommendation:\n  {pred['recommendation']}\n"

        return report
