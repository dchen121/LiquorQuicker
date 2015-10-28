from urllib.request import urlopen
from csv import DictReader
from io import TextIOWrapper

from .models import BCLiquorStore, PrivateStore, RuralAgencyStore


class Parser:
    naming = {'name': ['NAME', 'establishmentname', 'RAS Store Name'],
              'address': ['ADDRESS', 'address', 'Address'],
              'city': ['CITY', 'city', 'Town/City'],
              'post_code': ['POSTAL CODE', 'Postal code']}
    urls = [('http://goo.gl/7AI4ip', RuralAgencyStore),
            ('http://goo.gl/88yxeJ', BCLiquorStore),
            ('http://goo.gl/730MnE', PrivateStore)]

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
        if self.new_data(entry):
            self.add_to_model(data, model)

    @staticmethod
    def new_data(entry):
        """
        Tests to see if the data contained is unique data that needs to be
        entered. In the case of the private liquor store data set only those of
        the 'type' 'Private Liquor Store' need to be added.
        :param entry:
        :return:
        """
        # TODO: check to see if entry is in database already!!!
        if 'type' in entry:
            if entry['type'] == 'Private Liquor Store':
                return True
            else:
                return False
        else:
            return True

    def generate_data(self, entry):
        """
        Formats the data in the given entry from the csv file. Maps the keys
        from the entry onto usable keys in data using the self.key
        :param entry: A dictionary read from the csv file.
        :return: A dictionary formatted with the universal keys.
        :rtype: dict
        """
        data = {}
        for heading, value in entry.items():
            if heading in self.key and not value == '':
                data[self.key[heading]] = value
        return data

    @staticmethod
    def add_to_model(data, model):
        """
        Adds the data from the csv file if it contains at least a name, address
        and city. Postal code is added optionally.
        :param data: The formatted data from the csv file
        :param model: The class from the models module to store the data in.
        """
        if 'name' and 'address' and 'city' in data:
            location = model(store_name=data['name'],
                             address=data['address'],
                             city=data['city'])

            if 'post_code' in data:
                location.post_code = data['post_code']

            location.save()

    def invert_naming(self):
        """
        Inverts the naming dictionary so that each random csv term is a key
        mapping it to the standardized key value.
        :return: inverted dictionary
        :rtype: dict
        """
        inverted = {}
        for key, names in self.naming.items():
            for name in names:
                inverted[name] = key

        return inverted
