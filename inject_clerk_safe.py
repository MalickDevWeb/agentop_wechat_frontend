with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# S'assurer que 'use client' est en premier
content = content.replace("'use client'\n", "").replace("'use client';\n", "")
content = "'use client';\n" + content

# Ajouter import Clerk juste après 'use client'
if "useClerk" not in content:
    content = content.replace(
        "'use client';\n",
        "'use client';\nimport { useUser, useClerk } from '@clerk/nextjs';\n"
    )

# Remplacer la gestion du login: useState(false) → useUser
old = "const [loggedIn, setLoggedIn] = useState(false)"
new = """const { isLoaded, isSignedIn } = useUser()
  const { openSignIn, signOut } = useClerk()
  const loggedIn = isLoaded && isSignedIn"""
content = content.replace(old, new)

# Remplacer l'appel onLogin par openSignIn GitHub
content = content.replace("onLogin(selectedProfile)", "openSignIn({ appearance: { elements: { socialButtonsBlockButton__github: { display: 'flex' } } } })")
content = content.replace("onClick={()=>signIn('github')}", "onClick={()=>openSignIn()}")

# Ajouter loading state avant le check loggedIn
old_check = "if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />"
new_check = """if (!isLoaded) return (
    <div style={{minHeight:'100vh',background:'#030712',display:'flex',alignItems:'center',justifyContent:'center',color:'white'}}>
      <div style={{textAlign:'center'}}>
        <div style={{width:40,height:40,border:'3px solid #7c3aed',borderTopColor:'transparent',borderRadius:'50%',animation:'spin 0.8s linear infinite',margin:'0 auto 16px'}} />
        <p>Chargement de la plateforme Sonatel...</p>
      </div>
    </div>
  )
  if (!isSignedIn) return <Login onLogin={() => openSignIn()} />"""
content = content.replace(old_check, new_check)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Clerk injecté proprement dans page.tsx")
