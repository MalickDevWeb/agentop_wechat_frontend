import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ajouter les variables d'état pour l'ingestion dans la fonction Brain
old_brain_start = "function Brain() {"
new_brain_start = """function Brain() {
  const [chunks, setChunks] = useState<{id:string,content:string,status:string}[]>([]);
  const [query, setBrainQuery] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestMsg, setIngestMsg] = useState('');

  const launchIngestion = async () => {
    if(!githubUrl) return;
    setIngesting(true);
    setIngestMsg('');
    try {
      const res = await fetch(`${API_URL}/memory/ingest-github`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url: githubUrl })
      });
      const data = await res.json();
      setIngestMsg(data.message || 'Ingestion démarrée.');
      setGithubUrl('');
    } catch(e) {
      setIngestMsg('Erreur de connexion au serveur.');
    }
    setIngesting(false);
  };
"""
# Remplacement sécurisé pour Brain() 
if "const [chunks, setChunks]" in content and "const [githubUrl, setGithubUrl]" not in content:
    # On insère juste les variables si la fonction Brain a déjà des states
    content = content.replace(
        "const [query, setBrainQuery] = useState('');",
        """const [query, setBrainQuery] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestMsg, setIngestMsg] = useState('');
  
  const launchIngestion = async () => {
    if(!githubUrl) return;
    setIngesting(true); setIngestMsg('');
    try {
      const res = await fetch(`${API_URL}/memory/ingest-github`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ url: githubUrl }) });
      const data = await res.json();
      setIngestMsg(data.message || 'Ingestion démarrée.');
      setGithubUrl('');
    } catch(e) { setIngestMsg('Erreur.'); }
    setIngesting(false);
  };"""
    )
elif "const [githubUrl, setGithubUrl]" not in content:
    content = content.replace(old_brain_start, new_brain_start)

# 2. Ajouter l'UI d'ingestion sous le champ de recherche
ui_ingest = """<div style={{marginTop:20, padding:20, background:'#101f33', border:'1px solid #263a55', borderRadius:8}}>
      <h3 style={{fontSize:14, marginBottom:10, color:'white', display:'flex', alignItems:'center', gap:8}}><GitBranch size={16}/> Nourrir le Cerveau (GitHub)</h3>
      <p style={{fontSize:13, color:'#91a0b5', marginBottom:14}}>Collez l'URL d'un dépôt Git pour analyser son code source et renforcer l'IA.</p>
      <div style={{display:'flex', gap:10}}>
        <input style={{flex:1, padding:'10px 14px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, color:'white'}} placeholder="https://github.com/votre-equipe/projet" value={githubUrl} onChange={e=>setGithubUrl(e.target.value)} />
        <button className="button primary" onClick={launchIngestion} disabled={ingesting || !githubUrl}>{ingesting ? 'Analyse...' : 'Ingérer le code'}</button>
      </div>
      {ingestMsg && <div style={{marginTop:10, color:'#4ade80', fontSize:13}}>{ingestMsg}</div>}
    </div>"""

# On l'insère juste après le div brain-search
content = content.replace(
    '<kbd>⌘ K</kbd></div>',
    f'<kbd>⌘ K</kbd></div>\n    {ui_ingest}'
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
