"""
Example: Hybrid Provider Search
Demonstrates intelligent combination of real-time web search and static data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.provider_locator_hybrid import HybridProviderLocator


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_stats(locator):
    """Print search statistics"""
    stats = locator.get_stats()
    print("\n📊 SEARCH STATISTICS")
    print("-" * 70)
    print(f"Total Searches: {stats['total_searches']}")
    print(f"Web Searches: {stats['web_searches']} ({stats['percentages']['web_searches']}%)")
    print(f"Static Searches: {stats['static_searches']} ({stats['percentages']['static_searches']}%)")
    print(f"Hybrid Searches: {stats['hybrid_searches']} ({stats['percentages']['hybrid_searches']}%)")
    print(f"Web Failures: {stats['web_failures']} ({stats['percentages']['web_failures']}%)")
    print("-" * 70)


def main():
    """Demonstrate hybrid provider search"""

    print_section("HYBRID HEALTHCARE PROVIDER SEARCH DEMO")

    print("""
This demo shows how the Hybrid Provider Locator intelligently combines:
- Real-time web search (for current, accurate data)
- Static offline data (for reliability and speed)

The hybrid approach provides:
✅ Best of both worlds
✅ Automatic fallback
✅ Always returns results
✅ Tracks data sources
✅ Configurable modes
""")

    # =========================================================================
    # Example 1: Default Hybrid Mode (Web Preferred with Fallback)
    # =========================================================================
    print_section("Example 1: Default Hybrid Mode (Web Preferred)")

    locator = HybridProviderLocator(
        prefer_web_search=True,
        merge_results=False  # Use web or fall back to static
    )

    print("Configuration:")
    print("  - Prefer Web Search: True")
    print("  - Merge Results: False")
    print("  - Strategy: Try web first, fall back to static if needed\n")

    response1 = locator.process_request(
        "Find diabetes specialists in Baltimore, MD",
        context={}
    )

    print(f"Status: {response1['status']}")
    print(f"Search Mode Used: {response1['search_mode']}")
    print(f"Total Found: {response1['total_found']}")
    print(f"\nSearch Breakdown:")
    print(f"  - Web Results: {response1['search_breakdown']['web_results']}")
    print(f"  - Static Results: {response1['search_breakdown']['static_results']}")
    print(f"  - Displayed: {response1['search_breakdown']['displayed']}")

    print(f"\nTop 3 Facilities:\n")
    for i, facility in enumerate(response1['facilities'][:3], 1):
        print(f"{i}. {facility['name']}")
        source = facility.get('source', facility.get('primary_source', 'unknown'))
        print(f"   Source: {source}")
        print(f"   Address: {facility.get('address', 'N/A')}")
        print(f"   Phone: {facility.get('phone', 'N/A')}")
        if facility.get('rating'):
            print(f"   Rating: {facility['rating']}/5.0")
        print()

    # =========================================================================
    # Example 2: Hybrid Merge Mode
    # =========================================================================
    print_section("Example 2: Hybrid Merge Mode (Combine Both Sources)")

    locator2 = HybridProviderLocator(
        prefer_web_search=True,
        merge_results=True  # Merge web and static results
    )

    print("Configuration:")
    print("  - Prefer Web Search: True")
    print("  - Merge Results: True")
    print("  - Strategy: Get both web and static, merge unique results\n")

    response2 = locator2.process_request(
        "Find nearby hospitals with diabetes care",
        context={}
    )

    print(f"Search Mode: {response2['search_mode']}")
    print(f"Total Results: {response2['total_found']}")
    print(f"\nSearch Breakdown:")
    print(f"  - Web Results: {response2['search_breakdown']['web_results']}")
    print(f"  - Static Results: {response2['search_breakdown']['static_results']}")
    print(f"  - After Merging: {response2['total_found']}")

    print(f"\nMerged Results (showing source for each):\n")
    for facility in response2['facilities'][:5]:
        source = facility.get('source', facility.get('primary_source', 'unknown'))
        source_icon = "🌐" if 'web' in source else "📋"
        print(f"{source_icon} {facility['name']} [{source}]")

    # =========================================================================
    # Example 3: Mode Switching
    # =========================================================================
    print_section("Example 3: Dynamic Mode Switching")

    locator3 = HybridProviderLocator()

    print("Demonstrating different search modes:\n")

    # Mode 1: Web Preferred (default)
    print("1️⃣  WEB PREFERRED MODE")
    print("   Strategy: Try web first, use static only if web fails")
    locator3.set_mode('web_preferred')
    response3a = locator3.process_request("Find clinics in Boston", {})
    print(f"   Result: {response3a['search_mode']} ({response3a['total_found']} facilities)\n")

    # Mode 2: Static Preferred
    print("2️⃣  STATIC PREFERRED MODE")
    print("   Strategy: Use static data primarily")
    locator3.set_mode('static_preferred')
    response3b = locator3.process_request("Find clinics", {})
    print(f"   Result: {response3b['search_mode']} ({response3b['total_found']} facilities)\n")

    # Mode 3: Hybrid (merge both)
    print("3️⃣  HYBRID MERGE MODE")
    print("   Strategy: Always get and merge both sources")
    locator3.set_mode('hybrid')
    response3c = locator3.process_request("Find healthcare providers", {})
    print(f"   Result: {response3c['search_mode']} ({response3c['total_found']} facilities)\n")

    # =========================================================================
    # Example 4: Location-Based Search with Distances
    # =========================================================================
    print_section("Example 4: Location-Based Search (with Distance Calculation)")

    locator4 = HybridProviderLocator()

    print("Searching with user location coordinates...")
    print("Location: Baltimore area (39.2904°N, 76.6122°W)\n")

    response4 = locator4.process_request(
        "Find diabetes care centers",
        context={
            'user_location': {
                'lat': 39.2904,
                'lon': -76.6122
            }
        }
    )

    print(f"Found {response4['total_found']} facilities\n")
    print("Results sorted by distance:\n")

    for i, facility in enumerate(response4['facilities'][:5], 1):
        print(f"{i}. {facility['name']}")
        if facility.get('distance'):
            print(f"   📏 Distance: {facility['distance']} miles")
        print(f"   📍 {facility.get('address', 'Address N/A')}")
        print()

    # =========================================================================
    # Example 5: Forced Mode via Context
    # =========================================================================
    print_section("Example 5: Force Specific Mode via Context")

    locator5 = HybridProviderLocator()

    print("You can force a specific mode by passing it in context:\n")

    # Force web only
    print("🌐 Forcing WEB ONLY mode:")
    response5a = locator5.process_request(
        "Find hospitals",
        context={'search_mode': 'web_only'}
    )
    print(f"   Used: {response5a['search_mode']}\n")

    # Force static only
    print("📋 Forcing STATIC ONLY mode:")
    response5b = locator5.process_request(
        "Find hospitals",
        context={'search_mode': 'static_only'}
    )
    print(f"   Used: {response5b['search_mode']}\n")

    # =========================================================================
    # Example 6: Detailed Facility Information
    # =========================================================================
    print_section("Example 6: Detailed Facility Information")

    locator6 = HybridProviderLocator(merge_results=True)

    response6 = locator6.process_request(
        "Find diabetes specialists",
        context={}
    )

    print("Showing detailed information for top result:\n")
    if response6['facilities']:
        facility = response6['facilities'][0]
        print(locator6.format_facility_info(facility))

    # =========================================================================
    # Statistics Summary
    # =========================================================================
    print_section("FINAL STATISTICS")

    # Combine stats from all locators
    all_locators = [locator, locator2, locator3, locator4, locator5, locator6]

    total_searches = sum(l.stats['total_searches'] for l in all_locators)
    total_web = sum(l.stats['web_searches'] for l in all_locators)
    total_static = sum(l.stats['static_searches'] for l in all_locators)
    total_hybrid = sum(l.stats['hybrid_searches'] for l in all_locators)
    total_failures = sum(l.stats['web_failures'] for l in all_locators)

    print(f"Total Searches Performed: {total_searches}")
    print(f"  - Web Searches: {total_web}")
    print(f"  - Static Searches: {total_static}")
    print(f"  - Hybrid Searches: {total_hybrid}")
    print(f"  - Web Failures: {total_failures}")

    # =========================================================================
    # Benefits Summary
    # =========================================================================
    print_section("HYBRID APPROACH BENEFITS")

    print("""
✅ RELIABILITY
   - Always returns results (fallback to static if web fails)
   - Graceful degradation
   - No single point of failure

✅ ACCURACY
   - Prefers real-time web data when available
   - Up-to-date provider information
   - Real phone numbers and addresses

✅ FLEXIBILITY
   - Multiple search modes
   - Can be configured per-request
   - Supports offline operation

✅ PERFORMANCE
   - Caches web search results
   - Uses fast static data when appropriate
   - Optimized query building

✅ TRANSPARENCY
   - Tracks which source provided each result
   - Reports search mode used
   - Provides detailed statistics

✅ BEST OF BOTH WORLDS
   - Web search: Current, accurate data
   - Static data: Fast, reliable fallback
   - Hybrid: Maximum coverage
""")

    # =========================================================================
    # Configuration Options
    # =========================================================================
    print_section("CONFIGURATION OPTIONS")

    print("""
Initialize with different strategies:

1. WEB PREFERRED (DEFAULT)
   locator = HybridProviderLocator(prefer_web_search=True, merge_results=False)
   → Tries web first, falls back to static

2. STATIC PREFERRED
   locator = HybridProviderLocator(prefer_web_search=False, merge_results=False)
   → Uses static data by default

3. ALWAYS MERGE
   locator = HybridProviderLocator(prefer_web_search=True, merge_results=True)
   → Always gets both and merges unique results

4. CUSTOM LIMITS
   locator = HybridProviderLocator(max_results=20)
   → Control how many results to return

5. RUNTIME MODE CHANGE
   locator.set_mode('hybrid')  # or 'web_preferred', 'static_preferred'
   → Change mode dynamically

6. FORCE MODE IN REQUEST
   locator.process_request(query, context={'search_mode': 'web_only'})
   → Override for specific request
""")

    # =========================================================================
    # Integration Example
    # =========================================================================
    print_section("INTEGRATION WITH MAIN SYSTEM")

    print("""
The main Healthcare Multi-Agent System now uses Hybrid Provider Locator!

In main.py:
    from agents.provider_locator_hybrid import HybridProviderLocator

    agents = [
        DiabetesPredictionAgent(),
        AppointmentSchedulerAgent(),
        HybridProviderLocator(prefer_web_search=True, merge_results=False),
        # ... other agents
    ]

When you run the main system:
    python main.py
    You: Find diabetes centers near me

The coordinator will automatically route to the hybrid locator, which will:
1. Try web search first
2. Fall back to static data if needed
3. Return the best available results
""")

    # =========================================================================
    # Use Cases
    # =========================================================================
    print_section("COMMON USE CASES")

    print("""
🌐 PRODUCTION DEPLOYMENT
   Use: Web preferred mode
   Why: Get real-time data, fall back automatically
   Config: HybridProviderLocator(prefer_web_search=True, merge_results=False)

📋 OFFLINE/DEMO MODE
   Use: Static preferred mode
   Why: Work without internet, consistent results for demos
   Config: HybridProviderLocator(prefer_web_search=False)

🔄 MAXIMUM COVERAGE
   Use: Hybrid merge mode
   Why: Get results from all available sources
   Config: HybridProviderLocator(merge_results=True)

🧪 TESTING
   Use: Force specific modes
   Why: Test each source independently
   Config: context={'search_mode': 'web_only'} or 'static_only'
""")

    print_section("Demo Complete!")

    print("""
🎉 The hybrid approach is now active in your system!

Try it:
    python main.py
    You: Find diabetes specialists in your city

The system will automatically use the hybrid locator with web search
and fall back to static data if needed.

Documentation:
    - REALTIME_SEARCH.md: Web search details
    - agents/provider_locator_hybrid.py: Implementation
    - This file: Usage examples
""")


if __name__ == "__main__":
    main()
