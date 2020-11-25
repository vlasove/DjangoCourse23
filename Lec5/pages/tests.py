from django.test import SimpleTestCase
"""
SimpleTestCase - используем потому, что не задействована база данных
"""
# Create your tests here.
class PagesTests(SimpleTestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/') 
        self.assertEqual(response.status_code, 200)

    def test_aboutpage_status_code(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200) 

    def test_infopage_status_code(self):
        response = self.client.get("/info/")
        self.assertEqual(response.status_code, 200) 


