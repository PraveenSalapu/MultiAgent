"""
Hybrid Healthcare Provider Locator
Intelligently combines real-time web search with static fallback data
"""

from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseHealthcareAgent
from .provider_locator_agent import HealthcareProviderLocator
from .provider_locator_realtime import RealTimeProviderLocator
import math


class HybridProviderLocator(BaseHealthcareAgent):
    """
    Hybrid provider locator that intelligently uses both real-time and static sources

    Features:
    - Tries real-time web search first
    - Automatically falls back to static data if needed
    - Can merge results from both sources
    - Allows manual mode selection
    - Tracks data sources for transparency
    """

    def __init__(
        self,
        web_search_function: Optional[Callable] = None,
        prefer_web_search: bool = True,
        merge_results: bool = False,
        max_results: int = 10
    ):
        super().__init__(
            agent_name="Hybrid Healthcare Provider Locator",
            capabilities=["find_providers", "locate_facilities", "real_time_search",
                         "offline_search", "hybrid_search"]
        )

        # Initialize both locators
        self.realtime_locator = RealTimeProviderLocator(web_search_function=web_search_function)
        self.static_locator = HealthcareProviderLocator()

        # Configuration
        self.prefer_web_search = prefer_web_search
        self.merge_results = merge_results
        self.max_results = max_results

        # Statistics
        self.stats = {
            'total_searches': 0,
            'web_searches': 0,
            'static_searches': 0,
            'hybrid_searches': 0,
            'web_failures': 0
        }

    def calculate_distance(self, coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 3959  # Earth's radius in miles

        lat1, lon1 = math.radians(coord1['lat']), math.radians(coord1['lon'])
        lat2, lon2 = math.radians(coord2['lat']), math.radians(coord2['lon'])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def add_distance_to_facilities(
        self,
        facilities: List[Dict[str, Any]],
        user_location: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Add distance calculation to facilities that have coordinates"""
        for facility in facilities:
            if 'coordinates' in facility and user_location:
                distance = self.calculate_distance(user_location, facility['coordinates'])
                facility['distance'] = round(distance, 2)
        return facilities

    def search_web_and_static(
        self,
        user_input: str,
        context: Dict[str, Any],
        specialization: str = None,
        facility_type: str = None,
        emergency_only: bool = False
    ) -> Dict[str, Any]:
        """
        Perform hybrid search using both web and static sources

        Strategies:
        1. Web Only: Use only web search (falls back to static if fails)
        2. Static Only: Use only static data
        3. Hybrid: Try web first, merge with static if available
        """

        self.stats['total_searches'] += 1

        web_results = []
        static_results = []
        search_mode = 'unknown'

        # Strategy 1: Try web search if preferred
        if self.prefer_web_search:
            try:
                print("🌐 Attempting real-time web search...")
                web_response = self.realtime_locator.process_request(user_input, context)

                if web_response['status'] == 'success':
                    web_results = web_response.get('facilities', [])
                    self.stats['web_searches'] += 1
                    search_mode = 'web_search'
                    print(f"✅ Web search successful: {len(web_results)} results")
                else:
                    print("⚠️  Web search returned no results")
                    self.stats['web_failures'] += 1

            except Exception as e:
                print(f"❌ Web search failed: {e}")
                self.stats['web_failures'] += 1

        # Strategy 2: Get static results (as backup or for merging)
        if not web_results or self.merge_results:
            try:
                print("📋 Fetching static/offline data...")
                static_response = self.static_locator.process_request(user_input, context)

                if static_response['status'] == 'success':
                    static_results = static_response.get('facilities', [])
                    self.stats['static_searches'] += 1

                    if not web_results:
                        search_mode = 'static_fallback'
                        print(f"📋 Using static data: {len(static_results)} results")
                    else:
                        search_mode = 'hybrid'
                        self.stats['hybrid_searches'] += 1
                        print(f"🔄 Hybrid mode: {len(static_results)} static results to merge")

            except Exception as e:
                print(f"❌ Static search also failed: {e}")

        # Merge or choose results
        if self.merge_results and web_results and static_results:
            # Merge results, preferring web results but including unique static ones
            merged = self._merge_results(web_results, static_results)
            final_results = merged
            print(f"🔄 Merged results: {len(final_results)} total")
        elif web_results:
            final_results = web_results
        elif static_results:
            final_results = static_results
        else:
            final_results = []
            search_mode = 'no_results'

        # Add distance if user location is available
        user_location = context.get('user_location')
        if user_location and final_results:
            final_results = self.add_distance_to_facilities(final_results, user_location)
            # Sort by distance if available
            final_results.sort(key=lambda x: x.get('distance', float('inf')))

        return {
            'results': final_results[:self.max_results],
            'search_mode': search_mode,
            'web_count': len(web_results),
            'static_count': len(static_results),
            'total_count': len(final_results)
        }

    def _merge_results(
        self,
        web_results: List[Dict[str, Any]],
        static_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge web and static results, avoiding duplicates
        Prioritizes web results for better accuracy
        """
        merged = []

        # Add all web results first
        for result in web_results:
            result['primary_source'] = 'web_search'
            merged.append(result)

        # Add static results that don't appear to be duplicates
        for static_result in static_results:
            # Check if this might be a duplicate (simple name matching)
            is_duplicate = False
            for web_result in web_results:
                if self._is_similar_facility(web_result, static_result):
                    is_duplicate = True
                    break

            if not is_duplicate:
                static_result['primary_source'] = 'static_data'
                merged.append(static_result)

        return merged

    def _is_similar_facility(self, facility1: Dict[str, Any], facility2: Dict[str, Any]) -> bool:
        """
        Check if two facilities might be the same
        Uses simple name similarity check
        """
        name1 = facility1.get('name', '').lower()
        name2 = facility2.get('name', '').lower()

        # Simple substring matching
        if len(name1) > 10 and len(name2) > 10:
            # Check if significant portion of name matches
            shorter = min(name1, name2, key=len)
            longer = max(name1, name2, key=len)
            return shorter[:10] in longer

        return name1 == name2

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process provider search using hybrid approach"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Check for manual mode override in context
        force_mode = context.get('search_mode')
        if force_mode == 'web_only':
            print("🌐 Forced mode: Web search only")
            return self.realtime_locator.process_request(user_input, context)
        elif force_mode == 'static_only':
            print("📋 Forced mode: Static data only")
            return self.static_locator.process_request(user_input, context)

        # Display hybrid mode banner
        print("\n" + "="*60)
        print("🔄 HYBRID PROVIDER SEARCH")
        print("="*60)
        print(f"Mode: {'Web preferred' if self.prefer_web_search else 'Static preferred'}")
        print(f"Merge: {'Yes' if self.merge_results else 'No'}")
        print("="*60 + "\n")

        # Extract criteria (same as other locators)
        specialization = None
        facility_type = None
        emergency_only = False

        if any(word in user_lower for word in ['diabetes', 'diabetologist', 'endocrinologist']):
            specialization = 'diabetes'
        elif any(word in user_lower for word in ['nutrition', 'dietician', 'nutritionist']):
            specialization = 'nutrition'
        elif any(word in user_lower for word in ['cardio', 'heart']):
            specialization = 'cardiology'
        elif any(word in user_lower for word in ['emergency', 'urgent']):
            emergency_only = True

        if 'hospital' in user_lower:
            facility_type = 'hospital'
        elif 'clinic' in user_lower:
            facility_type = 'clinic'

        # Perform hybrid search
        search_result = self.search_web_and_static(
            user_input=user_input,
            context=context,
            specialization=specialization,
            facility_type=facility_type,
            emergency_only=emergency_only
        )

        facilities = search_result['results']
        search_mode = search_result['search_mode']

        if not facilities:
            return {
                'status': 'no_results',
                'agent': self.agent_name,
                'message': 'No healthcare facilities found matching your criteria',
                'search_mode': search_mode,
                'stats': self.stats,
                'suggestion': 'Try different location or broader search criteria'
            }

        # Build response
        response = {
            'status': 'success',
            'agent': self.agent_name,
            'message': f"Found {len(facilities)} healthcare facilities using {search_mode}",
            'facilities': facilities,
            'total_found': search_result['total_count'],
            'search_mode': search_mode,
            'search_breakdown': {
                'web_results': search_result['web_count'],
                'static_results': search_result['static_count'],
                'displayed': len(facilities)
            },
            'filters_applied': {
                'specialization': specialization,
                'facility_type': facility_type,
                'emergency_only': emergency_only
            },
            'stats': self.stats.copy(),
            'next_steps': [
                '📞 Call to verify current information',
                '🏥 Check if they accept your insurance',
                '📅 Schedule an appointment',
                '🗺️  Get directions to the facility',
                '⭐ Read recent reviews'
            ]
        }

        # Add mode-specific disclaimers
        if search_mode == 'web_search':
            response['disclaimer'] = 'Information from real-time web search. Please verify before visiting.'
        elif search_mode == 'static_fallback':
            response['disclaimer'] = 'Using offline sample data. Information may not be current.'
        elif search_mode == 'hybrid':
            response['disclaimer'] = 'Results from multiple sources. Verify details before visiting.'

        self.log_interaction(user_input, response)
        return response

    def format_facility_info(self, facility: Dict[str, Any]) -> str:
        """Format facility information with source indicator"""
        # Determine source icon
        source = facility.get('source', facility.get('primary_source', 'unknown'))
        if source == 'web_search' or source == 'live_web_search':
            icon = "🌐"
            source_text = "Web Search"
        elif source == 'static_data' or source == 'sample_data':
            icon = "📋"
            source_text = "Offline Data"
        else:
            icon = "❓"
            source_text = "Unknown"

        info = f"""
{icon} {facility['name']}
   📍 Address: {facility.get('address', 'Address not available')}
   📞 Phone: {facility.get('phone', 'Phone not available')}
   🏥 Type: {facility.get('type', 'Healthcare Facility')}
"""

        if facility.get('distance'):
            info += f"   📏 Distance: {facility['distance']} miles\n"

        if facility.get('rating') and facility['rating'] > 0:
            stars = '⭐' * int(facility['rating'])
            info += f"   {stars} Rating: {facility['rating']}/5.0\n"

        if facility.get('specializations'):
            specs = facility['specializations']
            if isinstance(specs, list):
                info += f"   🔬 Specializations: {', '.join(specs)}\n"

        if facility.get('website'):
            info += f"   🌐 Website: {facility['website']}\n"

        if facility.get('hours'):
            info += f"   🕐 Hours: {facility['hours']}\n"

        info += f"   ℹ️  Source: {source_text}\n"

        return info

    def set_mode(self, mode: str):
        """
        Change search mode

        Modes:
        - 'web_preferred': Try web first, fall back to static (default)
        - 'static_preferred': Use static data primarily
        - 'hybrid': Always merge both sources
        - 'web_only': Only use web (may return no results)
        - 'static_only': Only use static data
        """
        if mode == 'web_preferred':
            self.prefer_web_search = True
            self.merge_results = False
        elif mode == 'static_preferred':
            self.prefer_web_search = False
            self.merge_results = False
        elif mode == 'hybrid':
            self.prefer_web_search = True
            self.merge_results = True
        elif mode == 'web_only':
            self.prefer_web_search = True
            self.merge_results = False
        elif mode == 'static_only':
            self.prefer_web_search = False
            self.merge_results = False

        print(f"✅ Search mode set to: {mode}")

    def get_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        total = self.stats['total_searches']
        if total > 0:
            web_pct = (self.stats['web_searches'] / total) * 100
            static_pct = (self.stats['static_searches'] / total) * 100
            hybrid_pct = (self.stats['hybrid_searches'] / total) * 100
            failure_pct = (self.stats['web_failures'] / total) * 100
        else:
            web_pct = static_pct = hybrid_pct = failure_pct = 0

        return {
            **self.stats,
            'percentages': {
                'web_searches': round(web_pct, 1),
                'static_searches': round(static_pct, 1),
                'hybrid_searches': round(hybrid_pct, 1),
                'web_failures': round(failure_pct, 1)
            }
        }

    def reset_stats(self):
        """Reset search statistics"""
        self.stats = {
            'total_searches': 0,
            'web_searches': 0,
            'static_searches': 0,
            'hybrid_searches': 0,
            'web_failures': 0
        }
        print("📊 Statistics reset")
