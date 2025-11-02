"""
Configuration file for Healthcare Multi-Agent System
"""

# System Configuration
SYSTEM_NAME = "Healthcare Multi-Agent Assistant"
VERSION = "1.0.0"

# Agent Configuration
ENABLE_ALL_AGENTS = True
AGENT_TIMEOUT = 30  # seconds

# Diabetes Prediction Thresholds
DIABETES_THRESHOLDS = {
    'blood_glucose': {
        'normal': (0, 100),
        'prediabetes': (100, 126),
        'diabetes': (126, float('inf'))
    },
    'bmi': {
        'normal': (0, 25),
        'overweight': (25, 30),
        'obese': (30, float('inf'))
    }
}

# Risk Scoring Weights
RISK_WEIGHTS = {
    'age': 0.2,
    'bmi': 0.25,
    'blood_glucose': 0.4,
    'blood_pressure': 0.15,
    'family_history': 0.2,
    'physical_activity': 0.15
}

# Provider Search Configuration
DEFAULT_SEARCH_RADIUS = 10.0  # miles
MAX_RESULTS = 10

# Appointment Configuration
APPOINTMENT_BOOKING_WINDOW = 90  # days ahead
APPOINTMENT_SLOT_DURATION = 30  # minutes

# Logging Configuration
ENABLE_LOGGING = True
LOG_INTERACTIONS = True
LOG_FILE = "healthcare_agent_logs.json"

# API Configuration (for future integrations)
GOOGLE_MAPS_API_KEY = None  # Set when available
HEALTHCARE_API_KEY = None  # Set when available

# Feature Flags
FEATURES = {
    'diabetes_prediction': True,
    'appointment_scheduling': True,
    'provider_location': True,
    'diet_planning': True,
    'diabetes_care': True,
    'general_health': True
}
