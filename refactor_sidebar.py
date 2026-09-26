import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remplacer le logo / brand par Orange Senegal
old_brand = """<div className="brand"><Bot size={24} /><div><b>AgentOps</b><small>Enterprise workspace</small></div></div>"""
new_brand = """<div className="brand"><div style={{background:'#ff7900', color:'black', padding:4, borderRadius:4, fontWeight:'bold', fontSize:14, width:24, height:24, display:'flex', alignItems:'center', justifyContent:'center'}}>O</div><div><b>Orange Sénégal</b><small>Enterprise workspace</small></div></div>"""
content = content.replace(old_brand, new_brand)

# 2. Créer le composant Gouvernance (en extrayant le code du Leaderboard)
# Je vais d'abord enlever la gestion d'équipe du Leaderboard
gouvernance_code = """
function Gouvernance() {
  const [allUsers, setAllUsers] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/auth/users`).then(r=>r.json()).then(data => { if(data && data.length) setAllUsers(data); }).catch(()=>{});
  }, []);
  
  const toggleIngest = async (clerkId: string) => {
    const res = await fetch(`${API_URL}/auth/users/${clerkId}/toggle-ingest`, {method: 'POST'});
    if(res.ok) {
      const updated = await res.json();
      setAllUsers(allUsers.map(u => u.id === clerkId ? {...u, can_ingest: updated.can_ingest} : u));
    }
  };

  return (
    <div className="content">
      <Header eyebrow="SÉCURITÉ & ACCÈS" title="Gouvernance Complète" desc="Gérez les développeurs, leurs droits d'ingestion et de publication." />
      <div style={{marginTop: 40}}>
        <div className="card" style={{padding:20}}>
          <table style={{width:'100%', textAlign:'left', borderCollapse:'collapse'}}>
            <thead>
              <tr style={{borderBottom:'1px solid rgba(255,255,255,0.1)'}}>
                <th style={{paddingBottom:10}}>Développeur</th>
                <th style={{paddingBottom:10}}>Rôle</th>
                <th style={{paddingBottom:10, textAlign:'right'}}>Droit d'ingestion Git</th>
              </tr>
            </thead>
            <tbody>
              {allUsers.map(u => (
                <tr key={u.id} style={{borderBottom:'1px solid rgba(255,255,255,0.05)'}}>
                  <td style={{padding:'12px 0'}}>{u.name} <span style={{color:'#888', fontSize:12, marginLeft:8}}>{u.email}</span></td>
                  <td style={{padding:'12px 0'}}><Badge tone={u.role==='ADMIN'?'purple':'blue'}>{u.role}</Badge></td>
                  <td style={{padding:'12px 0', textAlign:'right'}}>
                    <button className={`button ${u.can_ingest ? 'primary' : 'ghost'}`} onClick={() => toggleIngest(u.id)} style={{padding:'4px 10px', fontSize:12}}>
                      {u.can_ingest ? '✓ Autorisé' : '✕ Interdit'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"""
# Je l'insère avant "export default function App"
content = content.replace("export default function App() {", gouvernance_code + "\nexport default function App() {")

# 3. Retirer le tableau de gouvernance du Leaderboard
content = re.sub(r'\{isAdmin && <div style=\{\{marginTop: 40\}\}>.*?</table >\s*</div>\s*</div>\}', '', content, flags=re.DOTALL)

# 4. Refaire la navigation (Sidebar)
old_nav_regex = r'<nav>.*?</nav>'
new_nav = """<nav>
        <div style={{fontSize: 10, fontWeight: 'bold', color: '#91a0b5', letterSpacing: 1, padding: '20px 20px 10px 20px'}}>POUR L'ÉQUIPE</div>
        <button onClick={() => setScreen('heal')} className={screen === 'heal' ? 'active' : ''}><Activity size={18}/> GitHub Auto-Heal</button>
        <button onClick={() => setScreen('brain')} className={screen === 'brain' ? 'active' : ''}><Network size={18}/> Explorateur de Cerveau</button>
        <button onClick={() => setScreen('leaderboard')} className={screen === 'leaderboard' ? 'active' : ''}><Trophy size={18}/> Leaderboard</button>
        <button onClick={() => setScreen('components')} className={screen === 'components' ? 'active' : ''}><Layers size={18}/> UI Components</button>
        
        {isAdmin && (
          <>
            <div style={{fontSize: 10, fontWeight: 'bold', color: '#91a0b5', letterSpacing: 1, padding: '30px 20px 10px 20px', borderTop: '1px solid rgba(255,255,255,0.05)', marginTop: 10}}>POUR L'ADMIN</div>
            <button onClick={() => setScreen('twin')} className={screen === 'twin' ? 'active' : ''}><Bot size={18}/> Digital Twin</button>
            <button onClick={() => setScreen('integrations')} className={screen === 'integrations' ? 'active' : ''}><Command size={18}/> Intégrations & IDE</button>
            <button onClick={() => setScreen('gouvernance')} className={screen === 'gouvernance' ? 'active' : ''}><ShieldCheck size={18}/> Gouvernance complète</button>
          </>
        )}
      </nav>"""

content = re.sub(old_nav_regex, new_nav, content, flags=re.DOTALL)

# 5. Ajouter l'écran Gouvernance au switch
content = content.replace("integrations: () => <Integrations userId={user.id} />, components:", "integrations: () => <Integrations userId={user.id} />, gouvernance: Gouvernance, components:")


with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

