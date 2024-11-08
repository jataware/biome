#!/usr/bin/env python

# usage: get the PDC js webpack bundle from the website's network request,
# run it through prettifier/any other JS formatter to ensure the string templates are easy
# to extract with regex, then run
#   $ python pdc_regex.py > pdc_schema.graphql
# to get a list of queries isolated.

import sys 
import re 

def main():
    if len(sys.argv) < 2:
        print("usage: pdc_regex.py [filename]")
        return 
    try:
        with open(sys.argv[1], 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"'{sys.argv[1]}': file not found")
        return
    except Exception as e:
        print(f"{e}")
        return 
    pattern = re.compile(r'`\n\s*(query [^`]+)', re.MULTILINE | re.IGNORECASE)
    results = [match.group(1) for match in re.finditer(pattern, content)]
    [print(result) for result in results]

if __name__ == "__main__":
    main()
