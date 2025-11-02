"""
Healthcare Provider Locator Agent
Finds nearby healthcare providers and facilities
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent
import math


class HealthcareProviderLocator(BaseHealthcareAgent):
    """
    Agent specialized in locating nearby healthcare providers and facilities
    """

    def __init__(self):
        super().__init__(
            agent_name="Healthcare Provider Locator",
            capabilities=["find_providers", "locate_facilities", "get_directions"]
        )
        self.healthcare_facilities = self._load_sample_facilities()

    def _load_sample_facilities(self) -> List[Dict[str, Any]]:
        """Load sample healthcare facilities database"""
        return [
            {
                'id': 'F001',
                'name': 'City Medical Center',
                'type': 'Hospital',
                'address': '123 Main Street, Downtown',
                'coordinates': {'lat': 40.7128, 'lon': -74.0060},
                'specializations': ['General Medicine', 'Emergency Care', 'Surgery', 'Endocrinology'],
                'phone': '(555) 123-4567',
                'rating': 4.5,
                'accepts_insurance': True,
                'emergency_services': True
            },
            {
                'id': 'F002',
                'name': 'Downtown Health Clinic',
                'type': 'Clinic',
                'address': '456 Oak Avenue, Downtown',
                'coordinates': {'lat': 40.7138, 'lon': -74.0070},
                'specializations': ['General Practice', 'Pediatrics', 'Family Medicine'],
                'phone': '(555) 234-5678',
                'rating': 4.3,
                'accepts_insurance': True,
                'emergency_services': False
            },
            {
                'id': 'F003',
                'name': 'Specialty Diabetes Care Center',
                'type': 'Specialty Center',
                'address': '789 Elm Street, Midtown',
                'coordinates': {'lat': 40.7158, 'lon': -74.0050},
                'specializations': ['Diabetology', 'Endocrinology', 'Nutrition Counseling'],
                'phone': '(555) 345-6789',
                'rating': 4.8,
                'accepts_insurance': True,
                'emergency_services': False
            },
            {
                'id': 'F004',
                'name': 'Wellness Healthcare Hub',
                'type': 'Wellness Center',
                'address': '321 Pine Road, Westside',
                'coordinates': {'lat': 40.7108, 'lon': -74.0090},
                'specializations': ['Nutrition', 'Physical Therapy', 'Preventive Care'],
                'phone': '(555) 456-7890',
                'rating': 4.6,
                'accepts_insurance': True,
                'emergency_services': False
            },
            {
                'id': 'F005',
                'name': 'Northside Community Hospital',
                'type': 'Hospital',
                'address': '654 Maple Drive, Northside',
                'coordinates': {'lat': 40.7178, 'lon': -74.0040},
                'specializations': ['Emergency Care', 'Internal Medicine', 'Cardiology', 'Diabetes Care'],
                'phone': '(555) 567-8901',
                'rating': 4.4,
                'accepts_insurance': True,
                'emergency_services': True
            },
            {
                'id': 'F006',
                'name': 'Sunrise Medical Plaza',
                'type': 'Medical Plaza',
                'address': '987 Cedar Lane, Eastside',
                'coordinates': {'lat': 40.7118, 'lon': -74.0030},
                'specializations': ['General Practice', 'Dermatology', 'Orthopedics'],
                'phone': '(555) 678-9012',
                'rating': 4.2,
                'accepts_insurance': True,
                'emergency_services': False
            }
        ]

    def calculate_distance(self, coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in miles
        """
        R = 3959  # Earth's radius in miles

        lat1, lon1 = math.radians(coord1['lat']), math.radians(coord1['lon'])
        lat2, lon2 = math.radians(coord2['lat']), math.radians(coord2['lon'])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def find_nearby_facilities(
        self,
        user_location: Dict[str, float] = None,
        specialization: str = None,
        facility_type: str = None,
        max_distance: float = 10.0,
        emergency_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Find nearby healthcare facilities based on criteria"""

        # Default location if not provided (Downtown)
        if user_location is None:
            user_location = {'lat': 40.7128, 'lon': -74.0060}

        results = []

        for facility in self.healthcare_facilities:
            # Apply filters
            if emergency_only and not facility['emergency_services']:
                continue

            if facility_type and facility['type'].lower() != facility_type.lower():
                continue

            if specialization:
                spec_match = any(
                    specialization.lower() in spec.lower()
                    for spec in facility['specializations']
                )
                if not spec_match:
                    continue

            # Calculate distance
            distance = self.calculate_distance(user_location, facility['coordinates'])

            if distance <= max_distance:
                result = facility.copy()
                result['distance'] = round(distance, 2)
                results.append(result)

        # Sort by distance
        results.sort(key=lambda x: x['distance'])

        return results

    def get_facility_details(self, facility_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific facility"""
        for facility in self.healthcare_facilities:
            if facility['id'] == facility_id:
                return facility

        return None

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process healthcare provider location request"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Extract search criteria
        specialization = None
        facility_type = None
        emergency_only = False

        # Determine specialization
        if any(word in user_lower for word in ['diabetes', 'diabetologist', 'endocrinologist']):
            specialization = 'Diabetes'
        elif any(word in user_lower for word in ['nutrition', 'dietician', 'nutritionist']):
            specialization = 'Nutrition'
        elif any(word in user_lower for word in ['emergency', 'urgent']):
            emergency_only = True

        # Determine facility type
        if 'hospital' in user_lower:
            facility_type = 'Hospital'
        elif 'clinic' in user_lower:
            facility_type = 'Clinic'

        # Get user location from context
        user_location = context.get('user_location')

        # Find nearby facilities
        nearby_facilities = self.find_nearby_facilities(
            user_location=user_location,
            specialization=specialization,
            facility_type=facility_type,
            emergency_only=emergency_only
        )

        if not nearby_facilities:
            return {
                'status': 'no_results',
                'message': 'No healthcare facilities found matching your criteria',
                'suggestion': 'Try expanding search radius or removing some filters'
            }

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'message': f"Found {len(nearby_facilities)} nearby healthcare facilities",
            'facilities': nearby_facilities[:5],  # Top 5 nearest
            'filters_applied': {
                'specialization': specialization,
                'facility_type': facility_type,
                'emergency_only': emergency_only
            },
            'next_steps': [
                'Select a facility to view more details',
                'Get directions to the facility',
                'Schedule an appointment'
            ]
        }

        self.log_interaction(user_input, response)

        return response

    def format_facility_info(self, facility: Dict[str, Any]) -> str:
        """Format facility information for display"""
        info = f"""
📍 {facility['name']}
   Type: {facility['type']}
   Distance: {facility.get('distance', 'N/A')} miles
   Address: {facility['address']}
   Phone: {facility['phone']}
   Rating: {'⭐' * int(facility['rating'])} ({facility['rating']}/5.0)

   Specializations: {', '.join(facility['specializations'])}
   Emergency Services: {'✓ Yes' if facility['emergency_services'] else '✗ No'}
   Insurance Accepted: {'✓ Yes' if facility['accepts_insurance'] else '✗ No'}
"""
        return info
