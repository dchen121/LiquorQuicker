from django.test import TestCase
from .parser import LocationParser
from .models import PrivateStore, BCLiquorStore, RuralAgencyStore


class ParserTests(TestCase):
    def test_sufficient_data_method(self):
        data = {'name': '', 'address': '', 'city': ''}
        self.assertTrue(LocationParser.sufficient_data(data))

        data = {}
        self.assertFalse(LocationParser.sufficient_data(data))

    def test_clean_data_method(self):
        name = 'LAKEWOOD INN'
        city = '100 MILE HOUSE'
        address = '365 S CARIBOO HWY'

        self.assertEqual(LocationParser.clean_data(name, 'name'), 'Lakewood Inn')
        self.assertEqual(LocationParser.clean_data(city, 'city'), '100 Mile House')
        self.assertEqual(LocationParser.clean_data(address, 'address'), '365 S Cariboo Hwy')

    def test_new_data_method_unique(self):
        store = PrivateStore(name='TEST NAME', address='TEST ADDRESS', city='TEST CITY')
        store.save()
        store_data = {'name': 'NEW NAME', 'address': 'NEW ADDRESS', 'city': 'NEW CITY'}

        self.assertTrue(LocationParser.new_data(store_data, PrivateStore))

    def test_new_data_method_not_unique(self):
        store = PrivateStore(name='TEST NAME', address='TEST ADDRESS', city='TEST CITY')
        store.save()
        store_data = {'name': 'NEW NAME', 'address': 'TEST ADDRESS', 'city': 'TEST CITY'}

        self.assertFalse(LocationParser.new_data(store_data, PrivateStore))

        store = PrivateStore.objects.get(address='TEST ADDRESS')
        self.assertEqual(store.name, 'NEW NAME')

    def test_if_only_unique_data_input(self):
        store = PrivateStore(name='TESTING TESTING', address='365 S Cariboo Hwy', city='100 Mile House')
        store.save()
        LocationParser()
        store = PrivateStore.objects.get(address='365 S Cariboo Hwy')

        self.assertEqual(store.name, 'Lakewood Inn')

    def test_if_Private_data_is_retrieved(self):
        LocationParser()

        self.assertTrue(PrivateStore.objects.get(name="Lakewood Inn"))
        self.assertTrue(PrivateStore.objects.get(name="Jolly Coachman"))
        self.assertTrue(PrivateStore.objects.get(name="Abc Liquor Store (Zeballos)"))

    def test_if_BCL_data_is_retrieved(self):
        LocationParser()

        self.assertTrue(BCLiquorStore.objects.get(name="Ashcroft"))
        self.assertTrue(BCLiquorStore.objects.get(name="Commercial Drive"))
        self.assertTrue(BCLiquorStore.objects.get(name="Whistler Village"))

    def test_if_RAS_data_is_retrieved(self):
        LocationParser()

        self.assertTrue(RuralAgencyStore.objects.get(name="Shuswap Lake Park Store"))
        self.assertTrue(RuralAgencyStore.objects.get(name="Baynes Lake General Store"))
        self.assertTrue(RuralAgencyStore.objects.get(name="Manning Park Resort"))
