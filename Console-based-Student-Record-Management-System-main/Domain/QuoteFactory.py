from DTOs import QuoteDTO
from Domain.Quote import Quote

class QuoteFactory:
    @staticmethod
    def create(dto: QuoteDTO) -> Quote:
        return Quote(dto.content, dto.author)