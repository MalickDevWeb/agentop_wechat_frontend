import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ajouter UserButton à l'import Clerk
content = content.replace("import { useUser, useClerk } from '@clerk/nextjs'", "import { useUser, useClerk, UserButton } from '@clerk/nextjs'")

# 2. Supprimer les profils mockés et l'ancien composant Login
start_idx = content.find("type Profile = {")
end_idx = content.find("export default function Page() {")

new_login = """function Login({ onLogin }: { onLogin: () => void }) {
  return <main className="login-shell"><div className="login-brand"><span className="brand-mark"><Sparkles size={14}/></span><b>agent<span>ops</span></b><small>Enterprise</small></div><div className="login-layout"><section className="login-story"><div className="eyebrow">ORANGE SENEGAL / AI GOVERNANCE</div><h1>Centralisez l&apos;intelligence de votre équipe technique.</h1><p>La plateforme qui transforme les bonnes pratiques de vos Lead Devs en une IA autonome, contrôlée et prête pour la production.</p><div className="terminal-card"><div className="terminal-top"><span><i/><i/><i/></span><small>agentops / digital-twin</small><span>•••</span></div><div className="terminal-line"><span className="terminal-prompt">$</span> agentops twin validate --workspace orange-sn</div><div className="terminal-success"><Check size={15}/><span><b>Jumeau Numérique activé</b><small>142 règles d&apos;architecture prêtes à l&apos;emploi.</small></span></div></div><div className="trust-list"><div><ShieldCheck size={17}/><span><b>Gouvernance sans friction</b><small>Chaque changement est vérifié avant production.</small></span></div><div><Lock size={17}/><span><b>Sécurité entreprise</b><small>Accès par rôle, audit et conformité centralisés.</small></span></div></div></section><section className="login-card"><div className="login-card-head"><span className="login-lock"><Sparkles size={17}/></span><div><h2>Bienvenue sur AgentOps</h2><p>Connectez-vous à l'espace de travail Orange Senegal</p></div></div><button className="button primary full" style={{padding:'14px', fontSize:'15px', marginTop:'24px'}} type="button" onClick={onLogin}><GitBranch size={17}/> Continuer avec GitHub</button><div className="login-foot" style={{marginTop:'40px'}}><span><ShieldCheck size={13}/> Accès sécurisé · authentifié par Clerk</span><span>Dakar · Production</span></div></section></div></main>
}

"""
content = content[:start_idx] + new_login + content[end_idx:]

# 3. Remplacer l'état du composant Page pour utiliser le vrai utilisateur
start_page = content.find("export default function Page() {")
end_page = content.find("const isDeveloper = profile.tone === 'dev'")
end_page = content.find("\n", end_page)

new_page_state = """export default function Page() {
  const { isLoaded, isSignedIn, user } = useUser()
  const { openSignIn } = useClerk()
  const [screen, setScreen] = useState('twin')
  const [dbUser, setDbUser] = useState({ role: 'ADMIN', tone: 'admin' })
  const [developerTrusted, setDeveloperTrusted] = useState(false)
  const [workspaceMenu, setWorkspaceMenu] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)

  useEffect(() => {
    if (isSignedIn && user) {
      fetch(`${API_URL}/auth/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress || '', name: user.fullName || 'Utilisateur' })
      }).then(r=>r.json()).then(d => {
        if (d.role) setDbUser({ role: d.role, tone: d.role === 'ADMIN' ? 'admin' : 'dev' })
      }).catch(e=>console.log(e))
    }
  }, [isSignedIn, user])

  if (!isLoaded) return null
  if (!isSignedIn) return <Login onLogin={() => openSignIn()} />

  const current = screens.find((s) => s.id === screen)!
  const profile = {
    id: user.id,
    initials: (user.firstName?.[0]||'') + (user.lastName?.[0]||''),
    name: user.fullName || 'Utilisateur',
    role: dbUser.role === 'ADMIN' ? 'Administrateur' : 'Développeur',
    tone: dbUser.tone
  }
  const isDeveloper = dbUser.role !== 'ADMIN'"""

content = content[:start_page] + new_page_state + content[end_page:]

# 4. Nettoyer la barre latérale pour insérer UserButton
# On utilise regex pour remplacer tout l'intérieur de div.profile-switcher
import re
content = re.sub(
    r'<div className="profile-switcher">.*?<MoreHorizontal size=\{15\}/></button></div>',
    r'<div className="profile-switcher" style={{display:"flex", alignItems:"center", gap:12, padding:"12px 16px", borderTop:"1px solid #263a55"}}><UserButton appearance={{elements:{userButtonAvatarBox:{width:32,height:32}}}} /><div style={{display:"flex", flexDirection:"column", overflow:"hidden"}}><b style={{fontSize:13, color:"white", whiteSpace:"nowrap", textOverflow:"ellipsis", overflow:"hidden"}}>{profile.name}</b><small style={{fontSize:11, color:"#91a0b5"}}>{profile.role}</small></div></div>',
    content,
    flags=re.DOTALL
)

# 5. Nettoyer la barre du haut pour insérer UserButton
content = content.replace(
    '<span className={`top-avatar ${profile.tone}`}>{profile.initials}</span>',
    '<div style={{marginLeft: 12}}><UserButton /></div>'
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Faux utilisateurs retirés et remplacés par Clerk !")
