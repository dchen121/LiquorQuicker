from django.test import TestCase
from .parser import Parser
from .models import PrivateStore, BCLiquorStore, RuralAgencyStore


class ParserTests(TestCase):
    def test_sufficient_data(self):
        data = {'name': '', 'address': '', 'city': ''}
        self.assertTrue(Parser.sufficient_data(data))

        data = {}
        self.assertFalse(Parser.sufficient_data(data))

    def test_clean_data(self):
        name = 'LAKEWOOD INN'
        city = '100 MILE HOUSE'
        address = '365 S CARIBOO HWY'

        self.assertEqual(Parser.clean_data(name, 'name'), 'Lakewood Inn')
        self.assertEqual(Parser.clean_data(city, 'city'), '100 Mile House')
        self.assertEqual(Parser.clean_data(address, 'address'), '365 S Cariboo Hwy')

    def test_if_data_is_retrieved(self):
        Parser()

        self.assertTrue(PrivateStore.objects.get(store_name="Lakewood Inn"))
        self.assertTrue(PrivateStore.objects.get(store_name="Jolly Coachman"))
        self.assertTrue(PrivateStore.objects.get(store_name="Abc Liquor Store (Zeballos)"))

        self.assertTrue(BCLiquorStore.objects.get(store_name="Ashcroft"))
        self.assertTrue(BCLiquorStore.objects.get(store_name="Commercial Drive"))
        self.assertTrue(BCLiquorStore.objects.get(store_name="Whistler Village"))

        self.assertTrue(RuralAgencyStore.objects.get(store_name="Shuswap Lake Park Store"))
        self.assertTrue(RuralAgencyStore.objects.get(store_name="Baynes Lake General Store"))
        self.assertTrue(RuralAgencyStore.objects.get(store_name="Manning Park Resort"))
