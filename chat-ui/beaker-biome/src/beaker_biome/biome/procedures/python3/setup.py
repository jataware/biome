import palimpzest as pz
import pandas as pd
import time
import os
import IPython

formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0

class ScientificPaper(pz.PDFFile):
   """Represents a scientific research paper, which in practice is usually from a PDF file"""
   paper_title = pz.Field(desc="The title of the paper. This is a natural language title, not a number or letter.", required=True)
   author = pz.Field(desc="The name of the first author of the paper", required=True)
   abstract = pz.Field(desc="A short description of the paper contributions and findings", required=False)

class Reference(pz.Schema):
    """ Represents a reference to another paper, which is cited in a scientific paper"""
    index = pz.Field(desc="The index of the reference in the paper", required=True)
    title = pz.Field(desc="The title of the paper being cited", required=True)
    first_author = pz.Field(desc="The author of the paper being cited", required=True)
    year = pz.Field(desc="The year in which the cited paper was published", required=True)

import IPython
formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0
print("Setup complete")