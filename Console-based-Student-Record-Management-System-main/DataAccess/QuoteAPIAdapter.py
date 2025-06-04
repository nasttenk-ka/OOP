import requests
from Domain.Quote import Quote
from DTOs.QuoteDTO import QuoteDTO
from Domain.QuoteFactory import QuoteFactory

class QuoteAPIAdapter:
    def get_quote(self) -> Quote:
        url = "http://api.forismatic.com/api/1.0/"
        params = {
            "method": "getQuote",
            "format": "json",
            "lang": "en"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                dto = QuoteDTO(data['quoteText'].strip(), data['quoteAuthor'].strip() or "Unknown")
            else:
                dto = QuoteDTO("Stay strong!", "System")
        except Exception as e:
            print(f"Error: {e}")
            dto = QuoteDTO("Error fetching quote", "System")
        return QuoteFactory.create(dto)