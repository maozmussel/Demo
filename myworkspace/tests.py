import os, sys, stat
from django.test import TestCase
from .fetch_alchemer_to_csv import *

class FetchDataFromAlchemerTests(TestCase):

    def test_complete_with_success(self):
        """
        fetch_survey_data_into_csv() returns Success when all parameters given properly
        """
        self.assertIs(fetch_survey_data_into_csv('/tmp/outputTest.csv', '2019-01-20', '2019-01-30'), 'Success')

    def test_wrong_file_path_given(self):
        """
        fetch_survey_data_into_csv() returns error message when given out file name is wrong
        """
        self.assertIs(fetch_survey_data_into_csv('/tmpX/outputTest.csv', '2019-01-20', '2019-01-30'), 'Problem converting data into CSV file')
