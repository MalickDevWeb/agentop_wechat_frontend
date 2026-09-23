import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# On supprime tous les 'use client' existants
content = re.sub(r"^['\"]use client['\"];?\s*\n", "", content, flags=re.MULTILINE)

# On force 'use client' à la toute première ligne
content = "'use client';\n" + content

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
