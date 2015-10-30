from urllib.request import urlopen
from csv import DictReader
from io import TextIOWrapper
import re

from .models import BCLiquorStore, PrivateStore, RuralAgencyStore


class Parser:
    naming = {'name': ['NAME', 'establishmentname', 'RAS Store Name'],
              'address': ['ADDRESS', 'address', 'Address'],
              'city': ['CITY', 'city', 'Town/City'],
              'post_code': ['POSTAL CODE', 'Postal code']}
    urls = [('http://goo.gl/7AI4ip', RuralAgencyStore),
            ('http://goo.gl/88yxeJ', BCLiquorStore),
            ('http://goo.gl/730MnE', PrivateStore)]
    formatting = {'address': r'(Physical: )?([0-9]{3,5} [A-Za-z0-9\-. ]*)( Mailing:)?',
                  'post_code': r'()?([A-Z][0-9][A-Z] ?[0-9][A-Z][0-9])()?'}

    def __init__(self):
        """
        Executes the parser which will download the information from each of
        the urls and then using the naming scheme provided, map the values from
        the csv files into the appropriate table.
        """
        self.key = self.invert_naming()
        for url in self.urls:
            self.parse(*url)

    def parse(self, url, model):
        """
        Parses a csv from the given url location and adds it to the given model
        :param url: A url to the associated cvs file
        :param model: A class from the models module
        """
        with urlopen(url) as content:
            csv = TextIOWrapper(content, encoding='cp1252')
            data = DictReader(csv)

            for row in data:
                self.add_entry(row, model)

    def add_entry(self, entry, model):
        """
        Adds an entry to the given model.
        :param entry: a dictionary entry from the csv file
        :param model: a model from the models module that entry is to be added
        """
        data = self.generate_data(entry)
        if model is not PrivateStore or self.private_store(entry):
            self.add_to_model(data, model)

    @staticmethod
    def private_store(entry):
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
        Cleans all data from file. Formats all input to capital first, removes
        extra whitespace and if the user has defined a specific format in
        self.formatting then uses regex to try and find the correctly formatted
        substring.
        :param value: The value to be cleaned
        :param key: The key associated with the value
        :return: The correctly formatted string
        :rtype: str
        """
        value = value.title()              # format text
        value = re.sub(r'[\t\n\r ]+', ' ', value)  # remove extra whitespace

        if key in cls.formatting:
            pattern = cls.formatting[key]
            value = re.findall(pattern, value)

            if value:
                return value[0][1]
            else:
                return ''

        else:
            return value

    def add_to_model(self, data, model):
        """
        Adds the data from the csv file if it is sufficient and new. Postal
        code is added optionally.
        :param data: The formatted data from the csv file
        :param model: The class from the models module to store the data in
        """
        if self.sufficient_data(data) and self.new_data(data, model):
            location = model(store_name=data['name'],
                             address=data['address'],
                             city=data['city'])

            if 'post_code' in data:
                location.post_code = data['post_code']

            location.save()

    @classmethod
    def sufficient_data(cls, data):
        """
        Insures that the data dictionary has sufficient data ie a name, city
        and address.
        :param data: The data to be entered into the database
        :return: True or false if all necessary data present
        :rtype: bool
        """
        return 'name' and 'city' and 'address' in data

    @classmethod
    def new_data(cls, data, model):
        """
        Returns true if there is no such entry in the database. If the entry
        does exist, the name of the store is updated and saved while false is
        returned by the function.
        :param data: The data to be added to the database
        :param model: The model being used by django
        :return: True or false if the data is new to the database
        :rtype: bool
        """
        if model.objects.filter(address=data['address']).count() == 0:
            return True
        else:
            store = model.objects.get(address=data['address'])
            store.store_name = data['name']
            store.save()
            return False

    @classmethod
    def invert_naming(cls):
        """
        Inverts the naming dictionary so that each random csv term is a key
        mapping it to the standardized key value.
        :return: inverted dictionary
        :rtype: dict
        """
        inverted = {}
        for key, names in cls.naming.items():
            for name in names:
                inverted[name] = key

        return inverted
