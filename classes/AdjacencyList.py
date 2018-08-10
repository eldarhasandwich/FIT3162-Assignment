
# from databaseController import *

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
        self.recipients[str(recipientID)] = newRecipient

class AdjacencyList:
    def __init__(self):
        self.senders = {}

    # def AddSender(self, senderID, email):
    #     newSender = Sender(senderID, email)
    #     self.senders.append(newSender)

    def AddSenderRecipientPair(self, _senderID, _senderAddress, _recipientID, _recipientAddress, _value = 1, _incrementValue = True):

        for key, sender in self.senders.items():
            if sender.id == _senderID:
                for key, recipient in sender.recipients.items():
                    if recipient.id == _recipientID:
                        if _incrementValue:
                            recipient.UpdateEmailCount(recipient.emailCount + _value)
                        else:
                            recipient.UpdateEmailCount(_value)
                        return
                    else: pass
                sender.AddRecipient(_recipientID, _recipientAddress, _value)
                return
            else: pass

        newSender = Sender(_senderID, _senderAddress)
        newRecipient = Recipient(_recipientID, _recipientAddress, _value)
        newSender.recipients[str(_recipientID)] = newRecipient
        self.senders[str(_senderID)] = newSender

        
    

