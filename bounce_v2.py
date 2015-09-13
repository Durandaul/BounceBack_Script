import imaplib
import re
import email as emlib
import json
import csv

mail = imaplib.IMAP4_SSL('imap.gmail.com')

regexMessage = b'Delivery to the following recipient failed permanently:\s{1,}.+\s'
find_bounce_back_message = re.compile(regexMessage)

regexEmail = b'.{1,}@.+'
find_email = re.compile(regexEmail)


def ok_detector(result, data):
    if result == 'OK':
        _data = data[0].split()
    try:
        rfc822 = [mail.uid('fetch', uid, '(RFC822)') for uid in _data]
        print "Retrieved UIDs"
        _data = [uid[1] for uid in rfc822]
        return _data

    except Exception as e:
        print "Error Occured"
        print e

def get_credentials(jsonfile='mySecret.json'):
    with open(jsonfile, 'rb') as jsonInFile:
        try:
            secrets = json.load(jsonInFile)
            password = secrets['password']
            print "Retrieved password"
            username = secrets['login']
            print "Retrieved Login"
            return username,password
        except Exception as e:
            print "Couldn't load JSON from file"
            print e

def login(username, password):
    return mail.login(username,password)


def pull_bounceback_messages(folder="BounceBack"):
    mail.select(folder)
    _result, _data = mail.uid('search', None, "ALL")
    _data = ok_detector(_result, _data)
    return _data

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def find_delivery_preamble(email):
    try:
        print email
        find_delivery_failed_message = find_bounce_back_message.search(email)
        print find_delivery_failed_message
        result = find_delivery_failed_message.group()
        message_delivery_notification = str(result)
        print message_delivery_notification
        return message_delivery_notification

    except Exception as e:
        print 'Couldn\'t find message delivery notification'
        return None

def find_email_address_in_preamble(message_delivery_notification):
    print "Find Email Address Function called once"
    print message_delivery_notification
    address_regex_search = find_email.search(message_delivery_notification)
    results = str(address_regex_search.group()).strip()
    print results
    return results

def csv_writer(email_address_list,verbose=True):
    if verbose:
        print "Writing to CSV"
    try:
        with open('BounceBackNames.csv', 'wb') as csvfile:
                output = csv.writer(csvfile, delimiter=' ')
                output.writerow('Email Address:')
                output.writerows(email_address_list)
        print "CSV File made"
    except Exception as e:
        print "Unable to write to output"
        print "Reason:"
        print e


def main():

    email_address_list = []
    credentials = get_credentials()
    username, password = credentials[0], credentials[1]
    try:
        login(username, password)
    except Exception as e:
        print "Couldn't logon:"
        print e

    data = pull_bounceback_messages()

    for email in data:
        email = emlib.message_from_string(email[0][1])
        email = get_first_text_block(email)
        print email
        message_delivery_notification = find_delivery_preamble(email)

        if message_delivery_notification != None:

            try:
                email_address = find_email_address_in_preamble(message_delivery_notification)
                email_address_list.append(email_address)

            except AttributeError as e:
                print "Couldn't find Email in string"


    if email_address_list != None:
        csv_writer(email_address_list)

    else:
        print " Uh... Talk to Max I guess?"

if __name__ == '__main__':
    main()