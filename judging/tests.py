from django.test import TestCase
from django.contrib.auth.models import User

from .models import Judge
from .forms import JudgeForm

# JudgeForm Tests
class JudgeFormTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("username", "email@email.com", 'password')
        self.judge = Judge.objects.create(user = user,
                                         first_name = "First-Name",
                                         last_name = "Last",
                                         email = "email@email.com",
                                         organization = "Organization",
                                         job_title = "Boss"
                                         )
        self.form = JudgeForm()

    def test_JudgeForm_valid(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': True})

        self.assertTrue(form.is_valid())

    def test_JudgeForm_valid_with_defaults(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot'})

        self.assertTrue(form.is_valid())

    def test_JudgeForm_invalid(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                                 'last_name': 'Buckeye',
                                 'email': 'buckeye.1@osu.edu',
                                 'organization': 'OSU',
                                 'sponsor_judge': True,
                                 'checked_in': True,
                                 'active': True})

        self.assertFalse(form.is_valid())

    def test_JudgeForm_invalid_email(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                                'last_name': 'Buckeye',
                                'email': 'buckeye.1@osu',
                                'organization': 'OSU',
                                'job_title': 'Mascot'})

        self.assertFalse(form.is_valid())

    def test_generate_username(self):
        name = self.form.generate_username(self.judge)
        self.assertEqual(name, "first-namelast")

    # TODO: Test save

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
