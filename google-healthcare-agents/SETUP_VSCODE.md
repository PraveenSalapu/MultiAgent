# Setup and Testing in VS Code

## 📥 Cloning to Local VS Code

### Step 1: Clone the Repository

Open your terminal (or VS Code integrated terminal) and run:

```bash
# Clone the repository
git clone <your-repository-url>

# Navigate to the project
cd MultiAgent
```

Or if you already have the repository URL:
```bash
git clone http://127.0.0.1:27289/git/PraveenSalapu/MultiAgent
cd MultiAgent
```

### Step 2: Checkout the Healthcare Branch

```bash
# Switch to the healthcare agents branch
git checkout claude/google-agent-healthcare-example-011CUjc6HpN7NXqLTdeX1Wv1
```

### Step 3: Open in VS Code

```bash
# Open VS Code in the healthcare agents directory
cd google-healthcare-agents
code .
```

Or from VS Code:
- File → Open Folder
- Navigate to `MultiAgent/google-healthcare-agents`
- Click "Select Folder"

---

## 🔧 VS Code Setup

### Recommended Extensions

Install these VS Code extensions for better experience:

1. **Python** (by Microsoft) - Essential for Python development
   - Extension ID: `ms-python.python`

2. **Pylance** (by Microsoft) - Python language server
   - Extension ID: `ms-python.vscode-pylance`

3. **Python Indent** (by Kevin Rose) - Correct Python indentation
   - Extension ID: `KevinRose.vsc-python-indent`

### Install Extensions

Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac) and search for:
- "Python"
- "Pylance"

---

## 🐍 Python Setup

### Verify Python Installation

Open VS Code terminal (`Ctrl+` ` or View → Terminal) and run:

```bash
python --version
# or
python3 --version
```

You should see Python 3.7 or higher.

### Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Your terminal should now show (venv) prefix
```

### Install Dependencies

```bash
# No dependencies required! This project uses only Python standard library
# But if you want to add optional enhancements later:
# pip install -r requirements.txt
```

---

## ✅ Testing the System

### Test 1: Quick Demo Mode

In VS Code terminal:

```bash
python main.py --demo
```

**Expected Output:** Automated demonstration showing all 5 agents in action.

**What to Look For:**
- ✓ System initializes with 6 agents
- ✓ Diabetes risk predictions
- ✓ Appointment scheduling
- ✓ Provider location results
- ✓ Meal plans generated
- ✓ Management protocols displayed

### Test 2: Interactive Mode

```bash
python main.py
```

**Try These Queries:**

```
You: load patient P002
You: What's my diabetes risk?
You: Find nearby diabetes care centers
You: Schedule an appointment with a diabetologist
You: Suggest a diet plan for diabetes
You: How do I manage diabetes?
You: quit
```

**Expected Behavior:**
- Each query routes to appropriate agent
- Responses include predictions, recommendations, next steps
- Context flows between queries

### Test 3: Run Example Scripts

#### Diabetes Prediction Example

```bash
python examples/example_diabetes_prediction.py
```

**Expected Output:**
- Example 1: High Risk Patient (Risk Score: 135/100)
- Example 2: Moderate Risk Patient (Risk Score: 80/100)
- Example 3: Low Risk Patient (Risk Score: 0/100)

#### Complete Workflow Example

```bash
python examples/example_full_workflow.py
```

**Expected Output:**
- Step 1: Health Assessment & Risk Prediction
- Step 2: Find Nearby Diabetes Specialists
- Step 3: Schedule Appointment
- Step 4: Personalized Diet Plan
- Step 5: Diabetes Management Plan
- Workflow Summary

### Test 4: Single Query Mode

```bash
python main.py "I'm 48 years old with BMI 29 and blood glucose 125. What's my diabetes risk?"
```

**Expected Output:** Immediate risk assessment with recommendations.

### Test 5: Run with Shell Script (Linux/Mac)

```bash
chmod +x run.sh
./run.sh
```

**Expected Behavior:** Interactive menu with options 1-5.

---

## 🧪 Testing Individual Agents

### Test Diabetes Prediction Agent

Create a test file `test_diabetes.py`:

```python
import sys
sys.path.insert(0, '.')

from agents.diabetes_prediction_agent import DiabetesPredictionAgent

# Create agent
agent = DiabetesPredictionAgent()

# Test case
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
response = agent.process_request("Predict my diabetes risk", context)

# Print results
print(f"Risk Level: {response['prediction']['risk_level']}")
print(f"Risk Score: {response['prediction']['risk_score']}/100")
print(f"Risk Factors: {len(response['prediction']['risk_factors'])}")

# Display full report
print(agent.format_report(response))
```

Run it:
```bash
python test_diabetes.py
```

### Test Provider Locator

Create `test_locator.py`:

```python
import sys
sys.path.insert(0, '.')

from agents.provider_locator_agent import HealthcareProviderLocator

# Create agent
locator = HealthcareProviderLocator()

# Test search
response = locator.process_request(
    "Find nearby diabetes care centers",
    context={'user_location': {'lat': 40.7128, 'lon': -74.0060}}
)

# Print results
print(f"Found {len(response['facilities'])} facilities\n")

for facility in response['facilities'][:3]:
    print(locator.format_facility_info(facility))
```

Run it:
```bash
python test_locator.py
```

### Test Appointment Scheduler

Create `test_appointments.py`:

```python
import sys
sys.path.insert(0, '.')

from agents.appointment_scheduler_agent import AppointmentSchedulerAgent

# Create agent
scheduler = AppointmentSchedulerAgent()

# Find available slots
response = scheduler.process_request(
    "Show available appointments with diabetologist",
    context={}
)

# Print results
print(f"Available Slots: {len(response['available_slots'])}\n")

for i, slot in enumerate(response['available_slots'][:5], 1):
    print(f"{i}. {slot['provider']} - {slot['specialization']}")
    print(f"   {slot['date']} at {slot['time']}")
    print(f"   Location: {slot['location']}\n")
```

Run it:
```bash
python test_appointments.py
```

---

## 🔍 Debugging in VS Code

### Set Up Python Debugger

1. Create `.vscode/launch.json` in your project:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Main (Interactive)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Main (Demo)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "args": ["--demo"],
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Diabetes Prediction Example",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/examples/example_diabetes_prediction.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Full Workflow Example",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/examples/example_full_workflow.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

2. Set breakpoints by clicking left of line numbers

3. Press `F5` or Run → Start Debugging

4. Select configuration from dropdown

### Useful Breakpoints to Try

- `coordinator_agent.py:54` - See intent recognition
- `diabetes_prediction_agent.py:119` - See risk calculation
- `coordinator_agent.py:77` - See agent routing

---

## 📊 Viewing Results in VS Code

### View Output in Terminal

All outputs display nicely in VS Code's integrated terminal with:
- Box drawing characters (╔═╗)
- Emojis (🏥 📊 💊)
- Colored text (if terminal supports it)

### View JSON Responses

Add this to any test script to see structured output:

```python
import json

# After getting response
print(json.dumps(response, indent=2))
```

Open in VS Code's JSON viewer for collapsible structure.

---

## 🧰 VS Code Tips & Tricks

### Code Navigation

- `Ctrl+Click` on class/function name to jump to definition
- `F12` - Go to definition
- `Alt+F12` - Peek definition
- `Shift+F12` - Find all references

### Quick Testing

Use VS Code's Python Interactive Window:

1. Right-click in Python file
2. Select "Run Selection/Line in Python Terminal"
3. Or use `Shift+Enter`

Example:
```python
# Select these lines and press Shift+Enter
from agents.diabetes_prediction_agent import DiabetesPredictionAgent
agent = DiabetesPredictionAgent()
print(agent.agent_name)
print(agent.capabilities)
```

### Terminal Shortcuts

- `` Ctrl+` `` - Toggle terminal
- `Ctrl+Shift+` ` - Create new terminal
- `Ctrl+Shift+5` - Split terminal

---

## 📝 Recommended VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "autopep8",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Python version 3.7+ installed
- [ ] Project opened in VS Code
- [ ] Can run `python main.py --demo` successfully
- [ ] Interactive mode works (`python main.py`)
- [ ] Example scripts execute without errors
- [ ] Can load patient data (`load patient P001`)
- [ ] All 6 agents initialize properly
- [ ] Risk prediction returns results
- [ ] Appointment slots display
- [ ] Provider search works
- [ ] Diet plans generate
- [ ] Management protocols show

---

## 🐛 Troubleshooting

### Issue: "Python not found"

**Solution:**
```bash
# On Windows, try:
py --version

# Or install Python from python.org
# Make sure to check "Add Python to PATH" during installation
```

### Issue: "No module named 'agents'"

**Solution:**
```bash
# Make sure you're in the correct directory
pwd  # Should show .../google-healthcare-agents

# If not:
cd google-healthcare-agents
```

### Issue: Import errors in VS Code but code runs

**Solution:**
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python interpreter (or venv)

### Issue: Terminal not showing output properly

**Solution:**
- Use VS Code's integrated terminal (not external)
- On Windows, use PowerShell or Command Prompt, not Git Bash
- Update VS Code to latest version

### Issue: Emojis not displaying

**Solution:**
- Install a font that supports emojis (e.g., "Cascadia Code")
- Set in VS Code: `"terminal.integrated.fontFamily": "Cascadia Code"`

---

## 🚀 Quick Start Commands Summary

```bash
# Clone and setup
git clone <repo-url>
cd MultiAgent/google-healthcare-agents
code .

# Verify Python
python --version

# Run tests
python main.py --demo                              # Demo mode
python main.py                                     # Interactive mode
python examples/example_diabetes_prediction.py    # Diabetes examples
python examples/example_full_workflow.py          # Full workflow

# Debug in VS Code
# Press F5 and select configuration
```

---

## 📚 What to Explore

1. **Start with README.md** - Overview of system
2. **Run QUICKSTART.md steps** - Get it working quickly
3. **Try main.py --demo** - See all features
4. **Read PROJECT_OVERVIEW.md** - Understand architecture
5. **Explore agent code** - See how each agent works
6. **Modify and experiment** - Try changing risk thresholds, add new agents

---

## 💡 Next Steps After Testing

1. **Experiment with different health data**
   - Modify values in `data/sample_patient_data.json`
   - Test edge cases (very high/low values)

2. **Customize the system**
   - Adjust risk thresholds in `config.py`
   - Add new meal plans in `dietician_agent.py`
   - Create new sample patients

3. **Extend functionality**
   - Add a new specialized agent
   - Integrate with actual APIs
   - Add database persistence

4. **Learn the architecture**
   - Study the coordinator pattern
   - Understand agent communication
   - Explore risk scoring algorithm

---

## 🎯 Success Criteria

You'll know everything is working when:

✅ Demo mode runs through all 5 scenarios
✅ Interactive mode responds to your queries
✅ Risk predictions show correct classifications
✅ Agents route properly based on intent
✅ Example scripts complete without errors
✅ Patient data loads successfully

**Enjoy exploring the Healthcare Multi-Agent System!**

---

**Need Help?**
- Check README.md for full documentation
- Review example scripts for usage patterns
- Read agent code for implementation details
- Experiment with different queries in interactive mode
