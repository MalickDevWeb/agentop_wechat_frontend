content = open("app/page.tsx", "r", encoding="utf-8").read()

# Ajouter l'import NextAuth au tout debut
if "next-auth/react" not in content:
    content = "'use client';\nimport { signIn, signOut, useSession } from 'next-auth/react';\n" + content.replace("'use client';\n", "").replace("'use client'\n", "")

# Remplacer la gestion de loggedIn par useSession
old = "const [loggedIn, setLoggedIn] = useState(false)"
new = """const { data: session, status } = useSession()
  const loggedIn = status === 'authenticated'"""
content = content.replace(old, new)

# Remplacer le onLogin dans les profiles par signIn
old2 = "onLogin(selectedProfile)"
new2 = "signIn('github')"
content = content.replace(old2, new2)

# Remplacer le bouton github dans Login
old3 = "onClick={()=>onLogin(selectedProfile)}"
new3 = "onClick={()=>signIn('github')}"
content = content.replace(old3, new3)

open("app/page.tsx", "w", encoding="utf-8").write(content)
print("✅ NextAuth injecté dans page.tsx")
