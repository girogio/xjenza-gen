import subprocess

from os import path
from article import Article
from latexbuild import render_latex_template


class LatexEngine:
    """This class is responsible for building the final PDF document from the given Article object."""

    template_folder: str
    template_file: str
    output_folder: str
    output_file: str

    def __init__(
        self,
        template_folder: str,
        template_file: str,
        output_folder: str,
        output_file: str,
    ):
        assert path.exists(template_folder), "Path to Jinja2 template does not exist"
        assert path.isfile(
            path.join(template_folder, template_file)
        ), "Path to template file does not exist"

        self.template_folder = template_folder
        self.template_file = template_file
        self.output_folder = output_folder
        self.output_file = output_file

    def write_tex(self, article: Article):
        """This method writes the content of the Article object to a .tex file, using the Jinja2 template engine."""
        content = render_latex_template(
            self.template_folder, self.template_file, article.dict(), escape_latex=False
        )

        with open(path.join(self.output_folder, self.output_file), "w") as f:
            f.write(content)
            f.close()

    def compile_pdf(self):
        """This method runs the pdflatex command on the generated .tex file."""
        print(f"Compiling {self.template_file}... ", end="")
        subprocess.run(
            ["pdflatex", "-output-directory", self.output_folder, self.output_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print("Done")

    def run_biber(self):
        """This method runs the biber command on the generated .tex file."""
        print(
            f"Running biber on {path.join(self.output_folder, self.output_file)}... ",
            end="",
        )
        pid = subprocess.run(
            ["biber", self.output_file.strip(".tex")],
            cwd=self.output_folder,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print("Done")

        return pid

    def build(self, article: Article) -> str:
        """
        This method is responsible for building the final PDF document from the given Article object.

        It performs the following steps:
        1. Writes the content of the Article object to a .tex file.
        2. Compiles the .tex file into a .pdf file.
        3. Runs the biber command to process the bibliography in the .tex file.
        4. Compiles the .tex file into a .pdf file two more times. This is necessary as LaTeX sometimes requires multiple passes to resolve all references correctly.

        Args:
            article (Article): The Article object containing the content to be written to the .tex file.

        Returns:
            path of the generated PDF file
        """
        self.write_tex(article)
        self.compile_pdf()
        self.run_biber()
        self.compile_pdf()
        self.compile_pdf()

        return path.join(self.output_folder, self.output_file.strip(".tex") + ".pdf")
