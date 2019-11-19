class Issue:
    def __init__(self, payload):
        issue = payload['issue']
        fields = issue['fields']
        self.id = issue['id']
        self.url = issue['self']
        self.key = issue['key']
        self.priority = fields['priority']['name']
        self.creator_username = fields['creator']['name']
        self.creator_displayname = fields['creator']['displayName']
        self.reporter_username = fields['reporter']['name']
        self.reporter_displayname = fields['reporter']['displayName']
        self.type = fields['issuetype']['name']
        self.project_key = fields['project']['key']
        self.project_name = fields['project']['key']
        self.summary = fields['summary']
        self.description = fields['description']
        self.type = fields['issuetype']['name']
        self.attachment = fields['attachment']
        self.due_date = fields['duedate']
