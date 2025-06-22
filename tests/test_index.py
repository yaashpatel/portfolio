import io
from html.parser import HTMLParser
from pathlib import Path

class SectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.capture_section = False
        self.title = ""
        self.sections = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "h2":
            self.capture_section = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h2":
            self.capture_section = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.capture_section:
            self.sections.append(data.strip())


def test_index_contents():
    parser = SectionParser()
    html_text = Path("index.html").read_text(encoding="utf-8")
    parser.feed(html_text)

    assert parser.title.strip() == "Yash Patel | Portfolio"

    assert any(
        section.startswith("About")
        for section in parser.sections
    ), "About section missing"
    assert any(
        section.startswith("Projects")
        for section in parser.sections
    ), "Projects section missing"
