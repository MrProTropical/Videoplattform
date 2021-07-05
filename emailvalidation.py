import re

def validateEmail(email):
    return re.match(r"[\w-]{1,20}@\w{2,20}\.\w{2,3}$", email)
email = "hanswurst@gmail.com"
valid = validateEmail(email)
if valid:
    print(email, "is correct")
else:
    print("invalid email format:", email)
    