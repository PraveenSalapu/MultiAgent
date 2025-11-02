"""
Example: Real-Time Healthcare Provider Search
Demonstrates dynamic web-based provider location
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.provider_locator_realtime import RealTimeProviderLocator


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    """Demonstrate real-time provider search"""

    print_section("REAL-TIME HEALTHCARE PROVIDER SEARCH DEMO")

    # Create real-time provider locator
    # In production, you would pass an actual web search function
    locator = RealTimeProviderLocator(web_search_function=None)  # Will use simulation

    # Example 1: Search for diabetes specialists in a specific city
    print_section("Example 1: Diabetes Specialists in Baltimore, MD")

    response1 = locator.process_request(
        "Find diabetes specialists in Baltimore, MD",
        context={}
    )

    print(f"Status: {response1['status']}")
    print(f"Search Mode: {response1['search_mode']}")
    print(f"Location Searched: {response1['location_searched']}")
    print(f"Total Found: {response1['total_found']}")
    print(f"\nTop Results:\n")

    for facility in response1['facilities']:
        print(locator.format_facility_info(facility))
        print("-" * 70)

    # Example 2: Search with different location
    print_section("Example 2: Nutritionists near New York, NY")

    response2 = locator.process_request(
        "Find nutritionist clinics near New York, NY",
        context={'location_name': 'New York, NY'}
    )

    print(f"Found {response2['total_found']} facilities")
    print(f"\nTop 3 Results:\n")

    for i, facility in enumerate(response2['facilities'][:3], 1):
        print(f"{i}. {facility['name']}")
        print(f"   Address: {facility['address']}")
        print(f"   Phone: {facility['phone']}")
        print(f"   Specializations: {', '.join(facility['specializations'])}")
        if facility.get('rating') and facility['rating'] > 0:
            print(f"   Rating: {facility['rating']}/5.0 ⭐")
        print()

    # Example 3: Emergency services search
    print_section("Example 3: Emergency Diabetes Care")

    response3 = locator.process_request(
        "Find hospitals with emergency diabetes care in Boston, MA",
        context={}
    )

    print(f"Status: {response3['status']}")
    print(f"Facilities found: {response3['total_found']}")
    print(f"\nFilters applied:")
    for key, value in response3['filters_applied'].items():
        print(f"  - {key}: {value}")

    # Example 4: Using coordinates
    print_section("Example 4: Search Using Coordinates")

    response4 = locator.process_request(
        "Find healthcare providers specializing in diabetes",
        context={
            'user_location': {
                'lat': 39.2904,
                'lon': -76.6122
            }
        }
    )

    print(f"Search location: {response4['location_searched']}")
    print(f"Found: {response4['total_found']} providers")

    # Show comparison with old system
    print_section("COMPARISON: Real-Time vs Static Data")

    print("✅ Real-Time Search Advantages:")
    print("   • Always up-to-date provider information")
    print("   • Search any location dynamically")
    print("   • Real phone numbers and addresses")
    print("   • Current ratings and reviews")
    print("   • Website links for more information")
    print("   • Actual hours of operation")
    print()

    print("📋 Static Data (Fallback) Advantages:")
    print("   • Works offline")
    print("   • Faster response time")
    print("   • No external dependencies")
    print("   • Predictable results for testing")
    print()

    # Show how the system handles the data
    print_section("HOW IT WORKS")

    print("🔍 Search Process:")
    print("   1. Extract location from user query or context")
    print("   2. Identify specialization/facility type needed")
    print("   3. Build optimized search query")
    print("   4. Perform web search (or use simulation)")
    print("   5. Parse search results to extract:")
    print("      • Provider name")
    print("      • Address and phone")
    print("      • Ratings and reviews")
    print("      • Specializations")
    print("      • Hours and website")
    print("   6. Format and return top results")
    print()

    print("🔄 Fallback Mechanism:")
    print("   • If web search fails → Use simulated data")
    print("   • If no results found → Suggest broader search")
    print("   • Cache results to reduce repeated searches")
    print()

    # Integration example
    print_section("INTEGRATION WITH HEALTHCARE SYSTEM")

    print("To use in the main healthcare system:")
    print()
    print("```python")
    print("from agents.provider_locator_realtime import RealTimeProviderLocator")
    print()
    print("# Create with web search capability")
    print("locator = RealTimeProviderLocator(")
    print("    web_search_function=your_search_function")
    print(")")
    print()
    print("# Register with coordinator")
    print("coordinator.register_agent(locator)")
    print()
    print("# Now queries will use real-time search!")
    print("response = coordinator.process_request(")
    print('    "Find diabetes centers in Chicago"')
    print(")")
    print("```")
    print()

    print_section("CUSTOMIZATION OPTIONS")

    print("You can customize the search by:")
    print()
    print("1. Location Formats Supported:")
    print("   • City, State: 'Baltimore, MD'")
    print("   • Coordinates: lat/lon pairs")
    print("   • ZIP code: '21201'")
    print("   • Neighborhood: 'Downtown Manhattan'")
    print()
    print("2. Search Filters:")
    print("   • Specialization: diabetes, nutrition, cardiology, etc.")
    print("   • Facility Type: hospital, clinic, medical center")
    print("   • Emergency Services: 24/7 availability")
    print("   • Insurance: specific insurance plans")
    print()
    print("3. Result Parsing:")
    print("   • Extracts structured data from text")
    print("   • Handles various format variations")
    print("   • Validates phone numbers and addresses")
    print("   • Detects specializations from descriptions")
    print()

    print_section("NEXT STEPS")

    print("To enable full web search capabilities:")
    print()
    print("1. Install web search package (if using external API):")
    print("   pip install requests beautifulsoup4")
    print()
    print("2. Integrate with search API:")
    print("   • Google Custom Search API")
    print("   • Bing Search API")
    print("   • SerpAPI")
    print("   • Or use the built-in WebSearch tool")
    print()
    print("3. Update main.py to use RealTimeProviderLocator:")
    print("   Replace HealthcareProviderLocator with RealTimeProviderLocator")
    print()
    print("4. Set up caching for better performance:")
    print("   • Cache results for common searches")
    print("   • Expire cache after reasonable time (e.g., 24 hours)")
    print()

    print("\n" + "=" * 70)
    print("  Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
