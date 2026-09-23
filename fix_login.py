import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. On supprime l'écran de protection générique moche que j'avais mis
generic_protection = r"export default function Page\(\) \{.*?return \(\s*<>\s*<SignedOut>.*?</SignedIn>\s*</>\s*\)\s*\}"
content = re.sub(generic_protection, "", content, flags=re.DOTALL)

# 2. On renomme MainApp en Page (le nom original)
content = content.replace("function MainApp() {", "export default function Page() {")

# 3. On remplace la fausse logique de Login par la logique Clerk
# Dans l'ancien code, il y avait: const [loggedIn, setLoggedIn] = useState(false)
# et if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />

# On importe useUser de Clerk
if "useUser" not in content:
    content = content.replace("import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';", "import { SignedIn, SignedOut, SignInButton, UserButton, useUser } from '@clerk/nextjs';")

# On remplace l'état loggedIn par la vérification Clerk
old_state = r"const \[loggedIn, setLoggedIn\] = useState\(false\)"
new_state = """const { isLoaded, isSignedIn, user } = useUser()
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    if (isSignedIn && user) {
       // Synchronisation avec le backend pour initier l'admin
       fetch(`${API_URL}/auth/sync`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress, name: user.fullName })
       }).then(r=>r.json()).then(data => setIsAdmin(data.role === 'ADMIN')).catch(e=>console.log(e))
    }
  }, [isSignedIn, user])"""
content = re.sub(old_state, new_state, content)

# On modifie le return de la Page pour utiliser le vrai composant Login mais sécurisé
old_return = r"if \(!loggedIn\) return <Login onLogin=\{\(\) => setLoggedIn\(true\)\} />"
new_return = """if (!isLoaded) return <div className="min-h-screen bg-[#030712] flex items-center justify-center text-white">Chargement sécurisé...</div>
  
  if (!isSignedIn) return (
    <SignInButton mode="modal" forceRedirectUrl="/">
       {/* On enveloppe votre magnifique composant Login pour que n'importe quel clic déclenche Clerk */}
       <div className="cursor-pointer hover:opacity-95 transition-opacity">
         <Login onLogin={() => {}} />
       </div>
    </SignInButton>
  )"""
content = re.sub(old_return, new_return, content)

# 4. On modifie le Header pour afficher le statut ADMIN (facultatif mais pro)
admin_badge = """<div className="flex items-center gap-3">
              {isAdmin && <span className="px-2 py-1 bg-amber-500/20 text-amber-400 text-xs rounded border border-amber-500/30">Admin</span>}
              <UserButton afterSignOutUrl="/"/>
            </div>"""
content = content.replace('<UserButton afterSignOutUrl="/"/>', admin_badge)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
