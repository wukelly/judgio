from django.test import TestCase
from django.contrib.auth.models import User

from .models import Judge

# Judge Model Tests
class JudgeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("username", "email@email.com", 'password')
        Judge.objects.create(user = user,
                             first_name = "First",
                             last_name = "Last",
                             email = "email@email.com",
                             organization = "Organization",
                             job_title = "Boss"
                             )

    def test_boolean_defaults(self):
        judge = Judge.objects.get(user=1)

        self.assertEqual(judge.sponsor_judge, False)
        self.assertEqual(judge.checked_in, False)
        self.assertEqual(judge.active, True)

    def test_name(self):
        judge = Judge.objects.get(user=1)
        self.assertEqual(judge.name(), "First Last")

    def test_username(self):
        judge = Judge.objects.get(user=1)
        self.assertEqual(judge.username(), "username")

    def test_str(self):
        judge = Judge.objects.get(user=1)
        self.assertEqual(judge.__str__(), "First Last")
