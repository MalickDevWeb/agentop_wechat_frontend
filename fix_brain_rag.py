import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Le but est de remplacer le composant Brain. Je vais utiliser les astuces de comptage d'accolades 
# pour éviter toute erreur de regex.

start_idx = content.find("function Brain() {")
if start_idx != -1:
    open_braces = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            open_braces += 1
        elif content[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                end_idx = i + 1
                break

    new_brain = """function Brain() {
  const [skills, setSkills] = useState<any[]>([]);
  const [skillPromptOpen, setSkillPromptOpen] = useState(false);
  const [newSkillTitle, setNewSkillTitle] = useState('');
  const [newSkillDesc, setNewSkillDesc] = useState('');
  
  useEffect(() => {
    fetch(`${API_URL}/memory/skills`).then(r=>r.json()).then(data => {
      if(data && data.length) setSkills(data);
    }).catch(()=>{});
  }, []);

  const handleShareSkill = () => {
    if(!newSkillTitle || !newSkillDesc) return;
    fetch(`${API_URL}/memory/skills`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({title: newSkillTitle, description: newSkillDesc})
    }).then(r=>r.json()).then(data => {
      setSkills([data, ...skills]);
      setSkillPromptOpen(false);
      setNewSkillTitle('');
      setNewSkillDesc('');
    });
  };

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

  // --- NOUVEAU : Logique RAG (Search) ---
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResult, setSearchResult] = useState<string | null>(null);

  const handleSearch = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchQuery.trim() !== '') {
      setIsSearching(true);
      setSearchResult(null);
      try {
        const res = await fetch(`${API_URL}/memory/prepare`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ project_id: 'mp-afritrips', prompt: searchQuery })
        });
        const data = await res.json();
        setSearchResult(data.context || "Aucune réponse trouvée.");
      } catch (err) {
        setSearchResult("Erreur lors de la recherche vectorielle.");
      }
      setIsSearching(false);
    }
  };

  return (
    <div className="content brain">
      <Header eyebrow="DEVELOPER EXPERIENCE / KNOWLEDGE" title="Explorateur de Cerveau" desc="Interrogez la mémoire validée de votre codebase." action="Partager un Skill (Règle)" onAction={() => setSkillPromptOpen(true)} />
      
      <div className="brain-search">
        <Sparkles size={20} />
        <input 
          placeholder="Posez une question sur l’architecture du projet... (Appuyez sur Entrée)" 
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          onKeyDown={handleSearch}
          disabled={isSearching}
        />
        <kbd>⌘ K</kbd>
      </div>

      {isSearching && (
        <div style={{marginTop: 15, padding: 15, color: '#91a0b5', fontSize: 13, display: 'flex', alignItems: 'center', gap: 10, background: 'rgba(255,255,255,0.02)', borderRadius: 8}}>
          <Sparkles size={14} className="spin-animation" /> L'IA fouille dans l'architecture et le code local du projet mp-afritrips...
        </div>
      )}

      {searchResult && (
        <div style={{marginTop: 15, padding: 20, background: '#0b1324', border: '1px solid #1e293b', borderRadius: 8, position: 'relative'}}>
          <div style={{position:'absolute', top: -12, left: 20, background: '#10b981', color: 'black', fontSize: 10, fontWeight: 'bold', padding: '2px 8px', borderRadius: 4, letterSpacing: 1}}>RÉPONSE RAG EXTRAITE DU CODE</div>
          <p style={{fontSize: 14, color: '#e2e8f0', whiteSpace: 'pre-wrap', fontFamily: 'monospace', margin: 0, lineHeight: 1.6}}>
            {searchResult}
          </p>
          <button className="button ghost" style={{marginTop: 15, fontSize: 12}} onClick={() => setSearchResult(null)}>Fermer le résultat</button>
        </div>
      )}

      {window.localStorage.getItem('canIngest') === 'true' && (
        <div style={{marginTop:20, padding:20, background:'#101f33', border:'1px solid #263a55', borderRadius:8}}>
          <h3 style={{fontSize:14, marginBottom:10, color:'white', display:'flex', alignItems:'center', gap:8}}><GitBranch size={16}/> Nourrir le Cerveau (GitHub)</h3>
          <p style={{fontSize:13, color:'#91a0b5', marginBottom:14}}>Collez l'URL d'un dépôt Git pour analyser son code source et renforcer l'IA.</p>
          <div style={{display:'flex', gap:10}}>
            <input style={{flex:1, padding:'10px 14px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, color:'white'}} placeholder="https://github.com/votre-equipe/projet" value={githubUrl} onChange={e=>setGithubUrl(e.target.value)} />
            <button className="button primary" onClick={launchIngestion} disabled={ingesting || !githubUrl}>{ingesting ? 'Analyse...' : 'Ingérer le code'}</button>
          </div>
          {ingestMsg && <div style={{marginTop:10, color:'#4ade80', fontSize:13}}>{ingestMsg}</div>}
        </div>
      )}

      <div className="brain-layout">
        <div>
          <div className="result-label">SKILLS IA (RÈGLES TRUSTED) <span>{skills.length} compétences</span></div>
          {skills.map((s) => (
            <Panel className="doc-card" key={s.id}>
              <div className="doc-top"><Badge tone="green">TRUSTED SKILL</Badge><span className="muted">#{s.id}</span></div>
              <h2>{s.title}</h2>
              <p>{s.description}</p>
              <div className="doc-foot"><span>{s.category || 'Engineering / Standards'}</span><span><Users size={13} /> Validé par {s.author}</span></div>
            </Panel>
          ))}
        </div>
        
        {skillPromptOpen && (
          <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.85)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:999, backdropFilter:'blur(4px)'}}>
            <div style={{background:'#0c1627', padding:30, borderRadius:12, width:450, border:'1px solid #1e2d40', boxShadow:'0 25px 50px -12px rgba(0,0,0,0.5)'}}>
              <h2 style={{fontSize:18, marginBottom:8, color: '#fff'}}>Créer un nouveau Skill</h2>
              <p style={{fontSize:14, color:'#91a0b5', marginBottom:20}}>Définissez une règle d'architecture que l'IA devra toujours respecter.</p>
              <input value={newSkillTitle} onChange={e=>setNewSkillTitle(e.target.value)} placeholder="Titre (ex: Variables CSS globales)" style={{width:'100%', padding:'12px', marginBottom:12, background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, outline:'none'}} />
              <textarea value={newSkillDesc} onChange={e=>setNewSkillDesc(e.target.value)} placeholder="Description stricte..." rows={5} style={{width:'100%', padding:'12px', marginBottom:24, background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, outline:'none', resize:'vertical'}} />
              <div style={{display:'flex', gap:12, justifyContent:'flex-end'}}>
                <button className="button ghost" onClick={()=>setSkillPromptOpen(false)}>Annuler</button>
                <button className="button primary" onClick={handleShareSkill}>Enseigner à l'IA</button>
              </div>
            </div>
          </div>
        )}

        <Panel className="brain-side">
          <h2>Sources de vérité</h2>
          <p>Le cerveau AgentOps se nourrit uniquement de contenu validé.</p>
          <div className="source"><Code2 size={15} /><div><b>342</b><small>fichiers indexés</small></div></div>
          <div className="source"><ShieldCheck size={15} /><div><b>98%</b><small>couverture TRUSTED</small></div></div>
          <button className="button ghost full" type="button" onClick={() => { const ev = new CustomEvent("navigate",{detail:"integrations"}); window.dispatchEvent(ev); }}>Gérer les sources <ArrowRight size={14} /></button>
        </Panel>
      </div>
    </div>
  );
}"""

    new_content = content[:start_idx] + new_brain + content[end_idx:]
    with open("app/page.tsx", "w", encoding="utf-8") as f:
        f.write(new_content)

