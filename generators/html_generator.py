import os
from jinja2 import Environment, PackageLoader
from helpers.progress import Progress


class HTMLGenerator:
    env = Environment(loader=PackageLoader(__name__, 'templates'))
    html_folder =  "/home/fatconan/workspace/git-projects/eihell/output"
    resources_folder = "resources"
    basic_html_template = 'base.html'
    progress = Progress()

    def __init__(self):
        with open('table.json', 'rb') as data:
            self.data = data
        self.generate_pages()

    def render_template(self, template, data, outputfile):
        outputfileFull = os.path.join(self.html_folder, outputfile)
        folderPath = '/'.join(outputfileFull.split('/')[:-1])
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        template = self.env.get_template(template)
        with open(outputfileFull, 'wb') as output:
            output.write(template.render(data))

    def generate_pages(self):
        pass


