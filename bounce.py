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

def multipart_detector(maintype):
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
            elif maintype == 'text':
                return email_message_instance.get_payload()


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

def main(password):

    _login = "max.humphrey@gmail.com"
    mail.login(_login,password)
    mail.select("BounceBack")

    _result, _data = mail.uid('search', None, "ALL")
    _data = ok_detector(_result, _data)
    #_sender_message = []   Fix so that it's the message and the email
    _email = []
    _errors, _success = 0,0

    for email in _data:

        _email_response = emlib.message_from_string(email[0][1])
        _email_response = str(_email_response)

        try:
            _find_delivery_failed_message = find_bounce_back_message.search(_email_response)
            _delivery_failed = str(_find_delivery_failed_message.group())

            print "Found Match"
            try:
                _email_address = find_email.search(_delivery_failed)
                _email_address = _email_address.group()
                _email_address_stringified =str(_email_address)
                _email_address_stringified = _email_address_stringified.strip()
                print _email_address_stringified
                _results.append(_email_address_stringified)
                _success += 1
            except AttributeError as e:
                print "Couldn't find Email in string"

        except AttributeError as e :
            pass
             
    if _results != None:
        _results_size = len(_results)
        with open('BounceBackNames.csv', 'wb') as csvfile:
            output = csv.writer(csvfile, delimiter=' ')
            output.writerow('Email Address:')
            output.writerows(_results)

    else:
        print " Uh... Talk to Max I guess?"

if __name__ == '__main__':

    with open('mySecret.json', 'rb') as jsonInFile:
        try:
            password =json.load(jsonInFile)['password']
            print "Password Retrievel successful"
        except Exception as e:
            print e
    main(password)