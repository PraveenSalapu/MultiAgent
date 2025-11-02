#!/bin/bash

# Healthcare Multi-Agent System - Quick Run Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║    Healthcare Multi-Agent System - Quick Launch           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Function to show menu
show_menu() {
    echo "Select mode:"
    echo "  1) Demo Mode (automated demonstration)"
    echo "  2) Interactive Mode (conversational)"
    echo "  3) Diabetes Prediction Example"
    echo "  4) Complete Workflow Example"
    echo "  5) Exit"
    echo ""
    read -p "Enter choice [1-5]: " choice
    return $choice
}

# Main menu loop
while true; do
    show_menu
    choice=$?

    case $choice in
        1)
            echo ""
            echo "Starting Demo Mode..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            python main.py --demo
            ;;
        2)
            echo ""
            echo "Starting Interactive Mode..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            python main.py
            ;;
        3)
            echo ""
            echo "Running Diabetes Prediction Example..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            python examples/example_diabetes_prediction.py
            ;;
        4)
            echo ""
            echo "Running Complete Workflow Example..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            python examples/example_full_workflow.py
            ;;
        5)
            echo ""
            echo "Thank you for using Healthcare Multi-Agent System!"
            exit 0
            ;;
        *)
            echo ""
            echo "Invalid choice. Please try again."
            ;;
    esac

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    read -p "Press Enter to return to main menu..."
    echo ""
done
