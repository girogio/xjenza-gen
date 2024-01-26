from article import Article, Author
from latex import LatexEngine

# Initialize the latex engine
latex = LatexEngine(
    template_folder="template",
    template_file="main.tex",
    output_folder="outputs",
    output_file="main.tex",
)

# Create some authors
authors = [
    Author("John", "Doe", "john@doe.com", "University of Malta").corresponding(),
    Author("Jane", "Doe", "jane@doe.com", "Univerity of Nowhere"),
    Author("Mark", "Dudinu", "dudino@mark.com", "University of Nowhere"),
]

# Create an article
my_article = Article("A very interesting article", authors=authors)

# Write the article to a tex file
latex.write_tex(my_article)

# Build the article
pdf_path = latex.build(my_article)

print(f"PDF saved to {pdf_path}")
