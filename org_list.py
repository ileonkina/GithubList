import xmlrpclib
import requests
import json

from conf import SPACE
from conf import TOP_PAGE
from conf import WIKI_USER
from conf import WIKI_PASS
from conf import page_name
from conf import wiki_url
from conf import org_name
from conf import use_token
from conf import oauth_token
from conf import github_login
from conf import github_pass

class getList:
    wiki_server = xmlrpclib.ServerProxy(wiki_url)
    wiki_token = wiki_server.confluence1.login(WIKI_USER, WIKI_PASS)
        
    def get_list(self,list_url):
        """
        get_list()
        
        This function get 
        """
        #list_url = "https://api.github.com/orgs/%s/repos" % org_name
        auth_type = ""
        if use_token:
            list_url += "?access_token=" + oauth_token
        else:
            auth_type = (github_login, github_pass)
        r = requests.get(url = list_url, auth = auth_type)
        if (r.status_code == requests.codes.OK):
            return json.loads(r.content)
        else:
            print r.headers
            return None
    
    def request(self, content, name_page, wiki_token, wiki_server):
            """
            request(content, name_page, wiki_token, wiki_server)
            This function sends the content to the specified wiki page
            and create a new page, if this page does not exist
            Input:
            content - Required unicode
            name_page - Required unicode
            wiki_token - Required string
            wiki_server - Required instance
            """
            try:
                page = wiki_server.confluence1.getPage(wiki_token, SPACE, name_page)
            except:
                parent = wiki_server.confluence1.getPage(wiki_token, SPACE, TOP_PAGE)
                #table_headers = "h1. News Feed (UTC) \n ||id||Date||Author||Event Type||\n"
                page = {
                      'parentId': parent['id'],
                      'space': SPACE,
                      'title': name_page,
                      'content': content
                      }
                wiki_server.confluence1.storePage(wiki_token, page)
            else:
                page['content'] = content
                wiki_server.confluence1.updatePage(wiki_token, page, {'versionComment':'','minorEdit':1})
                

    def main(self):
        list_url = "https://api.github.com/orgs/%s/repos" % org_name
        repos = self.get_list(list_url)
        content = ""
        print repos
        for i,repo in enumerate(repos):
            list_url = "https://api.github.com/repos/%s/%s/teams" % (org_name, repo['name'])
            teams = self.get_list(list_url)
            content += "h1.%s \n" % repo['name']
            for j,team in enumerate(teams):
                content += "|| %s |" % team['name']
                list_url = "https://api.github.com/teams/%s/members" % team['id']
                users = self.get_list(list_url)
                if users != []:
                    for k,user in enumerate(users):
                        content += user['login'] + ", "
                    content = content[:-2]
                content += " |\n"
            content += "\n"
        self.request(content, page_name, self.wiki_token, self.wiki_server)
        
getList = getList()
getList.main()        