from latex import LatexEngine

from prompts import prompt_article

# Initialize the latex engine
latex = LatexEngine(
    template_folder="template",
    template_file="main.tex",
    output_folder="outputs",
    output_file="main.tex",
)

# Create an article
my_article = prompt_article()

# Write the article to a tex file (for debugging)
latex.write_tex(my_article)

# Build the article
pdf_path = latex.build(my_article)
