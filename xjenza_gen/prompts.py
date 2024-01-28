from datetime import datetime

from typer import confirm, prompt

from .article import Article, Author


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
            "Author's full name? (leave empty to exit)",
            default="",
            show_default=False,
            type=str,
        )

        # Stop if the user leaves the prompt empty
        if not full_name:
            break

        name_words = full_name.strip().split(" ")
        if len(name_words) < 2:
            print("ERROR: Please enter the author's full name")
            continue
        else:  # We have a first name and a surname or more
            surname = name_words[-1]
            name = " ".join(name_words[:-1])

        email: str = prompt("Author's email?")
        affiliation: str = prompt("Author's affiliation?")
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
