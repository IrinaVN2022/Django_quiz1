from accounts.views import UserLoginView
from accounts.views import UserLogoutView
from accounts.views import UserProfileUpdateView
from accounts.views import UserReactivationView
from accounts.views import UserRegisterView
from accounts.views import user_activate
from accounts.views import user_profile_view

from django.test import SimpleTestCase
from django.urls import resolve
from django.urls import reverse
from django.views.generic import TemplateView


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)
        # assert resolve(url).func.view_class == UserRegisterView, 'rweqgfqfewf'

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, user_profile_view)

    def test_activate_user_url_resolves(self):
        url = reverse('accounts:register_activate', kwargs={'sign': 'ioewutrljc3409ur90u43ri3j4'})
        self.assertEqual(resolve(url).func, user_activate)

    def test_register_done_url_resolve(self):
        url = reverse('accounts:register_done')
        self.assertIs(TemplateView, resolve(url).func.view_class)

    def test_reactivation_url_resolve(self):
        url = reverse('accounts:reactivation')
        self.assertIs(UserReactivationView, resolve(url).func.view_class)

    def test_reactivation_done_url_resolve(self):
        url = reverse('accounts:reactivation_done')
        self.assertIs(TemplateView, resolve(url).func.view_class)

    def test_login_url_resolve(self):
        url = reverse('accounts:login')
        self.assertIs(UserLoginView, resolve(url).func.view_class)

    def test_logout_url_resolve(self):
        url = reverse('accounts:logout')
        self.assertIs(UserLogoutView, resolve(url).func.view_class)

    def test_profile_url_resolve(self):
        url = reverse('accounts:profile')
        self.assertIs(user_profile_view, resolve(url).func)

    def test_profile_update_url_resolve(self):
        url = reverse('accounts:profile_update')
        self.assertIs(UserProfileUpdateView, resolve(url).func.view_class)
