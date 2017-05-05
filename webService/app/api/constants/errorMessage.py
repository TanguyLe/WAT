

class ErrorMessage:
    EXISTS_ALREADY = "Such {name} already exists"
    DOESNT_EXIST = "{name} doesn't exist"
    VALUE = "Incorrect JSON body"
    KEY = "Key error in JSON body"
    PASSWORD = "Wrong password"
    TIMEOUT = "User not connected anymore"
    INCORRECT_TOKEN = "Wrong API Token"
    USER_IN_CONVERSATION = "User already participating in the conversation"
    USER_NOT_IN_CONVERSATION = "User doesn't participate in this conversation"
    NO_POSITION = "User doesn't have a position recorded"

    INTEGRITY_ERROR = "The data you're trying to insert is not correct : {error}"
    PROGRAMMING_ERROR = "The way you're trying to insert the data is wrong : {error}"
    UNKNOWN_ERROR = "Unknown Error"
