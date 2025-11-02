# Healthcare Multi-Agent System - Project Overview

## 🎯 Project Goal

Build a comprehensive multi-agent healthcare assistance system that demonstrates:
- **Diabetes prediction** using health features (BMI, blood glucose, etc.)
- **Intelligent routing** of user queries to specialized agents
- **Coordinated healthcare journey** from assessment to treatment planning
- **Real-world healthcare scenarios** (appointments, provider search, diet planning)

## 🏗️ System Architecture

### Core Components

#### 1. Healthcare Coordinator Agent (`coordinator_agent.py`)
**Purpose**: Central routing system that directs user queries to appropriate specialized agents

**Key Features**:
- Intent recognition from natural language queries
- Agent routing based on identified intent
- Context management across agent interactions
- Conversation history tracking

**Intent Patterns**:
```python
'diabetes_prediction': ['diabetes', 'blood sugar', 'glucose', 'predict diabetes']
'appointment': ['appointment', 'schedule', 'book', 'doctor visit']
'find_provider': ['find doctor', 'nearby clinic', 'healthcare provider']
'diet': ['diet', 'nutrition', 'meal plan', 'food', 'dietician']
'diabetes_care': ['manage diabetes', 'insulin', 'diabetes treatment']
'general_health': ['symptoms', 'health', 'medication', 'advice']
```

#### 2. Diabetes Prediction Agent (`diabetes_prediction_agent.py`)
**Purpose**: Analyze health features and predict diabetes risk

**Key Features**:
- Multi-factor risk scoring algorithm
- Health feature extraction from context
- Risk level classification (LOW/MODERATE/HIGH)
- Personalized recommendations based on risk

**Health Features Analyzed**:
- Age
- BMI (Body Mass Index)
- Blood glucose levels
- Blood pressure
- Family history
- Physical activity level

**Risk Scoring Algorithm**:
```
Total Risk Score = Σ(factor weights)

Factor Contributions:
- Blood glucose ≥126 mg/dL: +40 points (diabetic range)
- Blood glucose 100-125 mg/dL: +20 points (prediabetic)
- BMI ≥30: +25 points (obese)
- BMI 25-29.9: +15 points (overweight)
- Age >45: +20 points
- High blood pressure: +15 points
- Family history: +20 points
- Sedentary lifestyle: +15 points

Risk Levels:
- LOW: <40 points
- MODERATE: 40-69 points
- HIGH: ≥70 points
```

#### 3. Appointment Scheduler Agent (`appointment_scheduler_agent.py`)
**Purpose**: Manage healthcare appointment scheduling

**Key Features**:
- Provider database with specializations and availability
- Dynamic slot generation based on provider schedules
- Appointment booking and cancellation
- Specialization-based filtering

**Sample Providers**:
- Endocrinologists
- Diabetologists
- General Practitioners
- Nutritionists

**Availability Management**:
- 14-day booking window
- Configurable time slots
- Automatic conflict detection

#### 4. Healthcare Provider Locator (`provider_locator_agent.py`)
**Purpose**: Find nearby healthcare facilities and specialists

**Key Features**:
- Distance calculation using Haversine formula
- Specialization filtering
- Facility type filtering (Hospital, Clinic, Specialty Center)
- Rating and contact information

**Search Criteria**:
- User location (lat/lon coordinates)
- Specialization (diabetes care, nutrition, etc.)
- Facility type
- Maximum search radius (default: 10 miles)
- Emergency services availability

**Sample Facilities**:
- Hospitals with emergency services
- Specialty diabetes care centers
- General health clinics
- Wellness centers

#### 5. Dietician Agent (`dietician_agent.py`)
**Purpose**: Provide personalized dietary recommendations

**Key Features**:
- Condition-specific meal plans (diabetes, weight loss, heart health)
- Daily menu generation
- Macronutrient distribution
- Foods to eat/avoid recommendations
- Nutrition tips database

**Meal Plans Available**:
- **Diabetes-Friendly**: Low glycemic index, controlled carbs (45% carbs, 25% protein, 30% fat)
- **Weight Loss**: Calorie-controlled (40% carbs, 30% protein, 30% fat)
- **Heart-Healthy**: Mediterranean-style (50% carbs, 20% protein, 30% fat)
- **Balanced General**: Well-rounded nutrition (50% carbs, 25% protein, 25% fat)

**Daily Menu Components**:
- Breakfast options
- Lunch options
- Dinner options
- Healthy snacks
- Portion sizes and timing

#### 6. Diabetes Care Specialist (`diabetes_care_agent.py`)
**Purpose**: Specialized diabetes management and care protocols

**Key Features**:
- Type-specific management (Type 1, Type 2, Prediabetes)
- Blood sugar level assessment and guidance
- Complication screening schedules
- Medication guidance
- Target goals and monitoring plans

**Management Protocols**:
- **Type 1 Diabetes**: Insulin therapy, frequent monitoring, carb counting
- **Type 2 Diabetes**: Lifestyle modification, oral medications, insulin as needed
- **Prediabetes**: Weight loss, exercise, diet modification, prevention strategies

**Complication Screening**:
- Retinopathy (eye damage)
- Nephropathy (kidney damage)
- Neuropathy (nerve damage)
- Cardiovascular disease
- Foot problems

#### 7. General Health Assistant (`general_health_agent.py`)
**Purpose**: Handle general health queries and wellness guidance

**Key Features**:
- Health topic information database
- Basic symptom assessment (educational only)
- Wellness tips and recommendations
- Preventive care guidance

**Health Topics Covered**:
- Exercise and physical activity
- Sleep hygiene
- Hydration
- Stress management
- Preventive care

## 📊 Data Flow

### Complete Patient Journey Example

```
User Query: "I'm concerned about diabetes. Can you help?"
    ↓
[Healthcare Coordinator]
    ↓
Intent Recognition: "diabetes_prediction"
    ↓
[Diabetes Prediction Agent]
    ↓
Analyzes: age, BMI, blood glucose, BP, family history, activity
    ↓
Calculates Risk Score: 85/100
    ↓
Classification: HIGH RISK
    ↓
Recommendation: "Immediate consultation with healthcare provider"
    ↓
Suggests: Routing to Diabetes Care Specialist
    ↓
User: "Find nearby diabetes specialists"
    ↓
[Provider Locator Agent]
    ↓
Searches within 10 miles
    ↓
Returns: 5 nearby diabetes care centers with ratings
    ↓
User: "Schedule appointment with Dr. Rodriguez"
    ↓
[Appointment Scheduler]
    ↓
Shows available slots for next 14 days
    ↓
Books appointment
    ↓
User: "What diet should I follow?"
    ↓
[Dietician Agent]
    ↓
Generates diabetes-friendly meal plan
    ↓
Provides daily menu and nutrition tips
    ↓
User: "How do I manage diabetes?"
    ↓
[Diabetes Care Specialist]
    ↓
Provides comprehensive management protocol
    ↓
Includes: monitoring plan, medication guidance, target goals
```

## 🔑 Key Technical Concepts

### 1. Multi-Agent Architecture
- **Loose Coupling**: Agents operate independently
- **Coordinator Pattern**: Central routing with specialized handlers
- **Scalability**: Easy to add new agents
- **Maintainability**: Clear separation of concerns

### 2. Context Management
```python
context = {
    'patient_id': 'P001',
    'health_data': {...},
    'diabetes_risk': 'HIGH',
    'user_location': {...}
}
```
Context flows through agents, accumulating information.

### 3. Agent Communication
```python
# Base agent interface
class BaseHealthcareAgent(ABC):
    @abstractmethod
    def process_request(self, user_input: str, context: Dict) -> Dict:
        pass
```

All agents implement the same interface for consistency.

### 4. Response Structure
```python
{
    'status': 'success',
    'agent': 'Diabetes Prediction Agent',
    'message': 'Risk assessment complete',
    'prediction': {...},
    'next_steps': [...],
    'routed_to': 'Diabetes Prediction Agent',
    'intent': 'diabetes_prediction'
}
```

## 🎓 Educational Value

### Healthcare AI Concepts
1. **Clinical Decision Support**: Risk prediction, guideline-based recommendations
2. **Personalization**: Context-aware, patient-specific guidance
3. **Care Coordination**: Integrated journey from assessment to treatment
4. **Patient Engagement**: Educational information, empowerment

### Software Engineering Concepts
1. **Design Patterns**: Coordinator, Strategy, Factory
2. **Object-Oriented Programming**: Inheritance, polymorphism, abstraction
3. **Modular Architecture**: Independent, reusable components
4. **Separation of Concerns**: Each agent has single responsibility

### AI/ML Concepts
1. **Rule-Based Systems**: Diabetes risk scoring algorithm
2. **Intent Classification**: Natural language understanding
3. **Recommendation Systems**: Personalized suggestions
4. **Multi-Agent Systems**: Coordinated autonomous agents

## 🚀 Usage Modes

### 1. Interactive Mode
```bash
python main.py
```
Conversational interface for exploring system capabilities.

### 2. Demo Mode
```bash
python main.py --demo
```
Automated demonstration of all agent capabilities.

### 3. Single Query Mode
```bash
python main.py "What's my diabetes risk?"
```
One-off query processing.

### 4. Programmatic API
```python
from agents.coordinator_agent import HealthcareCoordinator

coordinator = HealthcareCoordinator()
# Register agents...
response = coordinator.process_request(query, context)
```

## 📈 Example Scenarios

### Scenario 1: High-Risk Patient Assessment
**Patient Profile**:
- Age: 55
- BMI: 32 (obese)
- Blood glucose: 140 mg/dL
- Family history: Yes
- Activity: Sedentary

**System Response**:
- Risk Level: HIGH
- Risk Score: 135/100
- Immediate action: Schedule with diabetologist
- Diet plan: Diabetes-friendly meal plan
- Management: Type 2 diabetes protocol

### Scenario 2: Preventive Care for Healthy Individual
**Patient Profile**:
- Age: 35
- BMI: 23 (normal)
- Blood glucose: 88 mg/dL
- No risk factors

**System Response**:
- Risk Level: LOW
- Recommendations: Continue healthy lifestyle
- Wellness tips: Exercise, nutrition, sleep
- Preventive measures: Annual checkups

### Scenario 3: Patient with Prediabetes
**Patient Profile**:
- Age: 48
- BMI: 29 (overweight)
- Blood glucose: 110 mg/dL (prediabetic)

**System Response**:
- Risk Level: MODERATE
- Action: Lifestyle modification program
- Diet plan: Weight loss meal plan
- Monitoring: A1C every 6 months

## 🔧 Customization and Extension

### Adding a New Agent

```python
# 1. Create new agent file
from agents.base_agent import BaseHealthcareAgent

class MentalHealthAgent(BaseHealthcareAgent):
    def __init__(self):
        super().__init__(
            agent_name="Mental Health Counselor",
            capabilities=["mental_health", "counseling"]
        )

    def process_request(self, user_input, context):
        # Implement logic
        return {...}

# 2. Register with coordinator
coordinator.register_agent(MentalHealthAgent())

# 3. Update intent patterns in coordinator
intent_patterns['mental_health'] = ['anxiety', 'depression', 'stress']
```

### Modifying Risk Algorithm

Edit `diabetes_prediction_agent.py`:
```python
def predict_diabetes_risk(self, features):
    # Modify scoring logic
    risk_score = custom_algorithm(features)
    return risk_score
```

### Adding New Meal Plans

Edit `dietician_agent.py`:
```python
self.meal_plans['custom_plan'] = {
    'name': 'Custom Plan',
    'meals': {...}
}
```

## 📋 File Descriptions

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `base_agent.py` | Abstract base class for all agents | `BaseHealthcareAgent` |
| `coordinator_agent.py` | Main routing coordinator | `HealthcareCoordinator` |
| `diabetes_prediction_agent.py` | Diabetes risk prediction | `DiabetesPredictionAgent` |
| `appointment_scheduler_agent.py` | Appointment management | `AppointmentSchedulerAgent` |
| `provider_locator_agent.py` | Healthcare provider search | `HealthcareProviderLocator` |
| `dietician_agent.py` | Dietary recommendations | `DieticianAgent` |
| `diabetes_care_agent.py` | Diabetes care protocols | `DiabetesCareSpecialist` |
| `general_health_agent.py` | General health guidance | `GeneralHealthAssistant` |
| `config.py` | System configuration | Thresholds, settings |
| `helpers.py` | Utility functions | Data loading, formatting |
| `main.py` | Entry point | `HealthcareAssistantSystem` |

## 🎯 Learning Objectives Achieved

1. ✅ **Multi-Agent System Design**: Coordinator pattern with specialized agents
2. ✅ **Healthcare AI Application**: Risk prediction, clinical decision support
3. ✅ **Natural Language Processing**: Intent recognition and routing
4. ✅ **Context Management**: State preservation across interactions
5. ✅ **Modular Architecture**: Extensible, maintainable design
6. ✅ **Real-World Healthcare Scenarios**: Comprehensive patient journey
7. ✅ **Software Engineering Best Practices**: OOP, design patterns, documentation

## 🌟 Unique Features

1. **Integrated Care Journey**: Complete workflow from risk assessment to treatment planning
2. **Context-Aware Routing**: Intelligent agent selection based on patient context
3. **Personalized Recommendations**: Tailored to individual health profiles
4. **Educational Focus**: Clear explanations, disclaimers, guidance
5. **No External Dependencies**: Pure Python implementation
6. **Extensible Architecture**: Easy to add new agents and capabilities

## 🚨 Important Notes

### Medical Disclaimer
This is an **educational demonstration system**. It is NOT:
- A medical device
- A diagnostic tool
- A substitute for professional medical advice
- Validated for clinical use

### Privacy Note
- Do not use real patient data
- System is for demonstration only
- No data persistence in this version

### Limitations
- Simulated ML model (rule-based, not trained)
- Sample data only
- No real API integrations
- Educational accuracy, not clinical accuracy

## 🎓 Ideal For

- Learning multi-agent system architecture
- Understanding healthcare AI concepts
- Exploring clinical decision support systems
- Demonstrating AI in healthcare applications
- Educational projects and presentations
- Prototyping healthcare AI solutions

## 📚 Further Reading

To learn more about the concepts used in this project:

**Multi-Agent Systems**:
- "Multi-Agent Systems: Algorithmic, Game-Theoretic, and Logical Foundations" by Shoham & Leyton-Brown
- "An Introduction to MultiAgent Systems" by Michael Wooldridge

**Healthcare AI**:
- "Artificial Intelligence in Medicine" by Ramesh et al.
- "Clinical Decision Support Systems: Theory and Practice" by Eta S. Berner

**Diabetes Care**:
- American Diabetes Association Standards of Care
- CDC National Diabetes Prevention Program

---

**Project Status**: Complete demonstration system for educational purposes

**Version**: 1.0.0

**Created**: 2025
