import os

def writeFile(name, body):
    with open(name, 'w') as file:
        file.write(body)


def formatFile(self):
    filetext = "---"
    for key in self.frontmatter.keys():
        filetext += '\n%s: %s' % (key, self.frontmatter[key])
    filetext += '\n---\n%s' % self.body
    return filetext

class Article():
    def __init__(self, name="", frontmatter={}, body="", filename=""):
        self.frontmatter = frontmatter
        self.body = body

        if filename: self.filename =  filename
        else: self.filename = f"{self.frontmatter['title']}.md"

    def __str__(self):
        return formatFile(self)

class Category():
    def __init__(self, name="", frontmatter={}, body=""):
        self.name = name
        self.frontmatter = frontmatter
        self.children = []
        self.body = body

    def newArticle(self, name="", frontmatter={}, body="", filename=""):
        article = Article(name, frontmatter, body, filename)
        self.children.append(article)
        return article

    
    def newCategory(self, name="", frontmatter={}, body=""):
        category = Category(name, frontmatter, body)
        self.children.append(category)
        return category

    def save(self, parent_folder="."):
        folder_path = os.path.join(parent_folder, self.name)
        os.makedirs(folder_path, exist_ok=True)


        index_content = formatFile(self)
        index_file_path = os.path.join(folder_path, "_index.md")
        writeFile(index_file_path, index_content)

        for child in self.children:
            if isinstance(child, Article):
                child_file_path = os.path.join(folder_path, child.filename)
                writeFile(child_file_path, formatFile(child))

            elif isinstance(child, Category):
                child.save(folder_path)