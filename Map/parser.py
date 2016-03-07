import re
from abc import abstractmethod, ABCMeta
from csv import DictReader
from io import TextIOWrapper
from urllib.request import urlopen

from .models import BCLiquorStore, PrivateStore, RuralAgencyStore, BCLiquor


class Parser(metaclass=ABCMeta):
    formatting = {}
    urls = []
    naming = {}
    encoding = 'cp1252'

    def __init__(self):
        """
        Executes the parser which will download the information from each of
        the urls and then using the naming scheme provided, map the values from
        the csv files into the appropriate table.
        """
        self.key = self.invert_naming()
        for url in self.urls:
            self.parse(*url)

    @classmethod
    def invert_naming(cls):
        """
        Inverts the naming dictionary so that each random csv term is a key
        mapping it to the standardized key value.
        :return: inverted dictionary
        :rtype: dict
        """
        inverted = {}
        for key, (names, req) in cls.naming.items():
            for name in names:
                inverted[name] = key

        return inverted

    def parse(self, url, model):
        """
        Parses a csv from the given url location and adds it to the given model
        :param url: A url to the associated cvs file
        :param model: A class from the models module
        """
        with urlopen(url) as content:
            csv = TextIOWrapper(content, encoding=self.encoding)
            data = DictReader(csv)

            for row in data:
                self.add_entry(row, *model)

    def add_entry(self, entry, model, filter):
        """
        Adds an entry to the given model.
        :param entry: a dictionary entry from the csv file
        :param model: a model from the models module that entry is to be added
        :param filter: None or the name of a function declared in the subclass
                       which returns true or false based on some information in
                       the raw data.
        """
        if self.addable(entry, filter):
            data = self.generate_data(entry)
            self.add_to_model(data, model)

    def addable(self, entry, filter):
        """
        Determines if the entry is addable based on any filters associated with
        the model. If filter is set to None returns True.
        :param entry: the raw data from the csv file in the form of a dictionary
        :param filter: None or the name of a static function declared in the
                       subclass which returns true or false based on some
                       information the raw data.
        :rtype: bool
        """
        if filter is None:
            return True
        else:
            filter_func = self.__class__.__dict__[filter].__func__
            return filter_func(entry)

    def generate_data(self, entry):
        """
        Formats the data in the given entry from the csv file. Maps the keys
        from the entry onto usable keys in data using the self.key. All values
        are formatted to be first letter uppercase.
        :param entry: A dictionary read from the csv file
        :return: A dictionary formatted with the universal keys
        :rtype: dict
        """
        data = {}

        for heading, value in entry.items():
            if heading in self.key:
                key = self.key[heading]
                value = self.clean_data(value, key)
                if value:
                    data[key] = value

        return data

    @classmethod
    def clean_data(cls, value, key):
        """
        Cleans all data from a file. Formats all input to capital first,
        removes extra whitespace and if the user has defined a specific format
        in self.formatting then uses regex to try and find the correctly
        formatted substring.
        :param value: The value to be cleaned
        :param key: The key associated with the value
        :return: The correctly formatted string
        :rtype: str
        """
        value = value.title()  # format text
        value = re.sub(r'[\t\n\r ]+', ' ', value)  # remove extra whitespace
        value = value.strip() # remove leading and trailing whitespace

        if key in cls.formatting:
            fmat = cls.formatting[key]

            if 'format_string' in fmat:
                pattern = fmat['format_string']
                value = re.findall(pattern, value)
                if not value:
                    return ''

                if 'index' in fmat:
                    index = fmat['index']
                    value = value[0][index]
                else:
                    value = value[0]

            if 'remove_chars' in fmat:
                remove = fmat['remove_chars']
                value = re.sub(remove, '', value)
                value = re.sub(r'[\t\n\r ]+', ' ', value)

        return value

    def add_to_model(self, data, model):
        """
        Adds all the data in data to a new instance of a model using the
        standardized keys values in data.
        :param data: a dictionary of data entries to be added to the model
        :param model: the model to be used
        """
        if self.sufficient_data(data) and self.new_data(data, model):
            instance = model()
            for key in data.keys():
                instance.__dict__[key] = data[key]

            instance.save()

    @classmethod
    def sufficient_data(cls, data):
        """
        Insures that the data dictionary has sufficient data as found in the
        self.naming tuple
        :param data: The data to be entered into the database
        :return: True or false if all necessary data present
        :rtype: bool
        """
        for key, (list, req) in cls.naming.items():
            if req == 'required' and key not in data:
                return False

        return True

    @classmethod
    @abstractmethod
    def new_data(cls, data, model):
        """
        Determines if the data is unique. If so true is returned. If not
        handles non-unique data and returns false.
        :param data: The data to be added to the database
        :param model: The model being used by django
        :return: True or false if the data is new to the database
        :rtype: bool
        """
        pass


class LocationParser(Parser):
    naming = {'name': (['NAME', 'establishmentname', 'RAS Store Name'], 'required'),
              'address': (['ADDRESS', 'address', 'Address'], 'required'),
              'city': (['CITY', 'city', 'Town/City'], 'required'),
              'post_code': (['POSTAL CODE', 'Postal code'], 'optional')}
    urls = [('https://catalogue.data.gov.bc.ca/dataset/f3686275-a70b-458f-a1a7-cdaecbd9d269/resource/07fd8b1e-34af-431b-9b12-392100968ea0/download/CWorking-CopiesOpen-DataJan2016ListsBCLiquorRuralAgencyStoreLocations.csv', (RuralAgencyStore, None)),
            ('https://catalogue.data.gov.bc.ca/dataset/5fd19e19-e2ee-4326-834f-84de7e653581/resource/0eb7f24c-babb-4dbf-8f43-536e3f8128fa/download/cworkingcopiesopendatabcliquorstorelocations.csv', (BCLiquorStore, None)),
            ('http://www.pssg.gov.bc.ca/lclb/docs-forms/web_lrs.csv', (PrivateStore, 'private_store_filter'))]
    formatting = {'address': {'format_string': r'(Physical: )?' +
                                               r'([0-9]{3,5} ?- ?)?' +
                                               r'(#[0-9]{1,4} (& #[0-9]{1,4} )?)?' +
                                               r'([0-9]{3,5} [A-Za-z0-9\-.#& ]*)' +
                                               r'( Mailing:)?',
                              'index': 4,
                              'remove_chars': r'[-]+'},
                  'post_code': {'format_string': r'[A-Z][0-9][A-Z] ?[0-9][A-Z][0-9]'}}

    @staticmethod
    def private_store_filter(entry):
        """
        Returns true if 'type' in entries from the private liquor store file is
        'Private Liquor Store'. Otherwise returns falls
        :param entry: An entry from the private liquor store csv file
        :return: True if the type is 'Private Liquor Store'
        :rtype: bool
        """
        if entry['type'] == 'Private Liquor Store':
            return True
        else:
            return False

    @classmethod
    def new_data(cls, data, model):
        """
        Implements this abstract method in Parser. Uniqueness determined by
        address. If the data is non-unique, updates the name updates the name
        of the store to the one stored in data.
        """
        test = model.objects.filter(address=data['address'])
        if test.count() == 0:
            return True
        else:
            store = test[0]
            store.name = data['name']
            store.save()
            return False


class PriceParser(Parser):
    naming = {'category': (['ITEM_CATEGORY_NAME'], 'optional'),
              'name': (['PRODUCT_LONG_NAME'], 'required'),
              'size': (['PRODUCT_LITRES_PER_CONTAINER'], 'required'),
              'price': (['PRODUCT_PRICE'], 'required')}
    urls = [('http://goo.gl/VQTMv7', (BCLiquor, None))]

    @classmethod
    def new_data(cls, data, model):
        """
        Implements the new_data method from Parser. Uniqueness based on name
        size of the liquor. If the liquor is in the DB then the price is
        updated.
        """
        test = model.objects.filter(name=data['name'], size=data['size'])
        if test.count() == 0:
            return True
        else:
            liquor = test[0]
            liquor.price = data['price']
            liquor.save()
            return False
