This is a simple script that will:

- Connect to gmail via IMAP
- Pull creds from a pre-formatted json file, MySecret.json
- Authenticate and choose a folder
- Use a regex to find "Delivery Notitifcation failed" messages 
- and a second regex to pull the actual email of the following line
- lasty, putting it into a CSV. 

It's just made for a friend out of all python standard lib, so nothing 
fancy ;) 

I'll try to complicate it later ;)
