import pandas as pd
from prettytable import PrettyTable

ds = pz.DataDirectory().list_registered_datasets()

# construct table for printing
table = [["Name", "Type", "Path"]]
for path, descriptor in ds:
    table.append([path, descriptor[0], descriptor[1]])

# print table of registered datasets
t = PrettyTable(table[0])
t.add_rows(table[1:])
t