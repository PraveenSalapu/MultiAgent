"""
Helper utilities for Healthcare Multi-Agent System
"""

import json
from datetime import datetime
from typing import Dict, Any, List


def load_patient_data(patient_id: str = None, file_path: str = None) -> Dict[str, Any]:
    """Load patient data from JSON file"""
    if file_path is None:
        file_path = 'data/sample_patient_data.json'

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        if patient_id:
            for patient in data['patients']:
                if patient['patient_id'] == patient_id:
                    return patient
            return None
        else:
            return data
    except FileNotFoundError:
        return None


def save_interaction_log(log_entry: Dict[str, Any], log_file: str = 'logs/interaction_log.json'):
    """Save interaction log to file"""
    try:
        # Try to load existing logs
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []

        # Add new log entry
        log_entry['timestamp'] = datetime.now().isoformat()
        logs.append(log_entry)

        # Save back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        return True
    except Exception as e:
        print(f"Error saving log: {e}")
        return False


def format_response(response: Dict[str, Any], format_type: str = 'pretty') -> str:
    """Format response for display"""
    if format_type == 'json':
        return json.dumps(response, indent=2)
    elif format_type == 'pretty':
        output = "\n" + "=" * 60 + "\n"
        output += f"Agent: {response.get('agent', 'System')}\n"
        output += f"Status: {response.get('status', 'unknown').upper()}\n"
        output += "=" * 60 + "\n"
        output += f"\n{response.get('message', '')}\n"

        if response.get('urgent'):
            output += "\n⚠️  URGENT ACTION REQUIRED ⚠️\n"

        return output
    else:
        return str(response)


def validate_health_data(health_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate health data completeness and ranges"""
    validation_results = {
        'valid': True,
        'warnings': [],
        'errors': []
    }

    # Check required fields
    required_fields = ['age', 'bmi', 'blood_glucose']
    for field in required_fields:
        if field not in health_data or health_data[field] is None:
            validation_results['errors'].append(f"Missing required field: {field}")
            validation_results['valid'] = False

    # Validate ranges
    if 'age' in health_data:
        age = health_data['age']
        if age < 0 or age > 120:
            validation_results['errors'].append(f"Age out of valid range: {age}")
            validation_results['valid'] = False

    if 'bmi' in health_data:
        bmi = health_data['bmi']
        if bmi < 10 or bmi > 60:
            validation_results['warnings'].append(f"BMI seems unusual: {bmi}")
        elif bmi >= 30:
            validation_results['warnings'].append("BMI indicates obesity")

    if 'blood_glucose' in health_data:
        glucose = health_data['blood_glucose']
        if glucose < 40 or glucose > 400:
            validation_results['warnings'].append(f"Blood glucose seems unusual: {glucose}")
        elif glucose >= 126:
            validation_results['warnings'].append("Blood glucose in diabetic range")

    return validation_results


def calculate_health_score(health_data: Dict[str, Any]) -> int:
    """Calculate overall health score (0-100)"""
    score = 100

    # BMI factor
    bmi = health_data.get('bmi', 25)
    if bmi >= 30:
        score -= 20
    elif bmi >= 25:
        score -= 10

    # Blood glucose factor
    glucose = health_data.get('blood_glucose', 90)
    if glucose >= 126:
        score -= 25
    elif glucose >= 100:
        score -= 15

    # Blood pressure factor (simplified)
    bp = health_data.get('blood_pressure', '120/80')
    if isinstance(bp, str) and '/' in bp:
        systolic = int(bp.split('/')[0])
        if systolic >= 140:
            score -= 15
        elif systolic >= 130:
            score -= 10

    # Age factor
    age = health_data.get('age', 40)
    if age > 60:
        score -= 5

    # Physical activity factor
    activity = health_data.get('physical_activity', 'moderate')
    if activity in ['sedentary', 'low', 'none']:
        score -= 10

    # Family history factor
    if health_data.get('family_history', False):
        score -= 5

    return max(0, min(100, score))  # Ensure score is between 0-100


def create_summary_report(patient_data: Dict[str, Any], interactions: List[Dict[str, Any]]) -> str:
    """Create a comprehensive summary report"""
    report = f"""
╔══════════════════════════════════════════════════════════╗
║         HEALTHCARE SUMMARY REPORT                        ║
╚══════════════════════════════════════════════════════════╝

Patient: {patient_data.get('name', 'Unknown')}
Patient ID: {patient_data.get('patient_id', 'N/A')}
Age: {patient_data.get('age', 'N/A')}

HEALTH METRICS:
"""

    health_data = patient_data.get('health_data', {})
    health_score = calculate_health_score(health_data)

    report += f"  Overall Health Score: {health_score}/100\n"
    report += f"  BMI: {health_data.get('bmi', 'N/A')}\n"
    report += f"  Blood Glucose: {health_data.get('blood_glucose', 'N/A')} mg/dL\n"
    report += f"  Blood Pressure: {health_data.get('blood_pressure', 'N/A')}\n"
    report += f"  Physical Activity: {health_data.get('physical_activity', 'N/A')}\n"

    report += f"\nTOTAL INTERACTIONS: {len(interactions)}\n"

    report += "\nRECENT ACTIVITY:\n"
    for interaction in interactions[-5:]:  # Last 5 interactions
        agent = interaction.get('agent', 'Unknown')
        timestamp = interaction.get('timestamp', 'N/A')
        report += f"  • {agent} - {timestamp}\n"

    return report
