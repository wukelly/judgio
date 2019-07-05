from django.test import TestCase
from django.contrib.auth.models import User

from judging.models import Judge
from judging.forms import JudgeForm

# JudgeForm Tests
class JudgeFormTestCase(TestCase):
    def test_judge_form_valid(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': True})

        self.assertTrue(form.is_valid())

    def test_judge_form_valid_with_defaults(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot'})

        self.assertTrue(form.is_valid())

    def test_judge_form_invalid(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': True})

        self.assertFalse(form.is_valid())

    def test_judge_form_invalid_email(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu',
                               'organization': 'OSU',
                               'job_title': 'Mascot'})

        self.assertFalse(form.is_valid())

    def test_generate_username(self):
        user = User.objects.create_user("username", "email@email.com", 'password')
        judge = Judge.objects.create(user = user,
                                     first_name = "First-Name",
                                     last_name = "Last",
                                     email = "email@email.com",
                                     organization = "Organization",
                                     job_title = "Boss",
                                     sponsor_judge = True,
                                     checked_in = True,
                                     active = False
                                     )

        name = JudgeForm().generate_username(judge)

        self.assertEqual(name, "first-namelast")

    def test_save(self):
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': False})

        judge = form.save()

        self.assertEqual(judge.user.username, 'brutusbuckeye')
        self.assertEqual(judge.user.email, 'buckeye.1@osu.edu')
        self.assertTrue(judge.user.check_password('password'))
        self.assertEqual(judge.first_name, 'Brutus')
        self.assertEqual(judge.last_name, 'Buckeye')
        self.assertEqual(judge.email, 'buckeye.1@osu.edu')
        self.assertEqual(judge.organization, 'OSU')
        self.assertEqual(judge.job_title, 'Mascot')
        self.assertTrue(judge.sponsor_judge)
        self.assertTrue(judge.checked_in)
        self.assertFalse(judge.active)
