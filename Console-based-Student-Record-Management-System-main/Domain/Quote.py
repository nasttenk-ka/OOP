class Quote:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def __str__(self):
        return f'\n"{self.content}" — {self.author}\n'