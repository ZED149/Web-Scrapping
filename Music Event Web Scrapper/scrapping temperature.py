

import requests
import selectorlib
import datetime

url = "https://programmer100.pythonanywhere.com/"
response = requests.get(url)

source = response.text

extractor = selectorlib.Extractor.from_yaml_file('example.yaml')
label = extractor.extract(source)['temperaturel']
id = extractor.extract(source)['temperatured']

print(f"Temperature Label: {label} \n "
      f"Temperature Id: {id}")

# doing some logging
with open('temperature.txt', 'a') as file:
    date = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    file.write(f"{str(date)},{id}\n")
