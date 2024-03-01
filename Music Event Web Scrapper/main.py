from time import sleep
from mews import MusicEventWebScrapper


# This program will make a request on the url and will perform web scrapping on it.

# url
url = "https://programmer100.pythonanywhere.com/tours/"
event = MusicEventWebScrapper()

while True:
    # making request
    source = event.make_request(url)

    # creating extractor for yaml file
    value = event.extract(source, "example.yaml")

    # finally, printing on to screen
    print(value)

    if not event.store(value):
        # also writing on the database file
        event.insert_to_db(value)

        message = f"""
        Subject: Music Event Web
        Tour: {value}\n
        Have a nice day!\n
        """

        # sending email
        event.send_email(message)

    print(event.read(value))
    sleep(2)
