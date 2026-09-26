import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Le composant n'a pas été inséré car "export default function App()" n'existait sûrement pas.
# Cherchons le bon "export default function" :
match = re.search(r'export default function \w+\(\) \{', content)
if match and "function Gouvernance()" not in content:
    main_func = match.group(0)
    gouvernance_code = """
function Gouvernance() {
  const [allUsers, setAllUsers] = React.useState<any[]>([]);

  React.useEffect(() => {
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
    content = content.replace(main_func, gouvernance_code + "\n" + main_func)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

