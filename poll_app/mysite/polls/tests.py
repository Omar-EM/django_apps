import datetime 

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.

def create_question(question_text, days):
    """Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published in the past, positive otherwise)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question(question_text=question_text, publication_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() should return False for questions whose publication_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() should return False for questions whose publication_date
        is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=5)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() should return True for questions whose publication_date
        is recent than 1 day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(publication_date=time)
        self.assertIs(question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exists, an appropriate message is displayed on the index page"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Question with a publication_date in the past are displayed on the index page"""
        question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        """Question with a future publication_date aren't displayed"""
        create_question(question_text="Future Qst", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed"""
        question = create_question(question_text="Past Question", days=-30)
        create_question(question_text="Future Qst", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])
