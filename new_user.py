from cork import Cork
from datetime import datetime

aaa = Cork('auth')
username = 'user'
password = 'password'
tstamp = str(datetime.utcnow())
aaa._store.users[username] = {
    'role': 'admin',
    'hash': aaa._hash(username, password),
    'email_addr': username + '@localhost.local',
    'desc': username + ' test user',
    'creation_date': tstamp
}
aaa._store.save_users()
