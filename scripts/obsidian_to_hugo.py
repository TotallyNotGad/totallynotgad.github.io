"""
Utilities to process obsidian notes and convert them to hugo ready content files.
"""

import os
from shutil import rmtree, copytree, ignore_patterns

from typing import TypedDict, List
import re

class ObsidianToHugo:
    """
    Process the obsidian vault and convert it to hugo ready content.
    """

    def __init__(self, obsidian_vault_dir: str, hugo_content_dir: str, processors: list = None, filters: list = None, ignoreDirs = None):
        self.obsidian_vault_dir = obsidian_vault_dir
        self.hugo_content_dir = hugo_content_dir

        self.processors = [replace_wiki_links, replace_md_marks]
        self.ignoreDirs = ['.git', '.obsidian']
        self.filters = []

        if processors:
            self.processors.extend(processors)
        if filters:
            self.filters.extend(filters)
        if ignoreDirs:
            self.ignoreDirs.extend(ignoreDirs)

    def run(self) -> None:
        """
        Delete the hugo content directory and copy the obsidian vault to the
        hugo content directory, then process the content so that the wiki links
        are replaced with the hugo links.

        # Clear old output folder and copy all non obsidian internal files to it
        rmtree(self.hugo_content_dir) 
        copytree(self.obsidian_vault_dir, self.hugo_content_dir, ignore=ignore_patterns('.obsidian')) 
        """

        for root, dirs, files in os.walk(self.obsidian_vault_dir):
            # Skip non-content folders
            dirs[:] = list(filter(lambda x: not x in self.ignoreDirs, dirs))

            for filePath in files: self.process_file(filePath)

    def process_file(self, filePath) -> None:
        """ Run all filters and processors on your notes files """ 
        if not filePath.endswith(".md"): return # ignore non markdown files

        # Read file contents
        with open(os.path.join(self.obsidian_vault_dir, filePath), "r", encoding="utf-8") as f:
            content = f.read()

        # Delete and skip any filtered files
        for filter in self.filters: 
            if filter(content, filePath): return

        # Run content through processors
        for processor in self.processors:
            content = processor(content, filePath)

        with open(os.path.join(self.hugo_content_dir, filePath), "w", encoding="utf-8") as f:
            f.write(content)

def replace_md_marks(text: str, path) -> str:
    """
    Replace all markdown marks in the given text with html marks.
    """
    
    md_marks_regex = r"==([^=\n]+)=="
    for match in re.finditer(md_marks_regex, text):
        text = text.replace(match.group(), f'<mark>{match.group(1)}</mark>')

    return text

WikiLink = TypedDict("WikiLink", {"wiki_link": str, "link": str, "text": str})


def get_wiki_links(text: str) -> List[WikiLink]:
    """
    Get all wiki links from the given text and return a list of them.
    Each list item is a dictionary with the following keys:
    - wiki_link: the exact match
    - link: the extracted link
    - text: the possible extracted text
    """
    wiki_links = []
    wiki_link_regex = r"\[\[(.*?)\]\]"
    for match in re.finditer(wiki_link_regex, text):
        out = {
            "wiki_link": match.group(),
        }

        if "\|" in match.group(1):
            out["link"], out["text"] = match.group(1).split("\|")
        elif "|" in match.group(1):
            out["link"], out["text"] = match.group(1).split("|")
        else:
            out["link"] = match.group(1)
            out["text"] = match.group(1)

        # if the link ends with `_index` remove it
        if out["link"].endswith("_index"):
            out["link"] = out["link"][:-6]

        wiki_links.append(out)
    return wiki_links


def wiki_link_to_hugo_link(wiki_link: WikiLink) -> str:
    """
    Convert the wiki link into a hugo link.
    """
    # if the links contains a link to a heading, convert the heading part to
    # lower case and replace spaces by minus
    link_seperated = wiki_link["link"].split("#", 1)
    if len(link_seperated) > 1:
        link_combined = "#".join(
            [link_seperated[0], link_seperated[1].lower().replace(" ", "-")]
        )
    else:
        link_combined = wiki_link["link"]
    hugo_link = f'[{wiki_link["text"]}]({{{{< ref "{link_combined}" >}}}})'
    return hugo_link


def replace_wiki_links(text: str, path) -> str:
    """
    Replace all wiki links in the given text with hugo links.
    """
    links = get_wiki_links(text)
    for link in links:
        hugo_link = wiki_link_to_hugo_link(link)
        text = text.replace(link["wiki_link"], hugo_link)
    return text
