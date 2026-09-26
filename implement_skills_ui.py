import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ajouter le state des Skills
old_brain_start = "function Brain() {\n  const [chunks, setChunks]"
new_brain_start = """function Brain() {
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

  const [chunks, setChunks]"""

content = content.replace(old_brain_start, new_brain_start)

# 2. Remplacer l'action "Partager une règle" du Header pour ouvrir notre popup
content = content.replace(
    'action="Partager une règle" onAction={() => { const ev = new CustomEvent("navigate",{detail:"integrations"}); window.dispatchEvent(ev); }}',
    'action="Partager un Skill (Règle)" onAction={() => setSkillPromptOpen(true)}'
)

# 3. Remplacer le contenu statique des Résultats TRUSTED par la liste des skills (depuis l'API)
old_trusted = """<div className="result-label">RÉSULTATS TRUSTED <span>24 documents</span></div>{[['Pourquoi utilise-t-on une queue durable pour les workflows ?','Architecture / Workflows','Il y a 2 jours'],['Comment gérer les tokens d’authentification côté serveur ?','Security / Authentication','Il y a 5 jours'],['Standards de revue de code pour les agents','Engineering / Standards','Il y a 1 semaine']].map((r,i)=><Panel className="doc-card" key={r[0]}><div className="doc-top"><Badge tone="green">TRUSTED</Badge><span className="muted">#{i+1}</span></div><h2>{r[0]}</h2><p>Cette règle validée décrit les décisions techniques et les garde-fous adoptés par l’équipe Platform...</p><div className="doc-foot"><span>{r[1]}</span><span><Users size={13} /> Validé par Marie Laurent · {r[2]}</span></div></Panel>)}"""

new_trusted = """<div className="result-label">SKILLS IA (RÈGLES TRUSTED) <span>{skills.length} compétences</span></div>
      {skills.map((s, i) => (
        <Panel className="doc-card" key={s.id}>
          <div className="doc-top"><Badge tone="green">TRUSTED SKILL</Badge><span className="muted">#{s.id}</span></div>
          <h2>{s.title}</h2>
          <p>{s.description}</p>
          <div className="doc-foot"><span>{s.category}</span><span><Users size={13} /> Validé par {s.author}</span></div>
        </Panel>
      ))}"""

content = content.replace(old_trusted, new_trusted)

# 4. Ajouter le Modal / Popover pour créer un Skill
modal_ui = """
      {skillPromptOpen && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.8)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:999}}>
          <div style={{background:'#0c1627', padding:30, borderRadius:12, width:400, border:'1px solid #1e2d40'}}>
            <h2 style={{fontSize:18, marginBottom:10}}>Créer un nouveau Skill</h2>
            <p style={{fontSize:13, color:'#888', marginBottom:20}}>Définissez une règle que l'IA devra toujours respecter.</p>
            <input value={newSkillTitle} onChange={e=>setNewSkillTitle(e.target.value)} placeholder="Titre de la règle (ex: Accessibilité)" style={{width:'100%', padding:10, marginBottom:10, background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6}} />
            <textarea value={newSkillDesc} onChange={e=>setNewSkillDesc(e.target.value)} placeholder="Description détaillée de la directive..." rows={4} style={{width:'100%', padding:10, marginBottom:20, background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6}} />
            <div style={{display:'flex', gap:10, justifyContent:'flex-end'}}>
              <button className="button ghost" onClick={()=>setSkillPromptOpen(false)}>Annuler</button>
              <button className="button primary" onClick={handleShareSkill}>Enseigner à l'IA</button>
            </div>
          </div>
        </div>
      )}
"""

content = content.replace(
    '<Panel className="brain-side">',
    f'{modal_ui}\n<Panel className="brain-side">'
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

