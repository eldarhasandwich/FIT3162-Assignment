
class Recipient:
    def __init__(self, _id, _emailCount):
        self.id = _id
        self.emailCount = _emailCount

class Sender:
    def __init__(self, _id, _email):
        self.id = _id
        self.email = _email
        self.recipients = []

    def AddRecipient(self, recipientID, emailCount):
        newRecipient = Recipient(recipientID, emailCount)
        self.recipients.append(newRecipient)

class AdjacencyList:
    def __init__(self):
        self.senders = []

    def AddSender(self, senderID, email):
        newSender = Sender(senderID, email)
        self.senders.append(newSender)

