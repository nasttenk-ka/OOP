import unittest
from unittest.mock import patch
from DataAccess.QuoteAPIAdapter import QuoteAPIAdapter

class QuoteApiTest(unittest.TestCase):

    @patch("DataAccess.QuoteAPIAdapter.requests.get")
    def test_quote_api_success(self, mock_get):
        # Simulate a valid Forismatic API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "quoteText": "Success is not final, failure is not fatal.",
            "quoteAuthor": "Winston Churchill"
        }

        adapter = QuoteAPIAdapter()
        quote = adapter.get_quote()

        self.assertEqual(quote.content, "Success is not final, failure is not fatal.")
        self.assertEqual(quote.author, "Winston Churchill")

    @patch("DataAccess.QuoteAPIAdapter.requests.get")
    def test_quote_api_missing_author(self, mock_get):
        # Author missing in response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "quoteText": "Act as if what you do makes a difference. It does.",
            "quoteAuthor": ""
        }

        adapter = QuoteAPIAdapter()
        quote = adapter.get_quote()

        self.assertEqual(quote.content, "Act as if what you do makes a difference. It does.")
        self.assertEqual(quote.author, "Unknown")

    @patch("DataAccess.QuoteAPIAdapter.requests.get")
    def test_quote_api_http_error(self, mock_get):
        # Simulate a non-200 status
        mock_get.return_value.status_code = 503

        adapter = QuoteAPIAdapter()
        quote = adapter.get_quote()

        self.assertEqual(quote.content, "Stay strong!")
        self.assertEqual(quote.author, "System")

    @patch("DataAccess.QuoteAPIAdapter.requests.get", side_effect=Exception("Connection timeout"))
    def test_quote_api_exception(self, mock_get):
        adapter = QuoteAPIAdapter()
        quote = adapter.get_quote()

        self.assertEqual(quote.content, "Error fetching quote")
        self.assertEqual(quote.author, "System")
