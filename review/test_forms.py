from django.test import TestCase
from .forms import RatingForm


class TestRatingForm(TestCase):
    def test_ratingform_valid(self):
        form = RatingForm(
            {
                'taste': 3,
                'ambience': 4,
                'customer_service': 3,
                'value_for_money': 4,
                'location': 4,
                'comment_text':"Love this restaurant",
            }
        )
        self.assertTrue(form.is_valid())

    def test_ratingform_review_empty(self):
        form = RatingForm(
            {
                'taste': 3,
                'ambience': 4,
                'customer_service': 3,
                'value_for_money': 4,
                'location': 4,
                'comment_text':"",
            }
        )
        self.assertIn("comment_text", form.errors.keys())
        self.assertEqual(form.errors["comment_text"][0], "This field is required.")
        self.assertFalse(form.is_valid())

    
    def test_ratingform_rating_above_max(self):
        """Review form has rating above 5"""
        form = RatingForm(
            {
                'taste': 8,
                'ambience': 6,
                'customer_service': 7,
                'value_for_money': 7,
                'location': 8,
                'comment_text':"Love this restaurant",
            }
        )
        self.assertIn("taste", form.errors.keys())
        self.assertIn("ambience", form.errors.keys())
        self.assertIn("customer_service", form.errors.keys())
        self.assertIn("value_for_money", form.errors.keys())
        self.assertIn("location", form.errors.keys())
        self.assertEqual(
            form.errors["taste"][0],
            "Select a valid choice. 8 is not one of the available choices.",
        )
        self.assertEqual(
            form.errors["ambience"][0],
            "Select a valid choice. 6 is not one of the available choices.",
        )
        self.assertEqual(
            form.errors["customer_service"][0],
            "Select a valid choice. 7 is not one of the available choices.",
        )
        self.assertEqual(
            form.errors["value_for_money"][0],
            "Select a valid choice. 7 is not one of the available choices.",
        )
        self.assertEqual(
            form.errors["location"][0],
            "Select a valid choice. 8 is not one of the available choices.",
        )
        self.assertFalse(form.is_valid())