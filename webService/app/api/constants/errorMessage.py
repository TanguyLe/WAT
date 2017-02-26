

class ErrorMessage:
    EXISTS_ALREADY = "Such {name} already exists"
    DOESNT_EXIST = "{name} doesn't exist"
    VALUE = "Incorrect JSON body"
    KEY = "Key error in JSON body"
    PASSWORD = "Wrong password"
    USER_IN_CONVERSATION = "User already participating in the conversation"
    USER_NOT_IN_CONVERSATION = "User doesn't participate in this conversation"
    NO_USER_OR_POSITION = "User doesn't exist or doesn't have a position recorded"
