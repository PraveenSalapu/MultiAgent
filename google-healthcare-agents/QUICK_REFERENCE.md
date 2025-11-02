# Quick Reference Guide

## 🚀 Quick Start Commands

### Clone and Setup
```bash
git clone <your-repo-url>
cd MultiAgent/google-healthcare-agents
code .  # Open in VS Code
```

### Verify Python
```bash
python --version  # Should be 3.7+
```

### Run the System

#### Demo Mode (Recommended First Run)
```bash
python main.py --demo
```

#### Interactive Mode
```bash
python main.py
```

#### Single Query
```bash
python main.py "What's my diabetes risk with high blood sugar?"
```

#### Run Examples
```bash
python examples/example_diabetes_prediction.py
python examples/example_full_workflow.py
```

#### Shell Menu (Linux/Mac)
```bash
./run.sh
```

---

## 💬 Sample Queries for Interactive Mode

### Diabetes Risk Assessment
```
You: I'm 52 years old, BMI 32, blood glucose 145, what's my diabetes risk?
You: Predict diabetes risk with blood glucose 140
```

### Find Healthcare Providers
```
You: Find nearby diabetes care centers
You: Show me hospitals with diabetes specialists
You: Find nearest diabetologist
```

### Schedule Appointments
```
You: Schedule an appointment with a diabetologist
You: Book appointment with endocrinologist
You: Show available time slots
```

### Diet and Nutrition
```
You: Suggest a diet plan for diabetes
You: I need nutrition advice for weight loss
You: What should I eat to manage diabetes?
```

### Diabetes Management
```
You: How do I manage diabetes?
You: What are diabetes care protocols?
You: Help me understand diabetes treatment
```

### General Health
```
You: What are healthy eating tips?
You: How much exercise do I need?
You: Give me wellness advice
```

### Load Patient Data
```
You: load patient P001
You: load patient P002
```

### Exit
```
You: quit
You: exit
You: q
```

---

## 🔧 VS Code Shortcuts

### Run & Debug
- **F5** - Start debugging (select configuration from dropdown)
- **Ctrl+F5** - Run without debugging
- **Ctrl+Shift+P** → "Tasks: Run Task" → Select task

### Available Tasks
1. Run Demo Mode
2. Run Interactive Mode
3. Run Diabetes Prediction Example
4. Run Full Workflow Example

### Navigation
- **Ctrl+Click** - Jump to definition
- **F12** - Go to definition
- **Shift+F12** - Find all references
- **Ctrl+P** - Quick file open

### Terminal
- **Ctrl+`** - Toggle terminal
- **Ctrl+Shift+`** - New terminal

---

## 📁 Project Structure Quick Reference

```
google-healthcare-agents/
│
├── main.py                          # Main entry point ⭐
│
├── agents/                          # All agent implementations
│   ├── coordinator_agent.py         # Routes queries to agents
│   ├── diabetes_prediction_agent.py # Predicts diabetes risk ⭐
│   ├── appointment_scheduler_agent.py
│   ├── provider_locator_agent.py
│   ├── dietician_agent.py
│   ├── diabetes_care_agent.py
│   └── general_health_agent.py
│
├── examples/                        # Example scripts to run ⭐
│   ├── example_diabetes_prediction.py
│   └── example_full_workflow.py
│
├── data/
│   └── sample_patient_data.json    # Sample patients (P001-P004)
│
├── utils/
│   └── helpers.py                  # Utility functions
│
├── config.py                       # Configuration settings
│
└── Documentation
    ├── README.md                   # Full documentation
    ├── QUICKSTART.md              # 5-minute guide
    ├── SETUP_VSCODE.md            # VS Code setup guide ⭐
    ├── PROJECT_OVERVIEW.md        # Technical details
    └── QUICK_REFERENCE.md         # This file
```

---

## 🧪 Testing Checklist

Run these to verify everything works:

```bash
# ✅ Test 1: Demo mode
python main.py --demo

# ✅ Test 2: Diabetes prediction example
python examples/example_diabetes_prediction.py

# ✅ Test 3: Full workflow
python examples/example_full_workflow.py

# ✅ Test 4: Interactive mode
python main.py
# Then type: load patient P002
# Then type: What's my diabetes risk?
# Then type: quit
```

---

## 📊 Understanding Output

### Risk Levels
- **LOW**: Score < 40 → Continue healthy lifestyle
- **MODERATE**: Score 40-69 → Schedule diabetes screening
- **HIGH**: Score ≥ 70 → Immediate medical consultation

### Health Metrics
- **Blood Glucose**:
  - Normal: < 100 mg/dL
  - Prediabetes: 100-125 mg/dL
  - Diabetes: ≥ 126 mg/dL

- **BMI**:
  - Normal: < 25
  - Overweight: 25-29.9
  - Obese: ≥ 30

---

## 🎯 Common Tasks

### View Available Agents
In interactive mode:
```python
You: help
```

### Load Patient Data
```python
You: load patient P001  # Moderate risk patient
You: load patient P002  # High risk patient (has diabetes)
You: load patient P003  # Low risk patient
You: load patient P004  # Moderate risk patient
```

### Test Individual Agent

Create `test.py`:
```python
from agents.diabetes_prediction_agent import DiabetesPredictionAgent

agent = DiabetesPredictionAgent()
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

response = agent.process_request("Predict risk", context)
print(agent.format_report(response))
```

Run: `python test.py`

---

## 🐛 Troubleshooting Quick Fixes

### "Python not found"
```bash
# Try:
python3 --version
# Or:
py --version
```

### "No module named 'agents'"
```bash
# Make sure you're in the right directory:
pwd  # Should show .../google-healthcare-agents
```

### Import errors in VS Code
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python interpreter

### Output looks weird
- Use VS Code integrated terminal (not external)
- Update VS Code to latest version

---

## 📚 Documentation Quick Links

- **Getting Started**: QUICKSTART.md
- **VS Code Setup**: SETUP_VSCODE.md
- **Full Documentation**: README.md
- **Technical Details**: PROJECT_OVERVIEW.md
- **This Guide**: QUICK_REFERENCE.md

---

## 💡 Pro Tips

1. **Start with demo mode** to see all features
2. **Load patient data** for realistic testing
3. **Use F5 in VS Code** for debugging
4. **Try different queries** to see agent routing
5. **Read agent code** to understand implementation
6. **Modify config.py** to adjust thresholds
7. **Check examples/** for usage patterns

---

## 🎓 Key Concepts

### Agents
- **Coordinator**: Routes queries to specialized agents
- **Diabetes Prediction**: Analyzes health features → Risk score
- **Appointment Scheduler**: Books appointments with specialists
- **Provider Locator**: Finds nearby healthcare facilities
- **Dietician**: Personalized meal plans and nutrition advice
- **Diabetes Care**: Management protocols for diabetes types
- **General Health**: Wellness tips and general guidance

### Workflow
```
User Query → Coordinator (Intent Recognition)
           → Specialized Agent (Processing)
           → Response with Recommendations
           → Next Steps Suggested
```

### Context Flow
```python
context = {
    'health_data': {...},      # Patient health metrics
    'diabetes_risk': 'HIGH',   # Risk assessment result
    'user_location': {...}     # For provider search
}
```
Context flows between agents, accumulating information.

---

## 🆘 Need Help?

1. **Read SETUP_VSCODE.md** for detailed setup instructions
2. **Try demo mode** to see how it should work
3. **Check example scripts** for usage patterns
4. **Review agent code** for implementation details
5. **Experiment** with different queries

---

## ✅ Success Indicators

You're all set when:
- ✅ `python main.py --demo` runs successfully
- ✅ Risk predictions show correct classifications
- ✅ All 6 agents initialize properly
- ✅ Example scripts complete without errors
- ✅ Interactive mode responds to queries
- ✅ Patient data loads successfully

---

**Happy Testing! 🎉**

Remember: This is an educational system. Do not use for actual medical decisions.
