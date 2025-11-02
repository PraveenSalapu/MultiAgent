"""
Appointment Scheduler Agent
Manages healthcare appointment scheduling
"""

from typing import Dict, Any, List
from .base_agent import BaseHealthcareAgent
from datetime import datetime, timedelta
import json
import re


class AppointmentSchedulerAgent(BaseHealthcareAgent):
    """
    Agent specialized in scheduling and managing healthcare appointments
    """

    def __init__(self):
        super().__init__(
            agent_name="Appointment Scheduler",
            capabilities=["appointment_scheduling", "appointment_management", "availability_check"]
        )
        self.appointments = []
        self.providers = self._load_sample_providers()

    def _load_sample_providers(self) -> List[Dict[str, Any]]:
        """Load sample healthcare providers"""
        return [
            {
                'id': 'P001',
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Endocrinologist',
                'location': 'City Medical Center',
                'available_days': ['Monday', 'Wednesday', 'Friday'],
                'time_slots': ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
            },
            {
                'id': 'P002',
                'name': 'Dr. Michael Chen',
                'specialization': 'General Practitioner',
                'location': 'Downtown Health Clinic',
                'available_days': ['Tuesday', 'Thursday', 'Friday'],
                'time_slots': ['08:00', '09:00', '10:00', '13:00', '14:00', '15:00']
            },
            {
                'id': 'P003',
                'name': 'Dr. Emily Rodriguez',
                'specialization': 'Diabetologist',
                'location': 'Specialty Diabetes Care Center',
                'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
                'time_slots': ['09:00', '10:30', '13:00', '14:30', '16:00']
            },
            {
                'id': 'P004',
                'name': 'Dr. James Williams',
                'specialization': 'Nutritionist',
                'location': 'Wellness Healthcare Hub',
                'available_days': ['Monday', 'Wednesday', 'Friday'],
                'time_slots': ['10:00', '11:00', '14:00', '15:00', '16:00']
            }
        ]

    def find_available_slots(self, specialization: str = None, days_ahead: int = 14) -> List[Dict[str, Any]]:
        """Find available appointment slots"""
        available_slots = []

        # Filter providers by specialization if specified
        providers = self.providers
        if specialization:
            providers = [p for p in providers if specialization.lower() in p['specialization'].lower()]

        # Generate slots for next N days
        today = datetime.now()

        for provider in providers:
            for day_offset in range(1, days_ahead + 1):
                check_date = today + timedelta(days=day_offset)
                day_name = check_date.strftime('%A')

                if day_name in provider['available_days']:
                    for time_slot in provider['time_slots']:
                        slot_datetime = datetime.strptime(
                            f"{check_date.strftime('%Y-%m-%d')} {time_slot}",
                            '%Y-%m-%d %H:%M'
                        )

                        # Check if slot is not already booked
                        is_booked = any(
                            apt['provider_id'] == provider['id'] and
                            apt['datetime'] == slot_datetime.isoformat()
                            for apt in self.appointments
                        )

                        if not is_booked:
                            available_slots.append({
                                'provider': provider['name'],
                                'provider_id': provider['id'],
                                'specialization': provider['specialization'],
                                'location': provider['location'],
                                'date': check_date.strftime('%Y-%m-%d'),
                                'day': day_name,
                                'time': time_slot,
                                'datetime': slot_datetime.isoformat()
                            })

        return sorted(available_slots, key=lambda x: x['datetime'])[:10]  # Return next 10 slots

    def book_appointment(self, slot: Dict[str, Any], patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """Book an appointment"""
        appointment_id = f"APT{len(self.appointments) + 1:04d}"

        appointment = {
            'appointment_id': appointment_id,
            'provider_id': slot['provider_id'],
            'provider_name': slot['provider'],
            'patient_name': patient_info.get('name', 'Patient'),
            'patient_contact': patient_info.get('contact', ''),
            'date': slot['date'],
            'time': slot['time'],
            'datetime': slot['datetime'],
            'location': slot['location'],
            'specialization': slot['specialization'],
            'status': 'confirmed',
            'booked_at': datetime.now().isoformat()
        }

        self.appointments.append(appointment)

        return {
            'status': 'success',
            'appointment': appointment,
            'confirmation_message': f"Appointment booked successfully! Confirmation ID: {appointment_id}"
        }

    def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """Cancel an appointment"""
        for apt in self.appointments:
            if apt['appointment_id'] == appointment_id:
                apt['status'] = 'cancelled'
                return {
                    'status': 'success',
                    'message': f"Appointment {appointment_id} has been cancelled",
                    'appointment': apt
                }

        return {
            'status': 'error',
            'message': f"Appointment {appointment_id} not found"
        }

    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process appointment scheduling request"""
        if context is None:
            context = {}

        user_lower = user_input.lower()

        # Check for cancellation request
        if 'cancel' in user_lower:
            apt_id_match = re.search(r'apt\d{4}', user_input, re.IGNORECASE)
            if apt_id_match:
                return self.cancel_appointment(apt_id_match.group(0).upper())
            else:
                return {
                    'status': 'error',
                    'message': 'Please provide appointment ID to cancel (e.g., APT0001)'
                }

        # Determine specialization needed
        specialization = None
        if any(word in user_lower for word in ['diabetes', 'diabetologist', 'endocrinologist']):
            specialization = 'Diabetologist'
        elif any(word in user_lower for word in ['diet', 'nutrition', 'nutritionist']):
            specialization = 'Nutritionist'
        elif any(word in user_lower for word in ['general', 'checkup', 'gp']):
            specialization = 'General Practitioner'

        # Get available slots
        available_slots = self.find_available_slots(specialization)

        if not available_slots:
            return {
                'status': 'no_availability',
                'message': 'No available slots found for the requested specialization',
                'suggestion': 'Try a different specialization or extend the search period'
            }

        response = {
            'status': 'success',
            'agent': self.agent_name,
            'message': f"Found {len(available_slots)} available appointment slots",
            'available_slots': available_slots[:5],  # Show top 5
            'specialization_filter': specialization,
            'next_steps': [
                'Select a slot from the available options',
                'Provide patient name and contact information',
                'Confirm the appointment booking'
            ]
        }

        # If context has booking confirmation, process the booking
        if context.get('confirm_booking') and context.get('selected_slot'):
            booking_result = self.book_appointment(
                context['selected_slot'],
                context.get('patient_info', {})
            )
            response.update(booking_result)

        self.log_interaction(user_input, response)

        return response

    def get_upcoming_appointments(self, patient_name: str = None) -> List[Dict[str, Any]]:
        """Get list of upcoming appointments"""
        now = datetime.now()
        upcoming = [
            apt for apt in self.appointments
            if apt['status'] == 'confirmed' and
               datetime.fromisoformat(apt['datetime']) > now
        ]

        if patient_name:
            upcoming = [apt for apt in upcoming if apt['patient_name'] == patient_name]

        return sorted(upcoming, key=lambda x: x['datetime'])
