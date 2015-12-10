from django.test import TestCase
from django.core.urlresolvers import resolve
from importing.views import import_page
from importing.models import structure_data
import xlrd

# Create your tests here.
class ImportingPageTest(TestCase):

    def test_importing_page_resolving(self):
        target = resolve('/importing/')
        self.assertEqual(target.func, import_page)


class XslProcessTest(TestCase):

    def test_read_xls_file(self):
        book = xlrd.open_workbook('test.xls')
        self.assertIsNotNone(book)
        self.assertEqual(book._all_sheets_count, 3)

    def test_analsys_xls(self):
        structure_data('test.xls')
