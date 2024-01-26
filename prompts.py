from datetime import datetime
from typer import prompt, confirm
from article import Article, Author


def prompt_title() -> str:
    """Prompt the user for the title of the article."""
    return prompt("Title of the article?", default="A very interesting article")


def prompt_short_title(title: str) -> str:
    """Prompt the user for the short title of the article."""
    return prompt(
        "Short title of the article?",
        default=title if len(title) < 150 else "",
        type=str,
    )


def prompt_year_of_publication() -> int:
    """Prompt the user for the year of publication of the article."""
    return prompt("Year of publication?", default=datetime.now().year, type=int)


def prompt_authors() -> list[Author]:
    """Prompt the user for the authors of the article."""
    authors = []
    while True:
        print(f"\n{len(authors)} author(s) so far\n{'-' * 20}\n")

        full_name: str = prompt(
            "Author full name? (leave empty to finish)",
            default="",
            show_default=False,
            type=str,
        )

        # Stop if the user leaves the prompt empty
        if not full_name:
            break

        name, surname = full_name.strip().split(" ")
        email: str = prompt("Author email?")
        affiliation: str = prompt("Author affiliation?")
        is_corresponding: bool = confirm(f"Is {full_name} the corresponding author?")
        author = Author(name, surname, email, affiliation, is_corresponding)

        authors.append(author)

    return authors


def prompt_abstract() -> str:
    """Prompt the user for the abstract of the article."""
    abstract = prompt("Abstract of the article?", default="", type=str)
    word_count = len(abstract.split(" "))
    if word_count >= 250:
        print(
            f"WARNING: Abstract is too long ({word_count} words), it should be less than 250 words"
        )

    return ". ".join([sentence.strip() for sentence in abstract.split(".")])


def prompt_keywords() -> list[str]:
    """Prompt the user for the keywords of the article."""
    keywords = prompt("Enter a comma-separated list of keywords", default="", type=str)
    return [keyword.strip() for keyword in keywords.split(",")]


def prompt_article() -> Article:
    """Prompt the user for the article."""
    title = prompt_title()
    short_title = prompt_short_title(title)
    year = prompt_year_of_publication()
    authors = prompt_authors()
    abstract = prompt_abstract()
    keywords = prompt_keywords()
    return Article(
        title=title,
        short_title=short_title,
        year=year,
        authors=authors,
        abstract=abstract,
    ).add_keywords(*keywords)
