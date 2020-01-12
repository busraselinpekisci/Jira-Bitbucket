from jira import JIRA
from atlassian import Bitbucket

jiraOptions = {"server": "http://localhost/jira"}
jiraBasicAuth = ('admin', '1234')

try:
    jira = JIRA(options=jiraOptions, basic_auth=jiraBasicAuth)
    bbucket = Bitbucket(url='http://localhost/bitbucket', username='admin', password=1234)
    # BR anahtarina sahip statusu To Do olan issuelari ceker
    issues = jira.search_issues(jql_str="project = BR AND status = 'To Do'")
    # BR anahtarina sahip bir proje Bitbucket da varsa bu kismi yapar
    if not bbucket.project(key="BR").get("errors"):
        # Her issue icin Bitbucketda repo olusturup Jirada da bu issueya ait statusu Done yapar
        for issue in issues:
            bbucket.create_repo(project_key="BR", repository=issue.fields.customfield_10001)
            jira.transition_issue(issue=issue, transition="DONE")
    # BR anahtarina sahip bir proje Bitbucketda yoksa bu kismi yapar
    else:
        # To Do statusuna ait tüm issuelar icin yapar
        for issue in issues:
            # BR anahtarina sahip bir sonraki issue icin Bitbucketda aynı projeyi tekrar oluşturmamak adina bu kontrolu yapar
            # BR anahtarina sahip bir proje Bitbucketda yoksa bu kısmı yapar
            if bbucket.project(key="BR").get("errors"):
                bbucket.create_project(key="BR", name=issue.fields.customfield_10000)
                bbucket.create_repo(project_key="BR", repository=issue.fields.customfield_10001)
                jira.transition_issue(issue=issue, transition="DONE")
            # BR anahtarına sahip bir proje Bitbucket da varsa bu kısmı yapar
            else:
                bbucket.create_repo(project_key="BR", repository=issue.fields.customfield_10001)
                jira.transition_issue(issue=issue, transition="DONE")
except Exception as e:
    print(e)
