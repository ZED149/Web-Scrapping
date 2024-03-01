import requests
import selectorlib
import smtplib, ssl
import sqlite3


# This file contains Music Event Web Scrapper class (mews)

class MusicEventWebScrapper():

    # make request
    def make_request(self, url):
        """
        This function takes a url and makes a request to it.
        Then it returns the source code of the webpage if return is 200 [success]
        :param url:
        :return:
        """
        # making a request to the specific url
        response = requests.get(url)
        # storing it in text format
        source = response.text
        # Return
        return source

    # extract
    def extract(self, source, filename):
        """
        This function extracts a specific word from the source of the webpage.
        It takes source and filename.
        :return:
        """
        # initiating extractor object
        extractor = selectorlib.Extractor.from_yaml_file(filename)
        # extracting the keyword
        value = extractor.extract(source)['tours']
        # Return
        return value

    # read
    def read(self, value):
        """
        This function reads from the database and returns all values.
        :return:
        """
        if value == "No upcoming tours":
            return None

        band, city, date = value.split(',')
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        conn.close()
        return rows[0]

    # store
    def store(self, value):
        """
        This function stores the event that is found on a database.
        :return:
        """
        if value != "No upcoming tours":
            content = ""
            with open('tours.txt', 'r') as f:
                content = f.read()
            if value not in content:
                with open('tours.txt', 'a') as f:
                    f.write(value + '\n')
                return False
            else:
                return True
        else:
            return True

    # send email
    def send_email(self, message):
        """
        This function sends an email with the provided message.
        :param message:
        :return:
        """
        host = 'smtp.gmail.com'
        port = 465

        username = "salmanahmad111499@gmail.com"
        password = "hozh uhdy dllv fpct"

        receiver = "salmanahmad1279@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)

        print("Email send successfully\n")

    # insert to db
    def insert_to_db(self, value):
        """
        This function inserts value into the database.
        :param value:
        :return:
        """

        # splitting value
        band, city, date = value.split(',')
        # making a conn
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events VALUES (?, ?, ?)", (band, city, date))
        conn.commit()
        conn.close()
