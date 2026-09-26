import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer la fausse génération de token par un appel API
old_token_gen = """const generateToken = () => {
    const t = 'sk_dev_' + Math.random().toString(36).slice(2,18) + Math.random().toString(36).slice(2,10);
    setToken(t); navigator.clipboard?.writeText(t); setTokenCopied(true); setTimeout(()=>setTokenCopied(false),2000);
  };"""

# On suppose qu'on peut récupérer l'ID Clerk depuis useUser() dans Integrations.
# Le composant Integrations ne reçoit actuellement pas "user". Modifions d'abord Integrations.
# 1. On donne l'ID utilisateur au composant
content = content.replace("function Integrations() {", "function Integrations({ userId }: { userId: string }) {")
content = content.replace("<Integrations />", "<Integrations userId={user?.id || ''} />")
# S'il y a d'autres références (ex: dans l'objet des composants)
content = content.replace("integrations: Integrations,", "integrations: () => <Integrations userId={user.id} />,")

new_token_gen = """const [generating, setGenerating] = useState(false);
  const generateToken = async () => {
    setGenerating(true);
    try {
      const r = await fetch(`${API_URL}/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerk_id: userId })
      });
      const data = await r.json();
      if (data.token) {
        setToken(data.token);
        navigator.clipboard?.writeText(data.token);
        setTokenCopied(true);
        setTimeout(()=>setTokenCopied(false), 2000);
      }
    } catch(e) { console.error('Erreur Token'); }
    setGenerating(false);
  };"""

content = content.replace(old_token_gen, new_token_gen)
content = content.replace("{tokenCopied ? \"✓ Token copié !\" : \"Générer mon Token CLI\"}", "{generating ? \"Génération en cours...\" : tokenCopied ? \"✓ Token généré et copié !\" : \"Générer mon Token CLI\"}")

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Bouton du token connecté à l'API !")
