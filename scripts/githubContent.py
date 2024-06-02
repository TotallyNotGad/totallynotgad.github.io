import requests

url = "https://api.github.com/graphql"

def graphqlQueary(url, token, query):
    response = requests.post(url=url, json={"query": query}, headers= \
      {
        "Authorization": "Bearer %s" % str(token).strip(),
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/124.0"
      })
    return (response.json(), response.status_code)

class GithubProfile():
    def __init__(self, token, username):
        self.token = token
        self.username = username

        self.authorBlurb = self.getAuthorBlurb()
        self.pinnedProjects = self.getPinnedProjects()

    def getAuthorBlurb(self):
        query = """{
              user(login: "%s") {
                repository(name: "%s") {
                    object(expression: "HEAD:README.md") {
                        ... on Blob {
                            text
                        }
                    }
                }
            }
        }""" % (self.username, self.username.lower())

        return graphqlQueary(url, self.token, query) \
                [0]['data']['user']['repository']['object']['text']

    def getPinnedProjects(self):
        query = """{
            user(login: "%s") {
              pinnedItems(first: 10, types: REPOSITORY) {
                nodes {
                  ... on Repository {
                    name
                    description
                    updatedAt
                    homepageUrl
                    object(expression: "HEAD:README.md") {
                      ... on Blob {
                        text
                      }
                    }
                  }
                }
              }
            }
        }""" % self.username

        return graphqlQueary(url, self.token, query) \
                            [0]['data']['user']['pinnedItems']['nodes']