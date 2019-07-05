from django.test import TestCase
from django.contrib.auth.models import User

from judging.models import Judge

# Judge Model Tests
class JudgeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("username", "email@email.com", 'password')
        self.judge = Judge.objects.create(user = user,
                                          first_name = "First",
                                          last_name = "Last",
                                          email = "email@email.com",
                                          organization = "Organization",
                                          job_title = "Boss"
                                          )

    def test_boolean_defaults(self):
        self.assertEqual(self.judge.sponsor_judge, False)
        self.assertEqual(self.judge.checked_in, False)
        self.assertEqual(self.judge.active, True)

    def test_name(self):
        self.assertEqual(self.judge.name(), "First Last")

    def test_username(self):
        self.assertEqual(self.judge.username(), "username")

    def test_str(self):
        self.assertEqual(self.judge.__str__(), "First Last")
