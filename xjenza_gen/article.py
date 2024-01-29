import datetime
from os import path

from xjenza_gen.insertable import Subsection


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
        is_corresponding: bool = False,
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.affiliation = affiliation
        self.is_corresponding = is_corresponding

    def corresponding(self) -> "Author":
        self.is_corresponding = True

        return self


class Section:
    title: str
    content: str

    def __init__(self, title: str = "", content: str = ""):
        self.title = title
        self.content = content

    def dict(self):
        return {"title": self.title, "content": self.content}

    def __repr__(self) -> str:
        return f"{self.title}: {self.content}"

    def __str__(self) -> str:
        return rf"\section{{{self.title}}}" + "\n" + self.content


class Article:
    title: str
    year: int
    authors: list[Author]
    abstract: str
    content: str

    def __init__(
        self,
        title: str = "",
        short_title: str = "",
        year: int = datetime.datetime.now().year,
        authors: list[Author] = [],
        abstract: str = "",
        keywords: list[str] = [],
        content: str = "",
    ):
        self.title = title
        self.short_title = short_title
        self.authors = authors
        self.year = year
        self.abstract = abstract
        self.keywords = keywords
        self.content = content

    def add_section(self, section: Section):
        self.content += "\n" + str(section) + "\n"
        return self

    def add_subsection(self, subsection: Subsection):
        self.content += "\n" + str(subsection) + "\n"
        return self

    def add_keywords(self, *keywords):
        self.keywords = list(keywords)
        return self

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
        author_affil_tuple = []
        for author in self.authors:
            rendered_name = (
                ". ".join(name[0] for name in author.name.split(" "))
                + "."
                + " "
                + author.surname
            )

            all_affiliations = [
                *dict.fromkeys(a.affiliation for a in self.authors)
            ]  # preseves order and removes duplicates

            tuple_to_append = (
                rendered_name,
                all_affiliations.index(author.affiliation) + 1,
                author.is_corresponding,
            )

            author_affil_tuple.append(tuple_to_append)

        corresponders = list(filter(lambda a: a.is_corresponding, self.authors))

        if len(corresponders) == 1:
            corresponder = corresponders[0]
        elif len(corresponders) > 1:
            corresponder = corresponders[0]
            print(
                f"WARNING: There are {len(corresponders)} corresponding authors, only the first one will be used"
            )
        else:
            print("ERROR: No corresponding author found")
            exit(1)

        dict_to_return = {
            "title": self.title,
            "short_title": self.short_title,
            "year": self.year,
            "authors": self.authors,
            "authors_string": authors_string,
            "author_affil_tuple": author_affil_tuple,
            "affiliations": all_affiliations,
            "corresponder": corresponder,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "content": self.content,
        }

        return dict_to_return
