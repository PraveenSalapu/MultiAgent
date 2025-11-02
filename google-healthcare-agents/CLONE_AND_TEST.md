# Clone and Test in VS Code - Simple Guide

## 📥 Step-by-Step Instructions

### Step 1: Get the Repository URL

Your repository URL is likely one of these formats:
```
https://github.com/PraveenSalapu/MultiAgent.git
# or
git@github.com:PraveenSalapu/MultiAgent.git
```

### Step 2: Clone the Repository

Open your terminal or command prompt and run:

```bash
# Navigate to where you want the project
cd ~/Documents  # or C:\Users\YourName\Documents on Windows

# Clone the repository
git clone https://github.com/PraveenSalapu/MultiAgent.git

# Go into the project
cd MultiAgent

# Checkout the healthcare branch
git checkout claude/google-agent-healthcare-example-011CUjc6HpN7NXqLTdeX1Wv1
```

### Step 3: Open in VS Code

```bash
# Navigate to the healthcare agents directory
cd google-healthcare-agents

# Open VS Code
code .
```

**Or from VS Code:**
1. Click `File` → `Open Folder`
2. Navigate to `MultiAgent/google-healthcare-agents`
3. Click `Select Folder`

### Step 4: Select Python Interpreter (Important!)

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Python: Select Interpreter`
3. Choose your Python installation (Python 3.7 or higher)

### Step 5: Run Your First Test

**Option A: Use Debug Menu (Easiest)**
1. Press `F5` on your keyboard
2. Select `Python: Main (Demo Mode)` from dropdown
3. Watch the demo run!

**Option B: Use Terminal**
1. Press `` Ctrl+` `` to open terminal in VS Code
2. Type: `python main.py --demo`
3. Press Enter

**Option C: Use Command Palette**
1. Press `Ctrl+Shift+P`
2. Type: `Tasks: Run Task`
3. Select `Run Demo Mode`

---

## ✅ Verification - You Should See This

When you run demo mode, you should see:

```
🏥 Initializing Healthcare Multi-Agent System...
============================================================
✓ Registered agent: Diabetes Prediction Agent
✓ Registered agent: Appointment Scheduler
✓ Registered agent: Healthcare Provider Locator
✓ Registered agent: Dietician Agent
✓ Registered agent: Diabetes Care Specialist
✓ Registered agent: General Health Assistant
============================================================
✓ System initialized with 6 specialized agents

============================================================
  HEALTHCARE MULTI-AGENT SYSTEM - DEMO MODE
============================================================

============================================================
DEMO 1: Diabetes Risk Prediction
============================================================

📝 Processing: "I'm 52 years old with BMI 32, blood glucose 145, what's my diabetes risk?"

============================================================
🤖 Agent: Diabetes Prediction Agent
📊 Status: SUCCESS
============================================================

🔍 DIABETES RISK ASSESSMENT:
   Risk Level: HIGH
   Risk Score: 135/100
   Confidence: 100%

   Risk Factors:
      • Age over 45
      • BMI indicates obesity (≥30)
      • Fasting blood glucose ≥126 mg/dL (diabetic range)
      ...
```

---

## 🎯 Quick Tests to Run

### Test 1: Demo Mode (RECOMMENDED FIRST!)
```bash
python main.py --demo
```
**Expected**: See 5 complete scenarios demonstrating all agents

### Test 2: Diabetes Prediction Example
```bash
python examples/example_diabetes_prediction.py
```
**Expected**: See 3 different risk assessments (High, Moderate, Low)

### Test 3: Full Workflow
```bash
python examples/example_full_workflow.py
```
**Expected**: Complete patient journey through all agents

### Test 4: Interactive Mode
```bash
python main.py
```
**Then try these commands:**
```
You: load patient P002
You: What's my diabetes risk?
You: Find nearby diabetes care centers
You: quit
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "python not found"

**Windows:**
```bash
# Try these instead:
py main.py --demo
# or
python3 main.py --demo
```

**Mac/Linux:**
```bash
python3 main.py --demo
```

### Issue 2: VS Code says "Python extension not installed"

**Solution:**
1. Click the "Install" button in VS Code
2. Or press `Ctrl+Shift+X` and search for "Python"
3. Install the official Python extension by Microsoft

### Issue 3: "No module named 'agents'"

**Solution:**
Make sure you're in the correct directory:
```bash
pwd  # Should show: .../google-healthcare-agents

# If not:
cd google-healthcare-agents
```

### Issue 4: Code runs in terminal but VS Code shows errors

**Solution:**
1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose your Python interpreter
4. Restart VS Code if needed

---

## 🎮 VS Code Features You Can Use

### 1. Debug with Breakpoints
- Click left of line number to set breakpoint (red dot appears)
- Press `F5` to start debugging
- Code will pause at breakpoint
- Use debug toolbar to step through code

**Try setting a breakpoint at:**
- `diabetes_prediction_agent.py` line 119 (risk calculation)
- `coordinator_agent.py` line 54 (intent recognition)

### 2. Run Tasks Quickly
- Press `Ctrl+Shift+P`
- Type: `Tasks: Run Task`
- Select from menu:
  - Run Demo Mode
  - Run Interactive Mode
  - Run Diabetes Prediction Example
  - Run Full Workflow Example

### 3. Terminal Shortcuts
- `` Ctrl+` `` - Open/close terminal
- `Ctrl+Shift+` ` - New terminal
- `Ctrl+C` - Stop running program

### 4. Navigate Code
- `Ctrl+Click` on any function/class name to jump to definition
- `F12` - Go to definition
- `Alt+←` - Go back
- `Ctrl+P` - Quick open file

---

## 📚 What to Explore Next

### 1. Read the Documentation
- Start with: `README.md`
- Quick start: `QUICKSTART.md`
- This guide: `SETUP_VSCODE.md`
- Reference: `QUICK_REFERENCE.md`

### 2. Explore the Agents
Open these files to see how agents work:
- `agents/diabetes_prediction_agent.py` - Risk scoring algorithm
- `agents/coordinator_agent.py` - Routing logic
- `agents/dietician_agent.py` - Meal planning

### 3. Modify and Experiment

**Easy modifications to try:**

**Change Risk Thresholds:**
Edit `config.py`:
```python
DIABETES_THRESHOLDS = {
    'blood_glucose': {
        'normal': (0, 100),
        'prediabetes': (100, 126),  # Try changing these
        'diabetes': (126, float('inf'))
    }
}
```

**Add a New Patient:**
Edit `data/sample_patient_data.json`:
```json
{
  "patient_id": "P005",
  "name": "Your Name",
  "age": 30,
  "health_data": {
    "bmi": 22.0,
    "blood_glucose": 85,
    "blood_pressure": "115/75",
    "family_history": false,
    "physical_activity": "high"
  }
}
```

**Test Your New Patient:**
```bash
python main.py
You: load patient P005
You: What's my diabetes risk?
```

### 4. Create Your Own Test Script

Create `my_test.py`:
```python
from agents.diabetes_prediction_agent import DiabetesPredictionAgent

agent = DiabetesPredictionAgent()

# Your own health data
context = {
    'health_data': {
        'age': 35,
        'bmi': 24.0,
        'blood_glucose': 90,
        'blood_pressure': '120/80',
        'family_history': False,
        'physical_activity': 'moderate'
    }
}

response = agent.process_request("Check my risk", context)
print(agent.format_report(response))
```

Run it: `python my_test.py`

---

## 🎓 Learning Path

### Day 1: Get It Running
- ✅ Clone repository
- ✅ Open in VS Code
- ✅ Run demo mode
- ✅ Try interactive mode

### Day 2: Understand the System
- ✅ Read README.md
- ✅ Read PROJECT_OVERVIEW.md
- ✅ Run example scripts
- ✅ Explore agent code

### Day 3: Experiment
- ✅ Modify config.py settings
- ✅ Add new patient data
- ✅ Create test scripts
- ✅ Try debugging with breakpoints

### Day 4: Extend
- ✅ Add new meal plan to dietician agent
- ✅ Add new healthcare facility
- ✅ Modify risk scoring algorithm
- ✅ Create new test scenarios

---

## 🎯 Success Checklist

Mark these off as you complete them:

- [ ] Repository cloned successfully
- [ ] VS Code opens without errors
- [ ] Python interpreter selected
- [ ] Demo mode runs and shows all 5 scenarios
- [ ] Diabetes prediction example shows 3 risk levels
- [ ] Full workflow example completes
- [ ] Interactive mode responds to queries
- [ ] Can load patient data (P001-P004)
- [ ] All 6 agents initialize properly
- [ ] Can set breakpoints and debug

---

## 🚀 You're Ready When...

✅ You can run `python main.py --demo` successfully

✅ You understand how queries route to agents

✅ You can modify patient data and see different results

✅ You've debugged code with breakpoints in VS Code

✅ You've explored the agent implementations

---

## 💪 Challenge Yourself

Once comfortable, try these:

1. **Add a new agent** for a different healthcare specialty
2. **Integrate with an API** (like Google Maps for real locations)
3. **Add a database** to persist patient data
4. **Create a web interface** using Flask or FastAPI
5. **Train a real ML model** for diabetes prediction
6. **Add unit tests** with pytest
7. **Create visualization** of risk factors

---

## 📞 Next Steps

1. **Start**: Run demo mode
2. **Explore**: Try different queries
3. **Learn**: Read the documentation
4. **Modify**: Change settings and data
5. **Extend**: Add new features
6. **Share**: Show others what you built!

---

## 🎉 Congratulations!

You now have a fully functional multi-agent healthcare system running locally in VS Code.

**Remember**: This is for educational purposes only - not for actual medical use.

**Have fun exploring!** 🚀

---

**Quick Command Reference:**

```bash
# Run demo
python main.py --demo

# Run interactive
python main.py

# Run examples
python examples/example_diabetes_prediction.py
python examples/example_full_workflow.py

# Get help in interactive mode
python main.py
You: help
You: quit
```

---

**Files to Read:**
1. `README.md` - Start here
2. `QUICKSTART.md` - Quick setup
3. `SETUP_VSCODE.md` - Detailed VS Code guide
4. `QUICK_REFERENCE.md` - Command reference
5. `PROJECT_OVERVIEW.md` - Technical deep dive

**Happy coding!** 💻🏥
