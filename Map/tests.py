from django.test import TestCase
from .parser import LocationParser, PriceParser
from .models import PrivateStore, BCLiquorStore, RuralAgencyStore, BCLiquor


class LocationParserTests(TestCase):
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


class PriceParserTest(TestCase):
    def test_new_data_method_unique(self):
        liquor = BCLiquor(category='Test Category', name='Test Name', size=0.375, price=3.50)
        liquor.save()

        data = {'category':'Test Category', 'name':'New Name', 'size':0.750, 'price':3.50}
        self.assertTrue(PriceParser.new_data(data, BCLiquor))

        data = {'category':'Test Category', 'name':'Test Name', 'size':0.750, 'price':3.50}
        self.assertTrue(PriceParser.new_data(data, BCLiquor))

        data = {'category':'Test Category', 'name':'New Name', 'size':0.375, 'price':3.50}
        self.assertTrue(PriceParser.new_data(data, BCLiquor))

    def test_new_data_method_not_unique(self):
        liquor = BCLiquor(category='Test Category', name='Test Name', size=0.375, price=3.50)
        liquor.save()
        data = {'category':'Test Category', 'name':'Test Name', 'size':0.375, 'price':2.50}

        self.assertFalse(PriceParser.new_data(data, BCLiquor))
        liquor = BCLiquor.objects.get(name='Test Name', size=0.375)
        self.assertEqual(liquor.price, 2.50)

    def test_if_data_is_retrieved(self):
        PriceParser()

        self.assertTrue(BCLiquor.objects.get(category='Wine',
                                             name='Cherry Point - Cowichan Blackberry',
                                             size=0.375,
                                             price=19.89))
        self.assertTrue(BCLiquor.objects.get(category='Wine',
                                             name='Valtellina Sfursat - Aldo Rainoldi 09',
                                             size=0.75,
                                             price=50.99))
        self.assertTrue(BCLiquor.objects.get(category='Beer',
                                             name='Mill St - Lager Organic',
                                             size=0.341,
                                             price=11.79))
