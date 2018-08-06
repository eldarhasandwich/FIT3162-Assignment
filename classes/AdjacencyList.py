
class Recipient:
    def __init__(self, _id, _emailAddress, _emailCount):
        self.id = _id
        self.emailAddress = _emailAddress
        self.emailCount = _emailCount

    def UpdateEmailCount(self, newEmailCount):
        self.emailCount = newEmailCount

class Sender:
    def __init__(self, _id, _emailAddress):
        self.id = _id
        self.emailAddress = _emailAddress
        self.recipients = {}

    def AddRecipient(self, recipientID, recipientAddress, emailCount):
        newRecipient = Recipient(recipientID, recipientAddress, emailCount)
        self.recipients.append(newRecipient)

class AdjacencyList:
    def __init__(self):
        self.senders = {}

    def AddSender(self, senderID, email):
        newSender = Sender(senderID, email)
        self.senders.append(newSender)

    def AddSenderRecipientPair(self, _senderID, _senderAddress, _recipientID, _recipientAddress):

        for key, sender in self.senders.items():
            if sender.id == _senderID:
                for key, recipient in sender.recipients.items():
                    if recipient.id == _recipientID:
                        recipient.UpdateEmailCount(recipient.emailCount + 1)
                        break
                    else: pass
                sender.AddRecipient(_recipientID, _recipientAddress, 1)
                break
            else: pass

        newSender = Sender(_senderID, _senderAddress)
        newRecipient = Recipient(_recipientID, _recipientAddress, 1)
        newSender[str(recipientAddress)] = newRecipient
        self.senders[str(_senderID)] = newSender

        print(self.senders)

    

