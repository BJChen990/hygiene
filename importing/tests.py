from django.test import TestCase
from django.core.urlresolvers import resolve
from importing.views import import_page

# Create your tests here.
class ImportingPageTest(TestCase):

    def test_importing_page_resolving(self):
        target = resolve('/importing/')
        self.assertEqual(target.func, import_page)

