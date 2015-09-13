This is a simple script that will:

- Connect to gmail via IMAP
- Pull creds from a pre-formatted json file, MySecret.json
- Authenticate and choose a folder
- Use a regex to find "Delivery Notitifcation failed" messages 
- and a second regex to pull the actual email of the following line
- lasty, putting it into a CSV. 


This script assumes you've made the following filter in gmail:

Matches: from:(mailer-daemon@googlemail.com) subject:(Delivery Status Notification (Failure))
Do this: Skip Inbox, Mark as read, Apply label "BounceBack", Never send it to Spam, Mark it as important

The label is important since IMAP chooses folders to read and labels are folders for the purpose of IMAP. Which actually makes a bit of sense. 


It's just made for a friend out of all python standard lib, so nothing 
fancy to import

I'll try to over-complicate it later ;)

Enjoy!
