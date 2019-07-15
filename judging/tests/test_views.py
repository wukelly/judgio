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


# judge_upload_view tests
class JudgeUploadViewTestCase(TestCase):
    def test_post_request_not_admin(self):
        # given
        c = Client()

        # when
        response = c.post('/admin/judge/judge-upload/')

        # then
        self.assertEqual(response.status_code, 302)

    def test_post_request_empty_admin(self):
        # given
        admin = User.objects.create_superuser(username='admin', email="admin@admin.com", password="password")
        admin.set_password('password')
        admin.save()
        c = Client()
        c.login(username='admin', password='password')

        # when
        judge_info = {'judge_info': ['[]']}
        response = c.post('/admin/judge/judge-upload/', judge_info)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Judge.objects.all()), 0)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertTrue(admin in User.objects.all())

    def test_post_request_single_admin(self):
        # given
        admin = User.objects.create_superuser(username='admin', email="admin@admin.com", password="password")
        admin.set_password('password')
        admin.save()
        c = Client()
        c.login(username='admin', password='password')

        # when
        judge_info = {'judge_info': ['[["test1","judge1","test1judge1@gmail.com","fake org 1","cool guy","TRUE",""]]']}
        response = c.post('/admin/judge/judge-upload/', judge_info)

        # then
        self.assertEqual(response.status_code, 200)

        judge = Judge.objects.get(first_name="test1")
        self.assertEqual(judge.last_name, 'judge1')
        self.assertEqual(judge.email, 'test1judge1@gmail.com')
        self.assertEqual(judge.organization, 'fake org 1')
        self.assertEqual(judge.job_title, 'cool guy')
        self.assertEqual(judge.sponsor_judge, True)
        self.assertEqual(judge.checked_in, False)
        self.assertEqual(judge.active, True)
        self.assertEqual(judge.user.username, 'test1judge1')

    def test_post_request_invalid_form_admin(self):
        # given
        admin = User.objects.create_superuser(username='admin', email="admin@admin.com", password="password")
        admin.set_password('password')
        admin.save()
        c = Client()
        c.login(username='admin', password='password')

        # when
        judge_info = {'judge_info': ['[["test1","judge1","not an email","fake org 1","cool guy","TRUE",""]]']}
        response = c.post('/admin/judge/judge-upload/', judge_info)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Judge.objects.all()), 0)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertTrue(admin in User.objects.all())

    def test_get_request_not_admin(self):
        # given
        c = Client()

        # when
        response = c.get(path='/admin/judge/judge-upload/')

        # then
        self.assertEqual(response.status_code, 302)

    def test_get_request_admin(self):
        # given
        admin = User.objects.create_superuser(username='admin', email="admin@admin.com", password="password")
        admin.set_password('password')
        admin.save()
        c = Client()
        c.login(username='admin', password='password')

        # when
        response = c.get(path='/admin/judge/judge-upload/')

        # then
        self.assertEqual(response.status_code, 200)

