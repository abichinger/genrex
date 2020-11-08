import genrex

emails = genrex.parse(r'(John|Jane)\.(Doe|Smith)@(gmail|outlook|protonmail)\.com')

print('random email address: ', emails.random())
print('first email address: ', emails[0])
print('number of email addresses: ', len(emails))

print('')
[print(email) for email in emails] #print all emails