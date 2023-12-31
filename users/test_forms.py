from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm

class UserSignupFormTest(TestCase):
    def test_usersignupform_valid(self):
        # Test when form data is valid
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = UserSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_usersignupform_passwords_not_matching(self):
        # Test when passwords don't match
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "mismatchedpassword",
        }
        form = UserSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors.keys())
        self.assertEqual(form.errors["password2"][0], "The two password fields didn’t match.")

    def test_usersignupform_invalid_email(self):
        # Test when email is invalid
        form_data = {
            "username": "testuser",
            "email": "invalidemail",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = UserSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors.keys())
        self.assertEqual(form.errors["email"][0], "Enter a valid email address.")

    def test_usersignupform_missing_fields(self):
        # Test when required fields are missing
        form_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        form = UserSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors.keys())
        self.assertIn("email", form.errors.keys())
        self.assertIn("password1", form.errors.keys())
        self.assertIn("password2", form.errors.keys())

class UserUpdateFormTest(TestCase):
    def test_userupdateform_valid(self):
        # Test when form data is valid
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            
        }
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_userupdateform_invalid_email(self):
        # Test when email is invalid
        form_data = {
            "username": "testuser",
            "email": "incorrectemail",
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors.keys())
        self.assertEqual(form.errors["email"][0], "Enter a valid email address.")

    def test_userupdateform_missing_fields(self):
        # Test when required fields are missing
        form_data = {
            "username": "",
            "email": "test@example.com",
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors.keys())
        self.assertEqual(form.errors["username"][0], "This field is required.")

class TestProfileForm(TestCase):
    def test_ifprofileform_valid(self):
        form_data = {
                "firstname": "soorya",
                "surname": "george",
                "about": "Foodie until i die",
                "profile_image": "image.jpg",
                "fav_food": "indian",
        }
        
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ifprofileform_invalid(self):
        
        form = ProfileUpdateForm(
            {
                "firstname": str("a" * 51),
                "surname": str("a" * 51),
                "about": str("a" * 201),
                "fav_food": str("a" * 51),
            }
        )
        self.assertIn("firstname", form.errors.keys())
        self.assertIn("surname", form.errors.keys())
        self.assertIn("about", form.errors.keys())
        self.assertIn("fav_food", form.errors.keys())
        self.assertEqual(
            form.errors["firstname"][0],
            'Ensure this value has at most 50 characters (it has 51).',
        )
        self.assertEqual(
            form.errors["surname"][0],
            'Ensure this value has at most 50 characters (it has 51).',
        )
        self.assertEqual(
            form.errors["about"][0],
            'Ensure this value has at most 200 characters (it has 201).',
        )
        self.assertEqual(
            form.errors["fav_food"][0],
            'Ensure this value has at most 50 characters (it has 51).',
        )
        
        self.assertFalse(form.is_valid())