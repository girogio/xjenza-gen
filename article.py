import datetime
from os import path


class Author:
    name: str
    email: str
    surname: str
    affiliation: str
    is_corresponding: bool

    def __init__(
        self,
        name: str = "",
        surname: str = "",
        email: str = "",
        affiliation: str = "",
        corresponding: bool = False,
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.affiliation = affiliation
        self.is_corresponding = corresponding

    def __repr__(self) -> str:
        return f"{self.name} {self.surname} ({self.email}) {'corresponding' if self.is_corresponding else ''}"

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

    def authors_from_file(self, file_path: str):
        assert path.exists(file_path), "Path to authors file does not exist"

        with open(file_path, "r") as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue

                name, surname, email, affiliation, corresponding = line.split(";")
                self.authors.append(
                    Author(
                        name.strip(),
                        surname.strip(),
                        email.strip(),
                        affiliation.strip(),
                        corresponding.lower().strip() == "yes",
                    )
                )

        return self

    def write_authors_to_file(self, file_path: str):
        assert path.exists(file_path), "Path to authors file does not exist"

        with open(file_path, "w") as f:
            f.write("# name; surname; email; affiliation; corresponding\n")
            for author in self.authors:
                f.write(
                    f"{author.name}; {author.surname}; {author.email}; {author.affiliation}; {'Yes' if author.is_corresponding else 'No'}\n"
                )

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
