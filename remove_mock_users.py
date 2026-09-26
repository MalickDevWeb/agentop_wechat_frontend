import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

old_users = """  const [allUsers, setAllUsers] = useState<any[]>([
    { id: 'usr_1', name: 'Papa Malick TEUW', email: 'malickteuw.devweb@gmail.com', role: 'ADMIN', perms: { submit: true, auto_learn: true, publish: true } },
    { id: 'usr_2', name: 'Marie Fall', email: 'marie.fall@orange-sonatel.com', role: 'DEV', perms: { submit: true, auto_learn: false, publish: false } },
    { id: 'usr_3', name: 'Amadou Diop', email: 'amadou.diop@orange-sonatel.com', role: 'DEV', perms: { submit: true, auto_learn: false, publish: true } },
    { id: 'usr_4', name: 'Ousmane Sow', email: 'ousmane.sow@orange-sonatel.com', role: 'DEV', perms: { submit: false, auto_learn: false, publish: false } }
  ]);"""

new_users = """  const [allUsers, setAllUsers] = useState<any[]>([
    { id: 'usr_1', name: 'Papa Malick TEUW', email: 'malickteuw.devweb@gmail.com', role: 'ADMIN', perms: { submit: true, auto_learn: true, publish: true } }
  ]);"""

content = content.replace(old_users, new_users)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
