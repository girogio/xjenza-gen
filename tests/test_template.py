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
    debug: bool

    def __init__(self, inspect: bool = True, debug=False):
        self.inspect = inspect
        self.debug = debug

    def __enter__(self):
        self.latex = copy_skel("xjenza_gen", "tests/test_article", self.debug)
        return self

    def __exit__(self, *args):
        if not self.inspect:
            shutil.rmtree(path.abspath("tests/test_article"))


test_author = Author(
    name="Albert Ball Carter",
    email="john@doe.com",
    surname="Doe",
    affiliation="University of Malta",
    is_corresponding=True,
)

test_author2 = Author(
    name="Elena Francesca",
    email="elena@fran.com",
    surname="Galea",
    affiliation="University of Zobbi",
    is_corresponding=False,
)


test_article = Article(
    title="Test article",
    authors=[test_author, test_author2],
    abstract="This is an abstract",
    year=2021,
).add_keywords("test", "article")


def test_tex_file_creation():
    with TestProject(inspect=True) as project:
        project.latex.write_tex(test_article)

        assert path.exists(path.abspath("tests/test_article/test_article.tex"))
