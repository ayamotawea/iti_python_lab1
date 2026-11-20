
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from Book import Book


# Load environment variables from the same directory as main.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def search_books_by_field(field: str, max_results: int = 5) -> list[Book]:
    """
    Search Google Books API by subject and return Book objects.
    """

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    if not api_key:
        raise ValueError("Missing GOOGLE_BOOKS_API_KEY in .env file.")

    base_url = os.getenv("SEARCH_BASE_URL")

    if not base_url:
        raise ValueError("Missing SEARCH_BASE_URL in .env file.")

    params = {
        "q": f"subject:{field}",
        "maxResults": max_results,
        "key": api_key,
    }

    response = requests.get(
        base_url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    books = []

    for item in data.get("items", []):

        volume_info = item.get("volumeInfo", {})
        sale_info = item.get("saleInfo", {})

        # Extract basic book information
        title = volume_info.get("title", "No Title Available")

        authors = volume_info.get("authors", [])

        description = volume_info.get(
            "description",
            "No description available."
        )

        published_date = volume_info.get(
            "publishedDate",
            "Unknown publication date"
        )

        source = volume_info.get(
            "infoLink",
            "No Source Link"
        )

        # Extract price and sale information
        saleability = sale_info.get("saleability", "UNKNOWN")

        if saleability == "FREE":

            price = "Free"

        elif saleability == "FOR_SALE":

            retail_price = sale_info.get("retailPrice")

            if retail_price:
                amount = retail_price.get("amount")
                currency = retail_price.get("currencyCode", "")

                if amount is not None:
                    price = f"{amount} {currency}".strip()
                else:
                    price = "For sale, but price unavailable"

            else:
                price = "For sale, but price unavailable"

        elif saleability == "NOT_FOR_SALE":

            price = "Not available for purchase"

        else:

            price = "Price information unavailable"

        # Create Book object
        book = Book(
            title=title,
            authors=authors,
            description=description,
            published_date=published_date,
            price=price,
            source=source
        )

        books.append(book)

    return books


def main():

    field = input(
        "Enter a book field/subject (e.g., Artificial Intelligence, History): "
    ).strip()

    if not field:
        print("Search field cannot be empty.")
        return

    print(
        f"\nSearching for books in '{field}'...\n"
        + "=" * 70
    )

    try:

        results = search_books_by_field(field)

        if not results:
            print("No books found for that field.")
            return

        for idx, book in enumerate(results, start=1):
            book.display_summary(idx)

    except requests.exceptions.RequestException as e:

        print(f"API Request Error: {e}")

    except ValueError as e:

        print(f"Configuration Error: {e}")


if __name__ == "__main__":
    main()
