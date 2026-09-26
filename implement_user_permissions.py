import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update session state to capture 'canIngest'
# Look for UserButton useEffect where /auth/sync is called
old_sync = """fetch(`${API_URL}/auth/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress || '', name: user.fullName || '' })
      }).then(r=>r.json()).then(data => setIsAdmin(data.role === 'ADMIN'));"""

new_sync = """fetch(`${API_URL}/auth/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress || '', name: user.fullName || '' })
      }).then(r=>r.json()).then(data => {
        setIsAdmin(data.role === 'ADMIN');
        window.localStorage.setItem('canIngest', data.can_ingest ? 'true' : 'false');
      });"""
content = content.replace(old_sync, new_sync)

# 2. Modify Brain component to conditionally hide Ingestion UI
# Ingestion UI is between `<h3 style={{fontSize:14, marginBottom:10` and `{ingestMsg &&`
old_ingest_ui = """<div style={{marginTop:20, padding:20, background:'#101f33', border:'1px solid #263a55', borderRadius:8}}>
      <h3 style={{fontSize:14, marginBottom:10, color:'white', display:'flex', alignItems:'center', gap:8}}><GitBranch size={16}/> Nourrir le Cerveau (GitHub)</h3>
      <p style={{fontSize:13, color:'#91a0b5', marginBottom:14}}>Collez l'URL d'un dépôt Git pour analyser son code source et renforcer l'IA.</p>
      <div style={{display:'flex', gap:10}}>
        <input style={{flex:1, padding:'10px 14px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, color:'white'}} placeholder="https://github.com/votre-equipe/projet" value={githubUrl} onChange={e=>setGithubUrl(e.target.value)} />
        <button className="button primary" onClick={launchIngestion} disabled={ingesting || !githubUrl}>{ingesting ? 'Analyse...' : 'Ingérer le code'}</button>
      </div>
      {ingestMsg && <div style={{marginTop:10, color:'#4ade80', fontSize:13}}>{ingestMsg}</div>}
    </div>"""

new_ingest_ui = """{window.localStorage.getItem('canIngest') === 'true' && <div style={{marginTop:20, padding:20, background:'#101f33', border:'1px solid #263a55', borderRadius:8}}>
      <h3 style={{fontSize:14, marginBottom:10, color:'white', display:'flex', alignItems:'center', gap:8}}><GitBranch size={16}/> Nourrir le Cerveau (GitHub)</h3>
      <p style={{fontSize:13, color:'#91a0b5', marginBottom:14}}>Collez l'URL d'un dépôt Git pour analyser son code source et renforcer l'IA.</p>
      <div style={{display:'flex', gap:10}}>
        <input style={{flex:1, padding:'10px 14px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:6, color:'white'}} placeholder="https://github.com/votre-equipe/projet" value={githubUrl} onChange={e=>setGithubUrl(e.target.value)} />
        <button className="button primary" onClick={launchIngestion} disabled={ingesting || !githubUrl}>{ingesting ? 'Analyse...' : 'Ingérer le code'}</button>
      </div>
      {ingestMsg && <div style={{marginTop:10, color:'#4ade80', fontSize:13}}>{ingestMsg}</div>}
    </div>}"""
content = content.replace(old_ingest_ui, new_ingest_ui)


# 3. Modify Leaderboard to include "Team Management" for Admins
# Search for function Leaderboard()
old_leaderboard_start = "function Leaderboard() {"
new_leaderboard_start = """function Leaderboard({ isAdmin }: { isAdmin: boolean }) {
  const [leaders, setLeaders] = useState<string[][]>([]);
  const [allUsers, setAllUsers] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/auth/seed-demo`).catch(()=>{}); // fallback si vide
    fetch(`${API_URL}/auth/users`).then(r=>r.json()).then(data => { if(data && data.length) setAllUsers(data); }).catch(()=>{});
  }, []);
  
  const toggleIngest = async (clerkId: string) => {
    const res = await fetch(`${API_URL}/auth/users/${clerkId}/toggle-ingest`, {method: 'POST'});
    if(res.ok) {
      const updated = await res.json();
      setAllUsers(allUsers.map(u => u.id === clerkId ? {...u, can_ingest: updated.can_ingest} : u));
    }
  };
"""

content = content.replace("function Leaderboard() {\n  const [leaders, setLeaders] = useState<string[][]>([]);", new_leaderboard_start)

# In the render, we pass isAdmin to Leaderboard
content = content.replace(
    "leaderboard: Leaderboard,",
    "leaderboard: () => <Leaderboard isAdmin={isAdmin} />,"
)

# Add the Team Management UI at the bottom of the Leaderboard
team_management_ui = """
      {isAdmin && <div style={{marginTop: 40}}>
        <h2 style={{fontSize:18, marginBottom:20, display:'flex', alignItems:'center', gap:10}}><Users size={20}/> Gestion de l'équipe et Permissions</h2>
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
      </div>}
"""

content = content.replace(
    "</div>\n    </div>\n  );",
    f"</div>{team_management_ui}\n    </div>\n  );"
)


with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
