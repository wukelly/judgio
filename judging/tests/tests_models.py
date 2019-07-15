from django.test import TestCase
from django.contrib.auth.models import User

from judging.models import Judge

# Judge and JudgeQuerySet Tests
class JudgeTestCase(TestCase):
    def setUp(self):
        # given
        user = User.objects.create_user("username", "email@email.com", 'password')
        self.judge = Judge.objects.create(user = user,
                                          first_name = "First",
                                          last_name = "Last",
                                          email = "email@email.com",
                                          organization = "Organization",
                                          job_title = "Boss"
                                          )

    def test_boolean_defaults(self):
        # then
        self.assertFalse(self.judge.sponsor_judge)
        self.assertFalse(self.judge.checked_in)
        self.assertTrue(self.judge.active)

    def test_name(self):
        # then
        self.assertEqual(self.judge.name(), "First Last")

    def test_username(self):
        # then
        self.assertEqual(self.judge.username(), "username")

    def test_str(self):
        # then
        self.assertEqual(self.judge.__str__(), "First Last")

    def test_delete(self):
        # when
        self.judge.delete()

        # then
        self.assertFalse(self.judge in Judge.objects.all())
        self.assertFalse(self.judge.user in User.objects.all())

    def test_delete_queryset(self):
        # when
        user = User.objects.create_user("username2", "email2@email.com", 'password2')
        judge = Judge.objects.create(user = user,
                                     first_name = "Last",
                                     last_name = "First",
                                     email = "email2@email.com",
                                     organization = "Department",
                                     job_title = "CEO")
        judges = Judge.objects.all()
        judges.delete()

        # then
        for judge in judges:
            self.assertFalse(judge in Judge.objects.all())
            self.assertFalse(judge.user in User.objects.all())
