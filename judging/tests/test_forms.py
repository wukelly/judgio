from django.test import TestCase
from django.contrib.auth.models import User

from judging.models import Judge
from judging.forms import JudgeForm

# JudgeForm Tests
class JudgeFormTestCase(TestCase):
    def test_judge_form_valid(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': True})

        # then
        self.assertTrue(form.is_valid())

    def test_judge_form_valid_with_defaults(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot'})

        self.assertTrue(form.is_valid())

    def test_judge_form_invalid(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': True})

        # then
        self.assertFalse(form.is_valid())

    def test_judge_form_invalid_email(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu',
                               'organization': 'OSU',
                               'job_title': 'Mascot'})

        # then
        self.assertFalse(form.is_valid())

    def test_generate_username(self):
        # given
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

        # when
        name = JudgeForm().generate_username(judge)

        # then
        self.assertEqual(name, "first-namelast")

    def test_save_new(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': False})

        # when
        judge = form.save()

        # then
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
        self.assertTrue(judge in Judge.objects.all())

    def test_save_commit_false(self):
        # given
        form = JudgeForm(data={'first_name': 'Brutus',
                               'last_name': 'Buckeye',
                               'email': 'buckeye.1@osu.edu',
                               'organization': 'OSU',
                               'job_title': 'Mascot',
                               'sponsor_judge': True,
                               'checked_in': True,
                               'active': False})

        judge = form.save(commit=False)

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
        self.assertFalse(judge in Judge.objects.all())
