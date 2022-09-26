import argparse
import re
import sys

class Server:
    """Stores data for emails found in dataset
    
    Attributes:
        emails: A list of objects where each object corresponds
        to one email"""
    def __init__(self, path):
        """Creates server objects
        Arguments:
            self
            Path: path to the file we are going to read"""
        self.emails = []
        list1 = []
        with open(path) as f:
            data = ''
            for line in f:
                if line.startswith('\"Message-ID: '):
                    data += line
                if not line.startswith('\"Message-ID: '):
                    data += line
                if line.startswith(" End Email\""):
                    list1.append(data)
                    data  = " "
    
        for thing in list1:
            message_id = re.search(r"Message-ID:\s(.*)", thing)[1]
            date = re.search(r"Date:\s(\S{0,}.{0,})\s-",thing)[1]
            subject = re.search(r"Subject:\s(\S{0,}.{0,}\w{0,})",thing)[1]
            sender = re.search(r"From:(\s{0,}.+)",thing)[1]
            receiver = re.search(r"To:(\s{0,}.+)",thing)[1]
            body = re.search(r"(X-FileName:\s.*\n)((.*|\n)*)(End Email)", thing)[0]
            email = Email(message_id, date, subject, sender, receiver, body)
            self.emails.append(email)      
        
class Email:
    """Class that stores data related to individual email messages
    Attributes:
        message_id (str): message_id unique to each message
        date (str): date the message was sent
        subject (str): subject of message
        sender (str): sender of message
        receiver (str): receiver of message
        body (str): body of message"""
    def __init__(self, message_id, date, subject, sender, receiver, body):
        """creates instances of email class
        Arguments:
        message_id (str): message_id unique to each message
        date (str): date the message was sent
        subject (str): subject of message
        sender (str): sender of message
        receiver (str): receiver of message
        body (str): body of message"""
        self.message_id = message_id
        self.date = date
        self.subject = subject 
        self.sender = sender
        self.receiver = receiver
        self.body = body
        
def main(path):
    """Retrieves length of emails attribute of instance
    Arguments
    Path (str): string representing path of file text to be parsed
    
    Returns
        I=Length of emails attribute of instance (int)"""
    server = Server(path)
    return len(server.emails)
    
def parse_args(args_list):
    """
    Attributes
    args_list: list of strings containing command-line arguments for program
    
    Returns
    Argument parser created
    """
    p = argparse.ArgumentParser()
    p.add_argument('path', type=str, help='path')
    arg = p.parse_args(args_list)
    return arg
    
if __name__ == "__main__":
    arg = parse_args(sys.argv[1:])
    main(arg.path)