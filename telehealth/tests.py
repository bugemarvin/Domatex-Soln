from datetime import timedelta
import logging
from django.test import TestCase
from django.utils import timezone
from telehealth.models import VideoConsultation, ChatInteraction, RemoteMonitoring
import asyncio

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class TelehealthModelsTestCase(TestCase):

    def setUp(self):
        self.video_consultation = VideoConsultation.objects.create(
            duration=timedelta(minutes=30),
            consultation_type='General',
            prescription='Take medication X',
            follow_up_date='2023-06-06',
            diagnosis='Common cold',
            recommendations='Rest and drink fluids'
        )

        self.chat_interaction = ChatInteraction.objects.create(
            video_consultation=self.video_consultation,
            message='Hello, how are you?',
            sent_datetime=timezone.now(),
            sender='John',
            attachments=None  # Set attachments explicitly to None
        )

        self.remote_monitoring = RemoteMonitoring.objects.create(
            sensor_type='Temperature',
            sensor_reading='37.2°C',
            reading_datetime=timezone.now(),
            sensor_location='Living Room',
            alert_threshold='38°C',
            alert_message=None
        )

    async def run_tests_async(self):
        await self.test_video_consultation_model()
        await self.test_chat_interaction_model()
        await self.test_remote_monitoring_model()

    async def test_video_consultation_model(self):
        self.assertEqual(self.video_consultation.duration, timedelta(minutes=30))
        self.assertEqual(self.video_consultation.consultation_type, 'General')
        self.assertEqual(str(self.video_consultation), 'Video Consultation - 1')
        print('VideoConsultation model test passed')

    async def test_chat_interaction_model(self):
        self.assertEqual(self.chat_interaction.video_consultation, self.video_consultation)
        self.assertEqual(self.chat_interaction.message, 'Hello, how are you?')
        self.assertIsNone(self.chat_interaction.attachments, "Attachments should be None")
        self.assertEqual(str(self.chat_interaction), 'Chat Interaction - 1')
        print('ChatInteraction model test passed')

    async def test_remote_monitoring_model(self):
        self.assertEqual(self.remote_monitoring.sensor_type, 'Temperature')
        self.assertEqual(self.remote_monitoring.sensor_reading, '37.2°C')
        self.assertEqual(str(self.remote_monitoring), 'Remote Monitoring - 1')
        print('RemoteMonitoring model test passed')

    def test_models(self):
        loop = asyncio.get_event_loop()
        tasks = asyncio.ensure_future(self.run_tests_async())
        loop.run_until_complete(tasks)

    def test_all_models(self):
        self.test_models()

    def tearDown(self):
        self.video_consultation.delete()
        self.chat_interaction.delete()
        self.remote_monitoring.delete()


if __name__ == '__main__':
    tests = TelehealthModelsTestCase()
    total_tests = 3
    tests.test_all_models()
    print(f"\n{total_tests} tests completed.")
