import re

# 1. Ajout du ClerkProvider dans layout.tsx
with open("app/layout.tsx", "r", encoding="utf-8") as f:
    layout = f.read()

if "ClerkProvider" not in layout:
    layout = "import { ClerkProvider } from '@clerk/nextjs';\n" + layout
    layout = layout.replace("<html", "<ClerkProvider>\n      <html")
    layout = layout.replace("</html>", "</html>\n    </ClerkProvider>")
    with open("app/layout.tsx", "w", encoding="utf-8") as f:
        f.write(layout)

# 2. Ajout de la protection dans page.tsx (sans casser les Hooks)
with open("app/page.tsx", "r", encoding="utf-8") as f:
    page = f.read()

if "import { SignedIn" not in page:
    # On ajoute l'import
    page = "import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';\n" + page
    
    # On isole le composant Page existant en le renommant MainApp
    page = page.replace("export default function Page() {", "function MainApp() {")
    
    # On ajoute un composant Header sécurisé avec le UserButton Clerk (à la place du placeholder)
    page = page.replace('className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/30 text-purple-400 font-medium"', 'className="w-8 h-8 rounded-full flex items-center justify-center"')
    page = page.replace('<div className="w-8 h-8 rounded-full flex items-center justify-center">\n              {profiles[0].initials}\n            </div>', '<UserButton afterSignOutUrl="/"/>')

    # On recrée un nouveau composant Page qui protège MainApp
    protection_wrapper = """
export default function Page() {
  return (
    <>
      <SignedOut>
        <div className="min-h-screen flex flex-col items-center justify-center bg-[#030712] text-white">
            <div className="p-8 border border-white/10 bg-white/5 rounded-2xl backdrop-blur-md text-center">
                <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">AgentOps Enterprise</h1>
                <p className="text-slate-400 mb-8">Authentification requise pour Sonatel</p>
                <SignInButton mode="modal">
                    <button className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium transition-all">
                        Se connecter (GitHub)
                    </button>
                </SignInButton>
            </div>
        </div>
      </SignedOut>
      <SignedIn>
        <MainApp />
      </SignedIn>
    </>
  )
}
"""
    page = page + protection_wrapper
    with open("app/page.tsx", "w", encoding="utf-8") as f:
        f.write(page)
