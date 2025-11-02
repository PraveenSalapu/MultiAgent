"""
Dietician Agent
Provides personalized dietary recommendations and meal planning
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent


class DieticianAgent(BaseHealthcareAgent):
    """
    Agent specialized in providing dietary recommendations and nutrition counseling
    """

    def __init__(self):
        super().__init__(
            agent_name="Dietician Agent",
            capabilities=["diet_planning", "nutrition_advice", "meal_recommendations"]
        )
        self.meal_plans = self._load_meal_plans()
        self.nutrition_database = self._load_nutrition_database()

    def _load_meal_plans(self) -> Dict[str, Any]:
        """Load sample meal plans for different conditions"""
        return {
            'diabetes': {
                'name': 'Diabetes-Friendly Meal Plan',
                'description': 'Low glycemic index, controlled carbohydrate meal plan',
                'daily_calories': 1800,
                'macros': {'carbs': '45%', 'protein': '25%', 'fat': '30%'},
                'meals': {
                    'breakfast': [
                        'Steel-cut oatmeal with berries and almonds',
                        'Greek yogurt with chia seeds and walnuts',
                        'Vegetable omelet with whole grain toast'
                    ],
                    'lunch': [
                        'Grilled chicken salad with olive oil dressing',
                        'Quinoa bowl with roasted vegetables and chickpeas',
                        'Turkey and avocado wrap with mixed greens'
                    ],
                    'dinner': [
                        'Baked salmon with steamed broccoli and brown rice',
                        'Grilled chicken breast with sweet potato and green beans',
                        'Lean beef stir-fry with mixed vegetables'
                    ],
                    'snacks': [
                        'Apple slices with almond butter',
                        'Carrot sticks with hummus',
                        'Handful of mixed nuts',
                        'Low-fat cheese with whole grain crackers'
                    ]
                }
            },
            'weight_loss': {
                'name': 'Healthy Weight Loss Plan',
                'description': 'Balanced, calorie-controlled meal plan',
                'daily_calories': 1500,
                'macros': {'carbs': '40%', 'protein': '30%', 'fat': '30%'},
                'meals': {
                    'breakfast': [
                        'Protein smoothie with spinach and berries',
                        'Egg white scramble with vegetables',
                        'Overnight oats with protein powder'
                    ],
                    'lunch': [
                        'Large mixed green salad with grilled chicken',
                        'Vegetable soup with lentils',
                        'Tuna salad with mixed greens'
                    ],
                    'dinner': [
                        'Grilled fish with roasted vegetables',
                        'Turkey meatballs with zucchini noodles',
                        'Chicken breast with cauliflower rice'
                    ],
                    'snacks': [
                        'Celery with peanut butter',
                        'Greek yogurt',
                        'Cherry tomatoes with mozzarella',
                        'Protein shake'
                    ]
                }
            },
            'heart_healthy': {
                'name': 'Heart-Healthy Mediterranean Plan',
                'description': 'Mediterranean-style diet for cardiovascular health',
                'daily_calories': 2000,
                'macros': {'carbs': '50%', 'protein': '20%', 'fat': '30%'},
                'meals': {
                    'breakfast': [
                        'Whole grain toast with avocado and tomato',
                        'Greek yogurt with honey and walnuts',
                        'Fruit salad with nuts and seeds'
                    ],
                    'lunch': [
                        'Mediterranean chickpea salad',
                        'Grilled fish with quinoa and vegetables',
                        'Lentil soup with whole grain bread'
                    ],
                    'dinner': [
                        'Grilled salmon with olive oil and herbs',
                        'Chicken with roasted Mediterranean vegetables',
                        'Bean and vegetable stew'
                    ],
                    'snacks': [
                        'Olives and whole grain crackers',
                        'Fresh fruit',
                        'Handful of almonds',
                        'Hummus with vegetable sticks'
                    ]
                }
            },
            'general': {
                'name': 'Balanced Healthy Eating Plan',
                'description': 'Well-rounded nutritious meal plan',
                'daily_calories': 2000,
                'macros': {'carbs': '50%', 'protein': '25%', 'fat': '25%'},
                'meals': {
                    'breakfast': [
                        'Whole grain cereal with milk and banana',
                        'Scrambled eggs with whole wheat toast',
                        'Smoothie bowl with granola'
                    ],
                    'lunch': [
                        'Chicken sandwich with vegetables',
                        'Brown rice bowl with protein and vegetables',
                        'Pasta salad with lean protein'
                    ],
                    'dinner': [
                        'Grilled chicken with roasted vegetables',
                        'Fish with quinoa and salad',
                        'Lean beef with sweet potato and broccoli'
                    ],
                    'snacks': [
                        'Fresh fruit',
                        'Yogurt',
                        'Trail mix',
                        'Vegetable sticks with dip'
                    ]
                }
            }
        }

    def _load_nutrition_database(self) -> Dict[str, List[str]]:
        """Load nutrition recommendations database"""
        return {
            'diabetes_foods_to_eat': [
                'Leafy green vegetables (spinach, kale, collards)',
                'Whole grains (quinoa, brown rice, oats)',
                'Fatty fish (salmon, mackerel, sardines)',
                'Nuts and seeds (almonds, walnuts, chia seeds)',
                'Beans and legumes',
                'Greek yogurt',
                'Berries (blueberries, strawberries)',
                'Non-starchy vegetables (broccoli, cauliflower, peppers)'
            ],
            'diabetes_foods_to_avoid': [
                'Sugary beverages (soda, sweetened tea, juice)',
                'White bread and refined grains',
                'Sweetened breakfast cereals',
                'Fried foods',
                'Candy and sweets',
                'Processed snacks',
                'High-fat dairy products',
                'Fatty red meats'
            ],
            'general_nutrition_tips': [
                'Stay hydrated - drink 8-10 glasses of water daily',
                'Eat at regular intervals to maintain blood sugar',
                'Include protein in every meal',
                'Choose complex carbohydrates over simple sugars',
                'Limit sodium intake to less than 2,300mg per day',
                'Eat plenty of fiber (25-30g daily)',
                'Practice portion control',
                'Limit alcohol consumption'
            ]
        }

    def get_meal_plan(self, condition: str = 'general') -> Dict[str, Any]:
        """Get appropriate meal plan based on health condition"""
        condition_lower = condition.lower()

        # Map various inputs to meal plan types
        if 'diabetes' in condition_lower or 'diabetic' in condition_lower:
            return self.meal_plans['diabetes']
        elif 'weight' in condition_lower or 'loss' in condition_lower:
            return self.meal_plans['weight_loss']
        elif 'heart' in condition_lower or 'cardiac' in condition_lower:
            return self.meal_plans['heart_healthy']
        else:
            return self.meal_plans['general']

    def generate_daily_menu(self, meal_plan: Dict[str, Any]) -> Dict[str, str]:
        """Generate a sample daily menu from meal plan"""
        import random

        daily_menu = {}
        for meal_type, options in meal_plan['meals'].items():
            if meal_type == 'snacks':
                # Select 2 snacks
                daily_menu[meal_type] = random.sample(options, min(2, len(options)))
            else:
                daily_menu[meal_type] = random.choice(options)

        return daily_menu

    def get_nutrition_recommendations(self, health_context: Dict[str, Any]) -> List[str]:
        """Get personalized nutrition recommendations"""
        recommendations = []

        # Check for diabetes
        if health_context.get('diabetes_risk') in ['HIGH', 'MODERATE'] or \
           health_context.get('has_diabetes'):
            recommendations.extend([
                'Focus on low glycemic index foods',
                'Monitor carbohydrate intake carefully',
                'Eat small, frequent meals throughout the day',
                'Avoid foods that spike blood sugar'
            ])

        # Check for weight management
        bmi = health_context.get('bmi', 0)
        if bmi >= 25:
            recommendations.extend([
                'Create a calorie deficit for weight loss',
                'Increase physical activity',
                'Practice mindful eating',
                'Track your food intake'
            ])

        # Check for blood pressure
        if health_context.get('high_blood_pressure'):
            recommendations.extend([
                'Reduce sodium intake (DASH diet)',
                'Eat potassium-rich foods',
                'Limit processed foods',
                'Increase fruits and vegetables'
            ])

        # General recommendations
        recommendations.extend(self.nutrition_database['general_nutrition_tips'][:3])

        return recommendations

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process dietary recommendation request"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Determine health condition
        condition = 'general'
        if any(word in user_lower for word in ['diabetes', 'diabetic', 'blood sugar']):
            condition = 'diabetes'
        elif any(word in user_lower for word in ['weight', 'lose weight', 'obesity']):
            condition = 'weight_loss'
        elif any(word in user_lower for word in ['heart', 'cardiovascular', 'blood pressure']):
            condition = 'heart_healthy'

        # Get appropriate meal plan
        meal_plan = self.get_meal_plan(condition)

        # Generate daily menu
        daily_menu = self.generate_daily_menu(meal_plan)

        # Get personalized recommendations
        health_context = context.get('health_data', {})
        health_context['diabetes_risk'] = context.get('diabetes_risk')
        recommendations = self.get_nutrition_recommendations(health_context)

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'meal_plan': meal_plan,
            'daily_menu': daily_menu,
            'recommendations': recommendations,
            'message': f"Generated {meal_plan['name']} for your needs",
            'nutrition_tips': {
                'foods_to_eat': self.nutrition_database.get(f'{condition}_foods_to_eat', []),
                'foods_to_avoid': self.nutrition_database.get(f'{condition}_foods_to_avoid', [])
            },
            'next_steps': [
                'Review the meal plan and adapt to your preferences',
                'Consult with a nutritionist for personalized guidance',
                'Track your meals and progress',
                'Stay consistent for best results'
            ]
        }

        self.log_interaction(user_input, response)

        return response

    def format_meal_plan(self, response: Dict[str, Any]) -> str:
        """Format meal plan for display"""
        meal_plan = response['meal_plan']
        daily_menu = response['daily_menu']

        output = f"""
╔══════════════════════════════════════════════════════════╗
║         {meal_plan['name'].upper().center(50)}         ║
╚══════════════════════════════════════════════════════════╝

{meal_plan['description']}

📊 Daily Calories: {meal_plan['daily_calories']} kcal
🥗 Macros: Carbs {meal_plan['macros']['carbs']}, Protein {meal_plan['macros']['protein']}, Fat {meal_plan['macros']['fat']}

TODAY'S MENU:
─────────────────────────────────────────────────────────

🍳 BREAKFAST:
   {daily_menu['breakfast']}

🥗 LUNCH:
   {daily_menu['lunch']}

🍽️ DINNER:
   {daily_menu['dinner']}

🍎 SNACKS:
"""
        for snack in daily_menu['snacks']:
            output += f"   • {snack}\n"

        output += "\n📝 KEY RECOMMENDATIONS:\n"
        for i, rec in enumerate(response['recommendations'][:5], 1):
            output += f"   {i}. {rec}\n"

        return output
