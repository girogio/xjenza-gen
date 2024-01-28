import shutil
from cgi import test
from os import path
from time import sleep

from xjenza_gen.article import Article, Author
from xjenza_gen.latex import LatexEngine
from xjenza_gen.main import copy_skel


class TestProject(object):
    __test__ = False
    latex: LatexEngine
    inspect: bool

    def __init__(self, inspect: bool = False):
        self.inspect = inspect

    def __enter__(self):
        self.latex = copy_skel("xjenza_gen", "tests/test_article", False)
        return self

    def __exit__(self, *args):
        if not self.inspect:
            shutil.rmtree(path.abspath("tests/test_article"))


test_author = Author(
    name="Albert Ball Carter",
    email="john@doe.com",
    surname="Doe",
    affiliation="University of Malta",
    corresponding=True,
)

test_author2 = Author(
    name="Elena Francesca",
    email="elena@fran.com",
    surname="Galea",
    affiliation="University of Zobbi",
    corresponding=False,
)


test_article = Article(
    title="Test article",
    authors=[test_author, test_author2],
    abstract="This is an abstract",
    year=2021,
).add_keywords("test", "article")


def test_latex():
    with TestProject(inspect=True) as project:
        project.latex.write_tex(test_article)
        project.latex.compile_pdf()

        assert path.exists(path.abspath("tests/test_article/test_article.tex"))
