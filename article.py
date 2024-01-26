import datetime


class Author:
    name: str
    email: str
    surname: str
    affiliation: str
    is_corresponding: bool

    def __init__(
        self, name: str = "", surname: str = "", email: str = "", affiliation: str = ""
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.affiliation = affiliation
        self.is_corresponding = False

    def corresponding(self) -> "Author":
        self.is_corresponding = True

        return self


class Article:
    title: str
    year: int
    authors: list[Author]

    def __init__(
        self,
        title: str = "",
        year: int = datetime.datetime.now().year,
        authors: list[Author] = [],
    ):
        self.title = title
        self.authors = authors
        self.year = year

    def dict(self):
        authors_string = ""
        for i, author in enumerate(self.authors):
            authors_string += f"{author.name[0]}. {author.surname}$^{{{i+1}}}$"
            if i == len(self.authors) - 2:
                authors_string += " and "
            elif i != len(self.authors) - 1:
                authors_string += ", "

        # if any affiliation is the same, group them together
        affiliation_string = ""
        for i, author in enumerate(self.authors):
            if author.affiliation in [a.affiliation for a in self.authors[:i]]:
                continue
            affiliation_string += f"$^{{{i+1}}}$ {author.affiliation}\\\\"

        # replace the affiliation number of the authors that have the same affiliation
        for i, author in enumerate(self.authors):
            for j, other_author in enumerate(self.authors[:i]):
                if author.affiliation == other_author.affiliation:
                    authors_string = authors_string.replace(
                        f"$^{{{i+1}}}$", f"$^{{{j+1}}}$"
                    )
                    break

        corresponder = [author for author in self.authors if author.is_corresponding]
        corresponder = corresponder[0] if len(corresponder) > 0 else None

        dict_to_return = {
            "title": self.title,
            "year": self.year,
            "authors": self.authors,
            "authors_string": authors_string,
            "affiliations": affiliation_string,
            "corresponder": corresponder,
        }

        return dict_to_return
