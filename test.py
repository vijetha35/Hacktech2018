
""""
from main import get_image_ailment


if __name__ == "__main__":
    s = get_image_ailment("https://api.twilio.com/2010-04-01/Accounts/AC1461e56cf2e8ac12cf643c44aa281fd6/Messages/MM32c9d25cafb334cec6e152a724e24548/Media/MEfef412454724239129a6b14b3f632b47")
    print(s)
"""
import unittest
import main


class firstAidTestCase(unittest.TestCase):

    def setUp(self):

        main.app.config['TESTING'] = True
        client = main.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()