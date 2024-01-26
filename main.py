from article import Article, Author
from latex import LatexEngine

# Initialize the latex engine
latex = LatexEngine(
    template_folder="template",
    template_file="main.tex",
    output_folder="outputs",
    output_file="main.tex",
)

# Create an article
my_article = Article(title="A very interesting article", year=2023).authors_from_file(
    "authors.csv"
)

# Write the article to a tex file
latex.write_tex(my_article)

# Build the article
pdf_path = latex.build(my_article)

print(f"PDF saved to {pdf_path}")
