from django.test import TestCase, Client
from django.contrib.auth.models import AnonymousUser, User

from judging.models import Judge

# Home View Tests
class HomeTestCase(TestCase):
    def test_user_not_authenticated_view(self):
        # given
        c = Client()

        # when
        response = c.get('')

        # then
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['checked_in'])

    def test_user_authenticated_not_judge_view(self):
        # given
        user = User.objects.create_user("username")
        user.set_password('password')
        user.save()

        c = Client()
        c.login(username='username', password='password')

        # when
        response = c.get('')

        # then
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['checked_in'])

    def test_user_judge_not_checked_in_view(self):
        # given
        user = User.objects.create_user("username")
        user.set_password('password')
        user.save()
        Judge.objects.create(user = user,
                             first_name = "First",
                             last_name = "Last",
                             email = "email@email.com",
                             organization = "Organization",
                             job_title = "Boss",
                             checked_in = False,
                             )

        c = Client()
        c.login(username='username', password='password')

        # when
        response = c.get('')

        # then
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['checked_in'])

    def test_user_judge_checked_in_view(self):
        # given
        user = User.objects.create_user("username")
        user.set_password('password')
        user.save()
        Judge.objects.create(user = user,
                             first_name = "First",
                             last_name = "Last",
                             email = "email@email.com",
                             organization = "Organization",
                             job_title = "Boss",
                             checked_in = True,
                             )

        c = Client()
        c.login(username='username', password='password')

        # when
        response = c.get('')

        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['checked_in'])
        self.assertEqual(response.context['name'], "First Last")
