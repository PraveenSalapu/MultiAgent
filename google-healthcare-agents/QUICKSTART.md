# Quick Start Guide

## 5-Minute Setup

### 1. Verify Python Installation
```bash
python --version  # Should be 3.7 or higher
```

### 2. Navigate to Project Directory
```bash
cd google-healthcare-agents
```

### 3. Run Demo Mode
```bash
python main.py --demo
```

This will run through 5 example scenarios showing all agent capabilities.

## Interactive Usage

### Start Interactive Mode
```bash
python main.py
```

### Try These Queries

#### Diabetes Risk Prediction
```
You: I'm 52 years old, BMI 32, blood glucose 145, what's my diabetes risk?
```

#### Find Healthcare Providers
```
You: Find nearby diabetes care centers
```

#### Schedule Appointment
```
You: Schedule an appointment with a diabetologist
```

#### Get Diet Plan
```
You: Suggest a diet plan for diabetes management
```

#### Diabetes Care Guidance
```
You: How should I manage my diabetes?
```

#### General Health
```
You: What are some healthy eating tips?
```

### Load Patient Data
```
You: load patient P001
You: Predict my diabetes risk
```

### Exit
```
You: quit
```

## Running Examples

### Diabetes Prediction Examples
```bash
python examples/example_diabetes_prediction.py
```

### Complete Workflow
```bash
python examples/example_full_workflow.py
```

## Single Query Mode

Ask a single question directly:
```bash
python main.py "What's my diabetes risk if I have high blood sugar?"
```

## Understanding Responses

Each response shows:
- **Agent**: Which specialized agent handled your query
- **Status**: Success/error status
- **Message**: Primary response message
- **Details**: Specific information (predictions, appointments, etc.)
- **Next Steps**: Recommended follow-up actions

## Tips

1. **Be Natural**: Ask questions in plain English
2. **Provide Context**: Include relevant health information
3. **Load Patients**: Use sample patient data for testing
4. **Explore Agents**: Try different types of queries to see all agents

## Common Commands

```bash
# Interactive mode (recommended for exploration)
python main.py

# Demo mode (shows all features)
python main.py --demo

# Single query
python main.py "your question here"

# Run examples
python examples/example_diabetes_prediction.py
python examples/example_full_workflow.py
```

## Troubleshooting

### "No module named..." error
Make sure you're in the `google-healthcare-agents` directory:
```bash
pwd  # Should show .../google-healthcare-agents
```

### Agent not responding as expected
Try being more specific in your query or include relevant context.

### Want to see raw response data
Responses are Python dictionaries. You can print them in code:
```python
import json
print(json.dumps(response, indent=2))
```

## Next Steps

1. ✅ Run demo mode to see all features
2. ✅ Try interactive mode with different queries
3. ✅ Load sample patient data
4. ✅ Run example scripts
5. ✅ Read the full README.md for detailed documentation
6. ✅ Explore the agent code in `agents/` directory

## Need Help?

- Type `help` in interactive mode
- Check README.md for full documentation
- Review example scripts in `examples/`
- Read agent code for implementation details

---

**Ready to start? Run:**
```bash
python main.py --demo
```
