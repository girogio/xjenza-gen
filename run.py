from latexbuild import render_latex_template
from article import Article, Author

import os

PATH_JINJA2 = "./template/"
PATH_TEMPLATE_RELATIVE_TO_PATH_JINJA2 = f"main.tex"
FILE_NAME = 'main' # input("Enter file name: ")
os.environ["LATEX_FILE_NAME"] = FILE_NAME
PATH_OUTPUT_TEX = f"./outputs/{FILE_NAME}.tex"

# Check if path to template exists
assert os.path.exists(PATH_JINJA2), "Path to Jinja2 template does not exist"
assert os.path.isfile(
    os.path.join(PATH_JINJA2, PATH_TEMPLATE_RELATIVE_TO_PATH_JINJA2)
), "Path to template file does not exist"

def compile_tex_file(path: str):
    print(f"Compiling {path}... ", end="")
    os.system(f"pdflatex -output-directory outputs {path} > /dev/null 2>&1")
    print("Done")

def run_biber(path: str):
    print(f"Running biber on {path}... ", end="")
    os.chdir("./outputs")
    filename = os.path.basename(path)
    os.system(f"biber {filename} > /dev/null 2>&1")
    os.chdir("..")
    print("Done")

def write_tex_file(path: str, article: Article):
    content = render_latex_template(
        PATH_JINJA2, PATH_TEMPLATE_RELATIVE_TO_PATH_JINJA2, article.dict(), escape_latex=False)

    with open(path, "w") as f:
        f.write(content)
        f.close()

if __name__ == "__main__":

    # 3 random authors
    authors = [Author("John", "Doe", 'john@doe.com', 'University of Nowhere'),
                Author("Jane", "Doe", 'jane@doe.com', 'Univeraasity of Nowhere'),
                Author("Mark", "Dudinu", 'dudino@mark.com', 'University of Nowhere')]

    authors[2].is_corresponding = True

    article_name = 'A very interesting article'

    article = Article(article_name, authors=authors)

    write_tex_file(PATH_OUTPUT_TEX, article)

    compile_tex_file(PATH_OUTPUT_TEX)
    run_biber(PATH_OUTPUT_TEX.strip('.tex'))
    compile_tex_file(PATH_OUTPUT_TEX)
    compile_tex_file(PATH_OUTPUT_TEX)



