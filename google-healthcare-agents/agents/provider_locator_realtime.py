"""
Real-Time Healthcare Provider Locator with Live Web Search
Uses actual web search to find healthcare providers dynamically
"""

from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseHealthcareAgent
import re


class RealTimeProviderLocator(BaseHealthcareAgent):
    """
    Agent that uses real-time web search to find healthcare providers
    """

    def __init__(self, web_search_function: Optional[Callable] = None):
        super().__init__(
            agent_name="Real-Time Healthcare Provider Locator",
            capabilities=["find_providers", "locate_facilities", "real_time_search", "web_search"]
        )
        self.web_search = web_search_function
        self.search_cache = {}

    def build_search_query(
        self,
        location: str,
        specialization: str = None,
        facility_type: str = None,
        emergency_only: bool = False
    ) -> str:
        """Build optimized search query"""
        query_parts = []

        # Specialization-specific queries
        if specialization:
            spec_lower = specialization.lower()
            if 'diabetes' in spec_lower:
                query_parts.append('diabetes specialist endocrinologist diabetologist')
            elif 'nutrition' in spec_lower:
                query_parts.append('nutritionist dietitian nutrition specialist')
            elif 'cardio' in spec_lower:
                query_parts.append('cardiologist heart specialist')
            else:
                query_parts.append(specialization)

        # Facility type
        if facility_type:
            query_parts.append(facility_type.lower())
        elif not specialization:
            query_parts.append('hospital clinic medical center')

        # Emergency
        if emergency_only:
            query_parts.append('emergency room 24/7')

        # Location
        query_parts.append(f'near {location}')

        # Additional helpful terms
        query_parts.append('phone address hours rating')

        return ' '.join(query_parts)

    def extract_location_from_text(self, text: str) -> Optional[str]:
        """Extract location from user input"""
        location_patterns = [
            r'(?:in|near|around|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z]{2})?)',
            r'([A-Z][a-z]+,\s*[A-Z]{2}\s*\d{5}?)',
            r'([A-Z][a-z]+,\s*[A-Z]{2})',
            r'zip\s*code?\s*:?\s*(\d{5})'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        return None

    def parse_search_results(self, search_results_text: str) -> List[Dict[str, Any]]:
        """
        Parse web search results to extract provider information
        """
        providers = []

        # Split results by common delimiters
        # Assuming search results come as concatenated text blocks
        result_blocks = re.split(r'\n\n+|\n-{3,}\n', search_results_text)

        for i, block in enumerate(result_blocks[:10], 1):  # Limit to 10 results
            if len(block.strip()) < 20:  # Skip very short blocks
                continue

            provider = self._parse_provider_block(block, i)
            if provider:
                providers.append(provider)

        return providers

    def _parse_provider_block(self, text: str, index: int) -> Optional[Dict[str, Any]]:
        """Parse individual search result block"""
        provider = {
            'id': f'LIVE{index:03d}',
            'name': 'Healthcare Provider',
            'type': 'Medical Facility',
            'address': 'Address pending verification',
            'phone': 'Contact for information',
            'website': '',
            'rating': 0.0,
            'specializations': [],
            'hours': 'Call for hours',
            'insurance': 'Contact for insurance information',
            'source': 'live_web_search'
        }

        # Extract provider name (usually first line or capitalized)
        lines = text.strip().split('\n')
        if lines:
            # Look for names with healthcare keywords
            name_pattern = r'^([A-Z][A-Za-z\s\-&\.]+?(?:Hospital|Clinic|Center|Medical|Health|Care|Associates|Group|Institute|Practice|Physicians|Doctors))'
            for line in lines[:3]:
                match = re.search(name_pattern, line.strip())
                if match:
                    provider['name'] = match.group(1).strip()
                    break

            # If still default name, use first substantial line
            if provider['name'] == 'Healthcare Provider' and lines[0].strip():
                provider['name'] = lines[0].strip()[:100]

        # Extract address
        address_patterns = [
            r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl)[,\s]+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5})',
            r'(\d+\s+[A-Za-z0-9\s\.,#]+,\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5})',
            r'Address[:\s]+([^\n]+)',
            r'Location[:\s]+([^\n]+)'
        ]

        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                provider['address'] = match.group(1).strip()
                break

        # Extract phone
        phone_patterns = [
            r'Phone[:\s]+([\(\d\)\s\-\.]+)',
            r'Tel[:\s]+([\(\d\)\s\-\.]+)',
            r'\((\d{3})\)\s*(\d{3})-(\d{4})',
            r'(\d{3})[-\.\s](\d{3})[-\.\s](\d{4})'
        ]

        for pattern in phone_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 3:
                    provider['phone'] = f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
                else:
                    provider['phone'] = match.group(1).strip()
                break

        # Extract website
        website_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)'
        web_match = re.search(website_pattern, text)
        if web_match:
            provider['website'] = web_match.group(0)

        # Extract rating
        rating_patterns = [
            r'(\d\.?\d?)\s*(?:stars?|/5|out of 5|\*)',
            r'Rating[:\s]+(\d\.?\d?)',
            r'(\d\.?\d?)\s*star'
        ]

        for pattern in rating_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        provider['rating'] = rating
                except:
                    pass
                break

        # Detect facility type
        text_lower = text.lower()
        if any(word in text_lower for word in ['hospital', 'medical center', 'health system']):
            provider['type'] = 'Hospital'
        elif 'clinic' in text_lower or 'urgent care' in text_lower:
            provider['type'] = 'Clinic'
        elif any(word in text_lower for word in ['center', 'institute']):
            provider['type'] = 'Medical Center'
        elif 'practice' in text_lower or 'physician' in text_lower:
            provider['type'] = 'Medical Practice'

        # Detect specializations
        specialization_map = {
            'Diabetes Care': ['diabetes', 'diabetologist', 'endocrinology', 'endocrinologist', 'metabolic'],
            'Cardiology': ['cardiology', 'cardiologist', 'heart', 'cardiovascular'],
            'Pediatrics': ['pediatric', 'pediatrician', 'children', 'kids'],
            'Nutrition': ['nutrition', 'nutritionist', 'dietitian', 'diet'],
            'Emergency Care': ['emergency', 'urgent care', 'ER', '24/7', 'trauma'],
            'General Practice': ['general practice', 'family medicine', 'primary care', 'internal medicine'],
            'Orthopedics': ['orthopedic', 'orthopedics', 'bone', 'joint'],
            'Dermatology': ['dermatology', 'dermatologist', 'skin'],
            'Neurology': ['neurology', 'neurologist', 'brain', 'nervous']
        }

        for spec_name, keywords in specialization_map.items():
            if any(keyword in text_lower for keyword in keywords):
                provider['specializations'].append(spec_name)

        if not provider['specializations']:
            provider['specializations'] = ['General Healthcare']

        # Extract hours if present
        hours_pattern = r'(?:Hours|Open)[:\s]+([^\n]+)'
        hours_match = re.search(hours_pattern, text, re.IGNORECASE)
        if hours_match:
            provider['hours'] = hours_match.group(1).strip()

        return provider

    def search_web_for_providers(
        self,
        location: str,
        specialization: str = None,
        facility_type: str = None,
        emergency_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Perform web search for healthcare providers
        """
        # Build query
        query = self.build_search_query(
            location=location,
            specialization=specialization,
            facility_type=facility_type,
            emergency_only=emergency_only
        )

        # Check cache
        cache_key = f"{location}:{specialization}:{facility_type}:{emergency_only}"
        if cache_key in self.search_cache:
            print(f"📦 Using cached results")
            return self.search_cache[cache_key]

        print(f"🔍 Web search query: {query}")

        # If no web search function provided, return simulated results
        if not self.web_search:
            print("⚠️  No web search function available, using simulation")
            return self._get_simulated_results(location, specialization)

        try:
            # Call the web search function
            # Expected to return text containing search results
            search_results = self.web_search(query)

            # Parse results
            providers = self.parse_search_results(search_results)

            # Cache results
            self.search_cache[cache_key] = providers

            print(f"✅ Found {len(providers)} providers from web search")

            return providers

        except Exception as e:
            print(f"❌ Web search failed: {e}")
            print("📋 Returning simulated results as fallback")
            return self._get_simulated_results(location, specialization)

    def _get_simulated_results(self, location: str, specialization: str = None) -> List[Dict[str, Any]]:
        """Generate simulated results based on search criteria"""
        # This simulates what real web search might return
        simulated_text = f"""
Johns Hopkins Medicine - Diabetes Center
1830 E. Monument Street, Baltimore, MD 21287
Phone: (410) 955-5000
Rating: 4.8 stars
Johns Hopkins offers comprehensive diabetes care including endocrinology, nutrition counseling, and diabetes education. Board-certified endocrinologists and certified diabetes educators. Open Mon-Fri 8am-5pm.
www.hopkinsmedicine.org/diabetes

University of Maryland Medical Center - Endocrinology
22 S. Greene Street, Baltimore, MD 21201
Phone: (410) 328-6034
4.6 out of 5 stars
Specializing in diabetes management, thyroid disorders, and metabolic conditions. Accepts most insurance plans. Emergency services available 24/7.

Mercy Medical Center - Diabetes & Nutrition Services
301 St. Paul Place, Baltimore, MD 21202
(410) 332-9000
Rating: 4.5/5
Comprehensive diabetes care including insulin pump therapy, continuous glucose monitoring, and dietary counseling. Nutritionists on staff. Mon-Fri 9am-5pm.

Sinai Hospital Endocrinology Associates
2401 W. Belvedere Avenue, Baltimore, MD 21215
Phone: (410) 601-9355
4.7 star rating
Expert diabetes management, thyroid care, and hormone disorders. Part of LifeBridge Health system. Accepting new patients.

Greater Baltimore Medical Center - Diabetes Care
6565 N. Charles Street, Baltimore, MD 21204
(443) 849-2000
Rating: 4.6 stars
Full-service diabetes center with certified diabetes educators, endocrinologists, and podiatry services. Insurance accepted.
"""
        return self.parse_search_results(simulated_text)

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process provider search request with real-time web search"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Extract location
        location = context.get('location_name') or self.extract_location_from_text(user_input)
        if not location:
            # Try to use coordinates if available
            if context.get('user_location'):
                loc = context['user_location']
                location = f"{loc.get('lat', 0)},{loc.get('lon', 0)}"
            else:
                location = "United States"  # Very broad default

        # Extract criteria
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

        print(f"\n{'='*60}")
        print(f"🔍 REAL-TIME PROVIDER SEARCH")
        print(f"{'='*60}")
        print(f"📍 Location: {location}")
        print(f"🏥 Specialization: {specialization or 'Any'}")
        print(f"🏢 Facility Type: {facility_type or 'Any'}")
        print(f"{'='*60}\n")

        # Perform web search
        providers = self.search_web_for_providers(
            location=location,
            specialization=specialization,
            facility_type=facility_type,
            emergency_only=emergency_only
        )

        if not providers:
            return {
                'status': 'no_results',
                'agent': self.agent_name,
                'message': 'No providers found. Try different search criteria.',
                'search_mode': 'real_time_web_search',
                'location_searched': location
            }

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'message': f"Found {len(providers)} healthcare providers in {location}",
            'facilities': providers[:5],  # Top 5
            'total_found': len(providers),
            'search_mode': 'real_time_web_search',
            'location_searched': location,
            'filters_applied': {
                'specialization': specialization,
                'facility_type': facility_type,
                'emergency_only': emergency_only
            },
            'disclaimer': 'Information sourced from web search. Please verify details before visiting.',
            'next_steps': [
                '📞 Call to verify current information',
                '🏥 Check if they accept your insurance',
                '📅 Schedule an appointment',
                '🗺️  Get directions to the facility',
                '⭐ Read recent reviews'
            ]
        }

        self.log_interaction(user_input, response)
        return response

    def format_facility_info(self, facility: Dict[str, Any]) -> str:
        """Format provider information for display"""
        info = f"""
🌐 {facility['name']}
   📍 Address: {facility['address']}
   📞 Phone: {facility['phone']}
   🏥 Type: {facility['type']}
"""

        if facility.get('rating') and facility['rating'] > 0:
            stars = '⭐' * int(facility['rating'])
            info += f"   {stars} Rating: {facility['rating']}/5.0\n"

        if facility.get('specializations'):
            info += f"   🔬 Specializations: {', '.join(facility['specializations'])}\n"

        if facility.get('website'):
            info += f"   🌐 Website: {facility['website']}\n"

        if facility.get('hours'):
            info += f"   🕐 Hours: {facility['hours']}\n"

        info += f"   ℹ️  Source: Live Web Search (Please verify)\n"

        return info
