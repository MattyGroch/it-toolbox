class Issue:
    def __init__(self, payload):
        # issue = payload['issue']
        # fields = issue['fields']

        issue = payload.get("issue", {})
        fields = issue.get("fields", {})

        # self.id = issue['id']
        # self.key = issue['key']
        # self.priority = fields['priority']['name']
        # self.creator_id = fields['creator']['accountId']
        # self.creator_displayname = fields['creator']['displayName']
        # self.reporter_id = fields['reporter']['accountId']
        # self.reporter_displayname = fields['reporter']['displayName']
        # self.type = fields['issuetype']['name']
        # self.project = fields['project']['key']
        # self.summary = fields['summary']
        # self.description = fields['description']
        # self.type = fields['issuetype']['name']
        # self.attachment = fields['attachment']
        # self.due_date = fields['duedate']

        self.id = issue.get("id")
        self.key = issue.get("key")
        self.priority = fields.get("priority", {}).get("name")
        self.creator_id = fields.get("creator", {}).get("accountId")
        self.creator_email = fields.get("creator", {}).get("emailAddress")
        self.creator_displayname = fields.get("creator", {}).get("displayName")
        self.reporter_id = fields.get("reporter", {}).get("accountId")
        self.reporter_email = fields.get("reporter", {}).get("emailAddress")
        self.reporter_displayname = fields.get("reporter", {}).get("displayName")
        self.type = fields.get("issuetype", {}).get("name")
        self.project = fields.get("project", {}).get("key")
        self.summary = fields.get("summary")
        self.description = fields.get("description")
        self.type = fields.get("issuetype", {}).get("name")
        self.attachment = fields.get("attachment")
        self.due_date = fields.get("duedate")


class Employee:
    def __init__(self, payload):
        # fields = payload['issue']['fields']
        
        fields = payload.get("issue", {}).get("fields")

        # self.wage_type = fields['customfield_10161']['value']
        # self.wage_amount = fields['customfield_10162']
        # self.email = fields['customfield_10163']
        # self.phone = fields['customfield_10164']
        # self.flsa = fields['customfield_10165']['value']
        # self.address1 = fields['customfield_10150']
        # self.address2 = fields['customfield_10151']
        # self.city = fields['customfield_10152']
        # self.state = fields['customfield_10153']['value']
        # self.zip = fields['customfield_10154']
        # self.title = fields['customfield_10167']
        # self.department = fields['customfield_10149']['value']
        # self.firstname = fields['customfield_10142']
        # self.lastname = fields['customfield_10143']
        # self.preferredname = fields['customfield_10144']
        # self.pronouns = fields['customfield_10170']
        # self.manager = fields['customfield_10145']['displayName']
        # self.manager_username = fields['customfield_10145']['name']
        # self.manager_email = self.manager_username + "@snapsheet.me"
        # self.location = fields['customfield_10146']['value']
        # self.cell_reimburse = fields['customfield_10168']['value']
        # self.internet_reimburse = fields['customfield_10169']['value']
        # self.start_date = fields['duedate']

        self.wage_type = fields.get("customfield_10161", {}).get("value")
        self.wage_amount = fields.get("customfield_10162")
        self.email = fields.get("customfield_10163")
        self.phone = fields.get("customfield_10164")
        self.flsa = fields.get("customfield_10165", {}).get("value")
        self.address1 = fields.get("customfield_10150")
        self.address2 = fields.get("customfield_10151")
        self.city = fields.get("customfield_10152")
        self.state = fields.get("customfield_10153", {}).get("value")
        self.zip = fields.get("customfield_10154")
        self.title = fields.get("customfield_10167")
        self.department = fields.get("customfield_10149", {}).get("value")
        self.firstname = fields.get("customfield_10142")
        self.lastname = fields.get("customfield_10143")
        self.preferredname = fields.get("customfield_10144")
        self.pronouns = fields.get("customfield_10170")
        self.manager = fields.get("customfield_10145", {}).get("displayName")
        self.manager_id = fields.get("customfield_10145", {}).get("accountId")
        self.manager_email = fields.get("customfield_10145", {}).get("emailAddress")
        self.location = fields.get("customfield_10146", {}).get("value")
        self.cell_reimburse = fields.get("customfield_10168", {}).get("value")
        self.internet_reimburse = fields.get("customfield_10169", {}).get("value")
        self.start_date = fields.get("duedate")
