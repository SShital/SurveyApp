"""
test cases
"""
from django.test import TestCase, modify_settings
from Surveyapp.models import(Organization, Employee, Survey, Question)


@modify_settings(MIDDLEWARE_CLASSES={
    'append': 'django.middleware.cache.FetchFromCacheMiddleware',
    'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
})
class MiddlewareTestCase(TestCase):
    """
    Performing middleware load tests
    """

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'django.middleware.cache.FetchFromCacheMiddleware',
        'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
    })
    def test_cache_middleware(self):
        """
        Cache middleware loading test.
        :return: None
        """
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'django.middleware.cache.FetchFromCacheMiddleware',
            'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
            'remove': [
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ],
        }):
            response = self.client.get('/')
            self.assertIn("http://127.0.0.1:8000/", response)


class ModelsTest(TestCase):
    """
    Testing Data model creation and inserting the value.
    """
    @staticmethod
    def create_organization(company_name='Harbinger',
                            location='Pune',
                            description='Innovate'):
        """
        Create object of organization data model.
        :param company_name: <data type: str>
        :param location: <data type: str>
        :param description: <data type: str>
        :return: None
        """
        return Organization.objects.create(company_name=company_name,
                                           location=location,
                                           description=description)

    @staticmethod
    def create_employee(emp_name='mona',
                        emp_username='shitalraut708@gmail.com',
                        emp_password='abcd',
                        emp_designation='Software Engineer',
                        emp_address='Pune',
                        organization=None):
        """
        Create object of organization data model.
        :param emp_name: <data type: str>
        :param emp_username: <data type: str>
        :param emp_password: <data type: str>
        :param emp_designation: <data type: str>
        :param emp_address: <data type: str>
        :param organization: <data type: str>
        :return: None
        """
        return Employee.objects.create(emp_name=emp_name,
                                       emp_username=emp_username,
                                       emp_password=emp_password,
                                       emp_designation=emp_designation,
                                       emp_address=emp_address,
                                       company=organization)

    @staticmethod
    def create_survey(survey_name='Annual Awards',
                      description='Annual Awards for harbinger',
                      date='2019-03-13'):
        """
        Create object for survey model.
        :param survey_name: <data type: str>
        :param description: <data type: str>
        :param date: <data type: datetime>
        :return: None
        """
        return Survey.objects.create(survey_name=survey_name,
                                     description=description,
                                     date=date)

    @staticmethod
    def create_question(question='How was CSR ?',
                        is_required=True,
                        question_type='text',
                        choices='good, bad, very good'):
        """
        Create object question model.
        :param question: <data type: str>
        :param is_required: <data type: bool>
        :param question_type: <data type: str>
        :param choices: <data type: str>
        :return: None
        """
        return Question.objects.create(question=question,
                                       is_required=is_required,
                                       question_type=question_type,
                                       choices=choices)

    def test_all(self):
        """
        Tests for data models.
        :return: None
        """
        org = self.create_organization()
        self.assertTrue(isinstance(org, Organization))
        self.assertEqual(org.__str__(), org.company_name)

        emp = self.create_employee(organization=org)
        self.assertTrue(isinstance(emp, Employee))
        self.assertEqual(emp.__str__(), emp.emp_name)
        self.assertEqual(str(Employee._meta.verbose_name_plural), "Employees")

        survey = self.create_survey()
        self.assertEqual(survey.__str__(), survey.survey_name)
        self.assertTrue(isinstance(survey, Survey))
        self.assertEqual(str(Survey._meta.verbose_name_plural), "surveys")

        question = self.create_question()
        self.assertTrue(isinstance(question, Question))
        self.assertEqual(question.__str__(), question.question)
