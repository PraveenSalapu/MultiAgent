# Healthcare Multi-Agent System

A comprehensive AI-powered healthcare assistance system featuring specialized agents for diabetes prediction, appointment scheduling, healthcare provider location, dietary recommendations, and more.

## 🌟 Overview

This multi-agent system demonstrates how multiple specialized AI agents can work together to provide comprehensive healthcare assistance. The system includes:

- **Diabetes Prediction Agent**: Analyzes health features to predict diabetes risk
- **Appointment Scheduler**: Manages healthcare appointment booking
- **Healthcare Provider Locator**: Finds nearby medical facilities and specialists
- **Dietician Agent**: Provides personalized dietary recommendations
- **Diabetes Care Specialist**: Offers specialized diabetes management guidance
- **General Health Assistant**: Handles general health queries and wellness tips

## 🏗️ Architecture

```
Healthcare Multi-Agent System
│
├── Healthcare Coordinator (Main Router)
│   ├── Intent Recognition
│   └── Agent Routing
│
├── Specialized Agents
│   ├── Diabetes Prediction Agent
│   │   ├── Health Feature Analysis
│   │   ├── Risk Scoring Algorithm
│   │   └── Prediction Model (Simulated ML)
│   │
│   ├── Appointment Scheduler
│   │   ├── Provider Database
│   │   ├── Availability Management
│   │   └── Booking System
│   │
│   ├── Healthcare Provider Locator
│   │   ├── Facility Database
│   │   ├── Distance Calculation
│   │   └── Specialization Filtering
│   │
│   ├── Dietician Agent
│   │   ├── Meal Plan Database
│   │   ├── Nutrition Recommendations
│   │   └── Personalized Diet Planning
│   │
│   ├── Diabetes Care Specialist
│   │   ├── Type Assessment
│   │   ├── Management Protocols
│   │   └── Complication Screening
│   │
│   └── General Health Assistant
│       ├── Health Topics Database
│       ├── Symptom Assessment
│       └── Wellness Guidance
│
└── Utilities
    ├── Patient Data Management
    ├── Logging & Analytics
    └── Response Formatting
```

## 📋 Features

### 1. Diabetes Risk Prediction
- **Input**: Age, BMI, blood glucose, blood pressure, family history, physical activity
- **Output**: Risk level (LOW/MODERATE/HIGH), risk score, risk factors, recommendations
- **Algorithm**: Multi-factor risk scoring based on clinical guidelines

### 2. Appointment Scheduling
- Search for appointments by specialization
- View available time slots
- Book appointments with specialists
- Cancel/manage existing appointments

### 3. Healthcare Provider Location
- Find nearby hospitals, clinics, and specialty centers
- Filter by specialization and facility type
- Distance-based search with radius control
- Detailed facility information (ratings, contact, services)

### 4. Dietary Recommendations
- Condition-specific meal plans (diabetes, weight loss, heart health)
- Personalized daily menus
- Nutritional guidance
- Foods to eat/avoid recommendations

### 5. Diabetes Care Management
- Type-specific management protocols (Type 1, Type 2, Prediabetes)
- Blood sugar level guidance
- Complication screening schedules
- Target goals and monitoring plans

### 6. General Health Guidance
- Health topic information (exercise, sleep, stress management)
- Symptom assessment (educational only)
- Wellness tips and preventive care guidance

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- No external dependencies required (uses Python standard library)

### Installation

1. Clone or download the repository:
```bash
cd google-healthcare-agents
```

2. The system is ready to use - no installation required!

### Quick Start

#### Interactive Mode
```bash
python main.py
```

This launches an interactive session where you can ask questions naturally:
```
You: Predict my diabetes risk
You: Schedule an appointment with a diabetologist
You: Find nearby diabetes care centers
You: Suggest a diet plan for diabetes
You: How do I manage diabetes?
```

#### Demo Mode
```bash
python main.py --demo
```

Run a complete demonstration showing all agent capabilities.

#### Single Query Mode
```bash
python main.py "What's my diabetes risk if I have high blood sugar?"
```

## 📖 Usage Examples

### Example 1: Complete Patient Workflow

```python
from agents.coordinator_agent import HealthcareCoordinator
from agents.diabetes_prediction_agent import DiabetesPredictionAgent
from agents.appointment_scheduler_agent import AppointmentSchedulerAgent
from agents.dietician_agent import DieticianAgent

# Initialize system
coordinator = HealthcareCoordinator()
coordinator.register_agent(DiabetesPredictionAgent())
coordinator.register_agent(AppointmentSchedulerAgent())
coordinator.register_agent(DieticianAgent())

# Patient context
patient_context = {
    'health_data': {
        'age': 48,
        'bmi': 29.0,
        'blood_glucose': 125,
        'blood_pressure': '138/88',
        'family_history': True,
        'physical_activity': 'low'
    }
}

# Step 1: Assess diabetes risk
response = coordinator.process_request(
    "What's my diabetes risk?",
    patient_context
)
print(f"Risk Level: {response['prediction']['risk_level']}")

# Step 2: Get diet recommendations
response = coordinator.process_request(
    "I need a diet plan for diabetes",
    patient_context
)
print(f"Meal Plan: {response['meal_plan']['name']}")

# Step 3: Schedule appointment
response = coordinator.process_request(
    "Schedule appointment with diabetologist",
    patient_context
)
print(f"Available slots: {len(response['available_slots'])}")
```

### Example 2: Using Individual Agents

```python
from agents.diabetes_prediction_agent import DiabetesPredictionAgent

# Create agent
agent = DiabetesPredictionAgent()

# Prepare health data
context = {
    'health_data': {
        'age': 55,
        'bmi': 32.0,
        'blood_glucose': 140,
        'blood_pressure': '145/92',
        'family_history': True,
        'physical_activity': 'sedentary'
    }
}

# Get prediction
response = agent.process_request(
    "Predict diabetes risk",
    context
)

# Display formatted report
print(agent.format_report(response))
```

### Example 3: Finding Healthcare Providers

```python
from agents.provider_locator_agent import HealthcareProviderLocator

# Create locator agent
locator = HealthcareProviderLocator()

# Search for diabetes specialists
response = locator.process_request(
    "Find nearby diabetes care centers",
    context={'user_location': {'lat': 40.7128, 'lon': -74.0060}}
)

# Display facilities
for facility in response['facilities']:
    print(f"{facility['name']} - {facility['distance']} miles")
```

## 🔬 Understanding the Diabetes Prediction Model

The diabetes prediction agent uses a rule-based scoring system that considers:

### Risk Factors and Weights:
- **Blood Glucose** (40%): Highest weight - direct indicator
  - < 100 mg/dL: Normal
  - 100-125 mg/dL: Prediabetic range (+20 points)
  - ≥ 126 mg/dL: Diabetic range (+40 points)

- **BMI** (25%): Obesity is major risk factor
  - 25-29.9: Overweight (+15 points)
  - ≥ 30: Obese (+25 points)

- **Age** (20%): Risk increases with age
  - > 45 years: +20 points
  - 35-45 years: +10 points

- **Family History** (20%): Genetic predisposition (+20 points)

- **Blood Pressure** (15%): Hypertension correlation
  - ≥ 140 systolic: +15 points

- **Physical Activity** (15%): Sedentary lifestyle (+15 points)

### Risk Classification:
- **LOW**: Score < 40 - Continue healthy lifestyle
- **MODERATE**: Score 40-69 - Schedule diabetes screening
- **HIGH**: Score ≥ 70 - Immediate medical consultation recommended

### Example Calculation:
```
Patient Profile:
- Age: 55 (>45) → +20 points
- BMI: 32 (obese) → +25 points
- Blood Glucose: 140 (diabetic) → +40 points
- BP: 145/92 (high) → +15 points
- Family History: Yes → +20 points
- Activity: Sedentary → +15 points

Total Risk Score: 135/100 = HIGH RISK
```

## 📂 Project Structure

```
google-healthcare-agents/
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py                    # Base agent class
│   ├── coordinator_agent.py             # Main coordinator
│   ├── diabetes_prediction_agent.py     # Diabetes risk prediction
│   ├── appointment_scheduler_agent.py   # Appointment management
│   ├── provider_locator_agent.py        # Healthcare provider search
│   ├── dietician_agent.py               # Dietary recommendations
│   ├── diabetes_care_agent.py           # Diabetes care specialist
│   └── general_health_agent.py          # General health assistant
│
├── data/
│   └── sample_patient_data.json         # Sample patient records
│
├── examples/
│   ├── example_diabetes_prediction.py   # Diabetes prediction examples
│   └── example_full_workflow.py         # Complete workflow demo
│
├── utils/
│   └── helpers.py                       # Utility functions
│
├── config.py                            # Configuration settings
├── main.py                              # Main entry point
└── README.md                            # This file
```

## 🎯 Use Cases

### 1. Diabetes Risk Assessment
**Scenario**: Patient wants to know their diabetes risk

**Input**:
```python
"I'm 48 years old, BMI is 29, blood sugar is 125. What's my diabetes risk?"
```

**Output**: Risk assessment with personalized recommendations

### 2. Complete Care Journey
**Scenario**: From assessment to treatment plan

**Steps**:
1. Assess diabetes risk
2. Find nearby specialists
3. Schedule appointment
4. Get diet plan
5. Receive management protocol

### 3. Preventive Care
**Scenario**: Healthy individual seeking wellness guidance

**Input**:
```python
"How can I prevent diabetes and stay healthy?"
```

**Output**: Preventive measures, lifestyle tips, screening recommendations

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Diabetes thresholds
DIABETES_THRESHOLDS = {
    'blood_glucose': {
        'normal': (0, 100),
        'prediabetes': (100, 126),
        'diabetes': (126, float('inf'))
    }
}

# Search parameters
DEFAULT_SEARCH_RADIUS = 10.0  # miles
MAX_RESULTS = 10

# Appointment settings
APPOINTMENT_BOOKING_WINDOW = 90  # days
```

## 📊 Sample Data

The system includes sample patient data in `data/sample_patient_data.json`:

```json
{
  "patient_id": "P001",
  "name": "John Doe",
  "age": 45,
  "health_data": {
    "bmi": 28.5,
    "blood_glucose": 118,
    "blood_pressure": "135/85",
    "family_history": true,
    "physical_activity": "low"
  }
}
```

Load patient data in interactive mode:
```
You: load patient P001
```

## 🧪 Running Examples

### Diabetes Prediction Example
```bash
python examples/example_diabetes_prediction.py
```

Demonstrates risk prediction for different patient profiles.

### Complete Workflow Example
```bash
python examples/example_full_workflow.py
```

Shows a complete patient journey through the system.

## 🚨 Important Disclaimers

⚠️ **Medical Disclaimer**: This system is for **educational and demonstration purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- **Not Diagnostic**: Predictions and assessments are educational simulations
- **Seek Professional Care**: Always consult qualified healthcare providers
- **Emergency Situations**: Call emergency services (911) for urgent medical needs
- **Privacy**: Do not use real patient data in this demonstration system

## 🔜 Future Enhancements

Potential improvements for production deployment:

### 1. Machine Learning Integration
- Train actual ML models on real diabetes datasets
- Use scikit-learn, TensorFlow, or PyTorch
- Implement proper cross-validation and testing

### 2. Real API Integrations
- Google Maps API for actual location services
- EHR (Electronic Health Records) integration
- Pharmacy and lab systems integration

### 3. Advanced Features
- Natural language processing for better intent recognition
- Voice interface support
- Multi-language support
- Telemedicine integration
- Wearable device data integration

### 4. Security & Privacy
- HIPAA compliance
- End-to-end encryption
- Secure authentication
- Audit logging

### 5. Clinical Validation
- Validation with medical professionals
- Clinical trial integration
- Evidence-based guideline updates

## 💡 Key Concepts Demonstrated

### Multi-Agent Architecture
- **Coordinator Pattern**: Central routing agent
- **Specialized Agents**: Domain-specific expertise
- **Loose Coupling**: Agents operate independently
- **Scalability**: Easy to add new agents

### Healthcare AI
- **Risk Prediction**: Clinical decision support
- **Personalization**: Context-aware recommendations
- **Care Coordination**: Integrated healthcare journey
- **Educational Support**: Patient empowerment

### Software Design
- **OOP Principles**: Inheritance, polymorphism
- **Separation of Concerns**: Clear responsibilities
- **Extensibility**: Plugin-like agent system
- **Maintainability**: Modular architecture

## 📝 Contributing

This is a demonstration project. To extend it:

1. **Add New Agent**: Inherit from `BaseHealthcareAgent`
2. **Implement `process_request()`**: Define agent behavior
3. **Register with Coordinator**: Add to agent registry
4. **Update Intent Mapping**: Add intent patterns

Example:
```python
from agents.base_agent import BaseHealthcareAgent

class MentalHealthAgent(BaseHealthcareAgent):
    def __init__(self):
        super().__init__(
            agent_name="Mental Health Counselor",
            capabilities=["mental_health", "stress_management"]
        )

    def process_request(self, user_input, context=None):
        # Implement mental health guidance
        return {
            'status': 'success',
            'message': 'Mental health guidance',
            'recommendations': [...]
        }
```

## 📚 References

### Clinical Guidelines
- American Diabetes Association (ADA) Standards of Care
- CDC Diabetes Prevention Program
- WHO Diabetes Diagnostic Criteria

### Technical Resources
- Multi-Agent Systems: Design Principles
- Healthcare AI Best Practices
- Clinical Decision Support Systems

## 🙏 Acknowledgments

This project demonstrates concepts from:
- Healthcare informatics
- Multi-agent system design
- Clinical decision support
- AI in healthcare

Built for educational purposes to showcase multi-agent architecture in healthcare applications.

## 📞 Support

For questions about this demonstration project:
- Review the example scripts in `examples/`
- Check the inline documentation in agent files
- Experiment with different queries in interactive mode

---

**Remember**: This is a demonstration system for learning purposes. Always consult qualified healthcare professionals for actual medical advice and care.

**Version**: 1.0.0
**Last Updated**: 2025
