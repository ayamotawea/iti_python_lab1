class Book:

    def __init__(
        self,
        title: str,
        authors: list,
        description: str,
        published_date: str,
        price: str,
        source: str
    ):
        self.title = title
        self.authors = ", ".join(authors) if authors else "Unknown Author"
        self.description = description or "No description available."
        self.published_date = published_date or "Unknown publication date"
        self.price = price
        self.source = source

    def display_summary(self, index: int) -> None:

        print(f"{index}. {self.title}")
        print(f"   Author(s)       : {self.authors}")
        print(f"   Published Date  : {self.published_date}")
        print(f"   Description     : {self.description}")
        print(f"   Price           : {self.price}")
        print(f"   Source          : {self.source}")
        print("-" * 70)