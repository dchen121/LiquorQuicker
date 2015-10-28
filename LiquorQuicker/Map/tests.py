from django.test import TestCase
from .parser import Parser
from .models import PrivateStore, BCLiquorStore, RuralAgencyStore


class ParserTests(TestCase):
    def test_if_data_is_retrieved(self):
        Parser()
        self.assertTrue(PrivateStore.objects.get(store_name="LAKEWOOD INN"))
        self.assertTrue(PrivateStore.objects.get(store_name="JOLLY COACHMAN"))
        self.assertTrue(PrivateStore.objects.get(store_name="ABC LIQUOR STORE (ZEBALLOS)"))

