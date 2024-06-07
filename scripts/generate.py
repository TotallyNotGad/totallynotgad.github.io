import os, dotenv, content, pprint, shutil
import githubContent

# Load Enviornment Variables
dotenv.load_dotenv()

# Set Up GitHub Profile
token = os.getenv('GH_TOKEN')
username = os.getenv('GH_USERNAME')
ghProfile = githubContent.GithubProfile(token, username)

root = content.Category("content", {
    'title': "Home"
}, ghProfile.authorBlurb)

root.newArticle(frontmatter={
  "title": "404 Not Found",
  "date": "None"
}, body="Sorry, the page your looking for cannot be found", filename="404.md")

#
postsCategory = root.newCategory("posts", {'title': 'Posts'})
projectsCategory = root.newCategory("projects", {'title': 'Projects'})

for repository in ghProfile.pinnedProjects:
    article = projectsCategory.newArticle(frontmatter = {
        'title': repository['name'],
        'date': repository['updatedAt'],
        'summary': repository['description'],
        'homepage': repository['homepageUrl'],
        'projectPage': 'https://github.com/' + username + '/' + repository['name'], 
    }, body = repository['object']['text'])

root.save()

shutil.rmtree('./temp', ignore_errors=True)
os.system('git clone ' + os.getenv('BLOG_REPO') + " temp")

from obsidian_to_hugo import ObsidianToHugo
import subprocess

def addFrontmatter(text, path):
    # Split out summary from article if a summarry exists
    splitArticle = text.split("---")
    if len(splitArticle) >= 2:
      summary = splitArticle[0].lstrip()
      body = '---'.join(splitArticle[1:])
    else:
      summary = ""
      body = text

    lastUpdated = subprocess.run(['cd temp && git log --pretty="format:%ct" "' + path + '"' + " | head -1"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    publishedDate = subprocess.run(['cd temp && git log --pretty="format:%ct" --reverse "' + path + '"' + " | head -1"], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    # Return a formatted article with the frontmatter added
    return str(content.Article(frontmatter = {
      'title': path.split('.')[0],
      'summary': summary,
      'date': str(publishedDate),
      'lastUpdated': str(lastUpdated)
    }, body = body))

obsidian_to_hugo = ObsidianToHugo(
    obsidian_vault_dir="./temp",
    hugo_content_dir="./content/posts",
    processors=[addFrontmatter]
)

obsidian_to_hugo.run()