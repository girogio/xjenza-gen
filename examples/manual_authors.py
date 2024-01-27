from article import Article, Author, Section
from latex import LatexEngine

# Initialize the latex engine
latex = LatexEngine(
    template_folder="template",
    template_file="main.tex",
    output_folder="outputs",
    output_file="main.tex",
)

# Create the authors
einstein = Author(
    "Albert",
    "Einstein",
    "albert@einstein.de",
    "Department of Physics, Faculty of Science, University of Malta, Malta",
).corresponding()

oppenheimer = Author(
    "Robert Julius",
    "Oppenheimer",
    "robbie@radioaktiv.com",
    "Department of Atomic Sciences, Faculty of Science, University of Malta, Malta",
)

schrodinger = Author(
    "Erwin",
    "Schrodinger",
    "cat_or_no_cat@both.com",
    "University of Vienna, Vienna, Austria",
)


authors = [einstein, oppenheimer, schrodinger]

my_article = (
    Article(
        title="An amazing paper",
        short_title="An amazing paper",
        authors=authors,
        year=2021,
        abstract="This is a test article",
    )
    .add_section(Section("Section 1", "Content 1"))
    .add_section(Section("Section 2", "Content 2"))
    .add_section(Section("Section 3", "Content 3"))
    .add_keywords("keyword1", "keyword2", "keyword3")
)


# Write the article to a tex file (for debugging)
latex.write_tex(my_article)

# Build the article
pdf_path = latex.build(my_article)
