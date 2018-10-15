from dataset_to_textfile import Clusters

group_output = open("group_output.txt", 'w')
enron_groups = Clusters()
f = open("enron_output.txt", 'r')
text = f.read()
f.close()
lines = text.split("\n")
text_to_remove = "Email sent by "
N = len(text_to_remove)
new_lines = []
for line in lines:
    new_line = line[N:]
    new_lines.append(new_line)


for a_string in new_lines:
    sender = None
    new_str = ""
    for char in a_string:
        if char != " ":
            new_str += char
        else:
            sender = new_str
            break
    M = len(" to ")
    K = len(sender)
    V = M + K
    receivers = a_string[V:]
    receiver_list = receivers.split(',')
    members = []
    members.append(sender)
    for receiver in receiver_list:
        members.append(receiver)
    enron_groups.add(members)

print(enron_groups.dyad_count())
print(enron_groups.triad_count())
