from django.test import TestCase
from ehr.models import Patient, MedicalProfessional, Appointment, MedicalHistory, VitalSigns, LabResult, MedicalImage
import asyncio

class EHRModelsTestCase(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            gender='Male',
            contact_number='1234567890',
            email_address='john@example.com',
            address='123 Main St',
            insurance_provider='ABC Insurance',
            insurance_policy_number='1234567890'
        )

        self.medical_professional = MedicalProfessional.objects.create(
            first_name='Dr. Jane',
            last_name='Smith',
            specialization='Cardiology',
            contact_number='9876543210',
            email_address='jane@example.com'
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            medical_professional=self.medical_professional,
            date='2023-06-05',
            time='10:00',
            purpose='General check-up'
        )

        self.medical_history = MedicalHistory.objects.create(
            patient=self.patient,
            diagnosis='Cold',
            allergies='None',
            chronic_conditions='None'
        )

        self.vital_signs = VitalSigns.objects.create(
            patient=self.patient,
            date='2023-06-05',
            time='10:00',
            blood_pressure='120/80',
            heart_rate=80,
            temperature='98.6',
            weight='70.5'
        )

        self.lab_result = LabResult.objects.create(
            patient=self.patient,
            test_name='Blood Test',
            test_result='Normal',
            date='2023-06-05',
            lab_technician='John Smith'
        )

        self.medical_image = MedicalImage.objects.create(
            patient=self.patient,
            image='path/to/image.jpg',
            description='X-ray of the chest',
            date='2023-06-05',
            uploaded_by='Jane Doe'
        )

    async def run_tests_async(self):
        await self.test_patient_model()
        await self.test_medical_professional_model()
        await self.test_appointment_model()
        await self.test_medical_history_model()
        await self.test_vital_signs_model()
        await self.test_lab_result_model()
        await self.test_medical_image_model()

    async def test_patient_model(self):
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(str(self.patient), 'John Doe')
        print('Patient model test passed')

    async def test_medical_professional_model(self):
        self.assertEqual(self.medical_professional.first_name, 'Dr. Jane')
        self.assertEqual(self.medical_professional.last_name, 'Smith')
        self.assertEqual(str(self.medical_professional), 'Dr. Jane Smith')
        print('MedicalProfessional model test passed')

    async def test_appointment_model(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.medical_professional, self.medical_professional)
        self.assertEqual(str(self.appointment), 'Appointment for John Doe on 2023-06-05 at 10:00')
        print('Appointment model test passed')

    async def test_medical_history_model(self):
        self.assertEqual(self.medical_history.patient, self.patient)
        self.assertEqual(self.medical_history.diagnosis, 'Cold')
        self.assertEqual(str(self.medical_history), 'Medical History for John Doe')
        print('MedicalHistory model test passed')

    async def test_vital_signs_model(self):
        self.assertEqual(self.vital_signs.patient, self.patient)
        self.assertEqual(self.vital_signs.date, '2023-06-05')
        self.assertEqual(str(self.vital_signs), 'Vital Signs for John Doe on 2023-06-05 at 10:00')
        print('VitalSigns model test passed')

    async def test_lab_result_model(self):
        self.assertEqual(self.lab_result.patient, self.patient)
        self.assertEqual(self.lab_result.test_name, 'Blood Test')
        self.assertEqual(str(self.lab_result), 'Lab Result for John Doe - Blood Test')
        print('LabResult model test passed')

    async def test_medical_image_model(self):
        self.assertEqual(self.medical_image.patient, self.patient)
        self.assertEqual(self.medical_image.description, 'X-ray of the chest')
        self.assertEqual(str(self.medical_image), 'Medical Image for John Doe - 2023-06-05')
        print('MedicalImage model test passed')

    def test_models(self):
        loop = asyncio.get_event_loop()
        tasks = asyncio.ensure_future(self.run_tests_async())
        loop.run_until_complete(tasks)

    def test_all_models(self):
        self.test_models()

    def tearDown(self):
        self.patient.delete()
        self.medical_professional.delete()
        self.appointment.delete()
        self.medical_history.delete()
        self.vital_signs.delete()
        self.lab_result.delete()
        self.medical_image.delete()


if __name__ == '__main__':
    tests = EHRModelsTestCase()
    total_tests = 7
    tests.test_all_models()
    print(f"\n{total_tests} tests completed.")    
