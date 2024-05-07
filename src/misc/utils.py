import re 

def strip_non_numeric(input_string):
    # Match only the numeric part of the string
    match = re.search(r'\d+', input_string)
    if match:
        return match.group()
    else:
        return ""  