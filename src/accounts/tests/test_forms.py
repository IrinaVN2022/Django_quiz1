from accounts.forms import UserReactivationForm, UserRegisterForm, UserUpdateForm
from accounts.models import User
from accounts.validators import validate_email_exist

from django.forms import DateField
from django.forms import DateInput
from django.forms import EmailField
from django.test import TestCase


class TestForms(TestCase):
    def setUp(self):
        self.username = 'user_1'
        self.password = '123qwe!@#'
        self.email = 'user_1@test.com'

    def test_register_form_valid_data(self):
        form = UserRegisterForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            }
        )

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestUserUpdateForm(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user',
            'email': 'user@test.com',
        }
        self.not_required_data = {
            'firs_name': 'user_first_name',
            'last_name': 'user_last_name',
            'city': 'Odesa',
        }
        self.form = UserUpdateForm

    def test_birthday_field(self):
        form = self.form(self.data)
        field = form.fields['birthday']
        self.assertIsInstance(field, DateField)
        self.assertFalse(field.required)
        self.assertIsInstance(field.widget, DateInput)

    def test_email_field(self):
        form = self.form(self.data)
        field = form.fields['email']
        self.assertIsInstance(field, EmailField)
        self.assertTrue(field.required)

    def test_form_valid_data(self):
        # required data
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

        # full data
        self.data.update(self.not_required_data)
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # no data
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))

        # not required data
        form = self.form(data=self.not_required_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))


class TestReactivationForm(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'user@test.com',
        }

        User.objects.create(
            username='user',
            password='123qwe!@#',
            email=self.data['email']
        )

        self.form = UserReactivationForm

    def test_email_field(self):
        form = self.form(data=self.data)
        field = form.fields['email']
        self.assertIsInstance(field, EmailField)
        self.assertTrue(field.required)
        self.assertIn(validate_email_exist, field.validators)

    def test_valid_email(self):
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = self.form(data={'email': '1test@te.cm'})
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test_clear_email_of_exist_user(self):
        form = self.form(data=self.data)
        form.is_valid()
        self.assertEqual(self.data['email'], form.clean_email())

    def test_clear_email_of_not_exist_user(self):
        form = self.form(data={'email': 'not_exist_user@test.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
