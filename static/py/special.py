"""Custom MARC21 Ingester Class"""
__author__ = "Jeremy Nelson"

import rdflib
from bibcat.ingesters.marc import MARCIngester

class SpecialMARCIngester(MARCIngester):

    def __init__(self, **kwargs):
        self.legacy_ils_pattern = "http://tiger.coloradocollege.edu/record={}"
        super(SpecialMARCIngester, self).__init__(**kwargs)

    def generate_item_iri(self, record):
        if not '907' in record:
            return
        bib_number = record['907']['a'][1:-1]
        return rdflib.URIRef(self.legacy_ils_pattern.format(bib_number))

    def transform(self, record=None, instance_uri=None, item_uri=None):
        item_iri = self.generate_item_iri(record)
        super(SpecialMARCIngester, self).transform(record=record, 
                                                   instance_uri=instance_uri, 
                                                   item_uri=item_iri)  
