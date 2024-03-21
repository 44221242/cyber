from easygui import enterbox


def chat(msg):
    client_Message = enterbox(msg, title="Message From Attacker")
    return client_Message
