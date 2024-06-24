# response_formatter.py
# may only be needed when using Claude Opus
# we are using Claude Sonnet 3.5
def extract_reply(reply):
    start_tag = "<reply>"
    end_tag = "</reply>"
    start_index = reply.find(start_tag) + len(start_tag)
    end_index = reply.find(end_tag)
    if start_index != -1 and end_index != -1:
        return reply[start_index:end_index].strip()
    return reply