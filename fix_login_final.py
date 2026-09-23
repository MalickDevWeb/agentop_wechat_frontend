import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# On supprime tout le code de la fausse fonction Page existante avec ses bugs
# et on la réécrit proprement.
content = re.sub(r"export default function Page\(\) \{.*$", "", content, flags=re.DOTALL)

nouvelle_page = """export default function Page() {
  const { isLoaded, isSignedIn, user } = useUser()
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    if (isSignedIn && user) {
       fetch(`${API_URL}/auth/sync`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress, name: user.fullName })
       }).then(r=>r.json()).then(data => setIsAdmin(data.role === 'ADMIN')).catch(e=>console.log(e))
    }
  }, [isSignedIn, user])

  if (!isLoaded) {
    return <div className="min-h-screen bg-[#030712] flex flex-col items-center justify-center text-white"><Sparkles className="w-8 h-8 text-purple-500 animate-pulse mb-4"/><span>Chargement de la plateforme Sonatel...</span></div>
  }

  if (!isSignedIn) {
    return (
      <div className="relative">
         {/* On affiche l'écran Login original en arrière-plan */}
         <div className="pointer-events-none opacity-50 blur-sm">
           <Login onLogin={() => {}} />
         </div>
         {/* Et le vrai bouton d'authentification au centre */}
         <div className="absolute inset-0 flex items-center justify-center">
            <div className="bg-[#030712]/90 border border-purple-500/30 p-8 rounded-2xl backdrop-blur-xl flex flex-col items-center">
               <ShieldCheck className="w-12 h-12 text-purple-400 mb-4" />
               <h2 className="text-2xl font-bold text-white mb-2">Accès Sécurisé</h2>
               <p className="text-slate-400 mb-6 text-center max-w-xs">Vous devez être authentifié(e) avec votre compte GitHub pour accéder à l'AgentOps Sonatel.</p>
               <SignInButton mode="modal">
                 <button className="flex items-center gap-2 bg-white text-black px-6 py-3 rounded-lg font-medium hover:bg-slate-200 transition-colors">
                    <GitBranch className="w-5 h-5" />
                    Continuer avec GitHub
                 </button>
               </SignInButton>
            </div>
         </div>
      </div>
    )
  }

  // Si l'utilisateur est connecté, on affiche l'application complète
  return (
    <>
      <SignedIn>
        <div style={{display: 'none'}}>Badge secret pour forcer l'import</div>
        <MainApp />
      </SignedIn>
    </>
  )
}
"""

with open("app/page.tsx", "a", encoding="utf-8") as f:
    f.write(nouvelle_page)

