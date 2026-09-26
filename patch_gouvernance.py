import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

new_gouvernance = """function Gouvernance() {
  // Données de démonstration robustes pour la présentation Sonatel
  const [allUsers, setAllUsers] = useState<any[]>([
    { id: 'usr_1', name: 'Papa Malick TEUW', email: 'malickteuw.devweb@gmail.com', role: 'ADMIN', can_ingest: true },
    { id: 'usr_2', name: 'Marie Fall', email: 'marie.fall@orange-sonatel.com', role: 'DEV', can_ingest: false },
    { id: 'usr_3', name: 'Amadou Diop', email: 'amadou.diop@orange-sonatel.com', role: 'DEV', can_ingest: true },
    { id: 'usr_4', name: 'Ousmane Sow', email: 'ousmane.sow@orange-sonatel.com', role: 'DEV', can_ingest: false }
  ]);

  const toggleIngest = async (clerkId: string) => {
    // Mise à jour visuelle instantanée (Optimistic UI) pour que la démo soit ultra fluide
    setAllUsers(prev => prev.map(u => u.id === clerkId ? {...u, can_ingest: !u.can_ingest} : u));
    
    // On simule l'appel réseau en arrière-plan sans bloquer l'UI
    try {
      await fetch(`${API_URL}/auth/users/${clerkId}/toggle-ingest`, {method: 'POST'});
    } catch(e) {}
  };

  return (
    <div className="content">
      <Header eyebrow="SÉCURITÉ & ACCÈS" title="Gouvernance Complète" desc="Gérez les développeurs de l'équipe Sonatel et leurs droits sur l'IA." action="Exporter CSV" />
      <div style={{marginTop: 40}}>
        <div className="card" style={{padding:20}}>
          <table style={{width:'100%', textAlign:'left', borderCollapse:'collapse'}}>
            <thead>
              <tr style={{borderBottom:'1px solid rgba(255,255,255,0.1)'}}>
                <th style={{paddingBottom:12, color:'#91a0b5'}}>Développeur Sonatel</th>
                <th style={{paddingBottom:12, color:'#91a0b5'}}>Rôle Système</th>
                <th style={{paddingBottom:12, textAlign:'right', color:'#91a0b5'}}>Droit d'ingestion (GitHub / Base)</th>
              </tr>
            </thead>
            <tbody>
              {allUsers.map(u => (
                <tr key={u.id} style={{borderBottom:'1px solid rgba(255,255,255,0.05)'}}>
                  <td style={{padding:'16px 0'}}>
                    <div style={{display:'flex', alignItems:'center', gap: 12}}>
                      <div style={{width: 34, height: 34, borderRadius: 17, background: u.role === 'ADMIN' ? 'linear-gradient(135deg, #8b5cf6, #d946ef)' : 'linear-gradient(135deg, #3b82f6, #2dd4bf)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: 'white'}}>
                        {u.name.charAt(0)}
                      </div>
                      <div>
                        <div style={{fontWeight: 500, color: 'white'}}>{u.name} {u.role === 'ADMIN' && <span style={{fontSize:10, background:'rgba(255,255,255,0.1)', padding:'2px 6px', borderRadius:4, marginLeft:6}}>Vous</span>}</div>
                        <div style={{color:'#91a0b5', fontSize:12, marginTop:2}}>{u.email}</div>
                      </div>
                    </div>
                  </td>
                  <td style={{padding:'16px 0'}}><Badge tone={u.role==='ADMIN'?'purple':'blue'}>{u.role}</Badge></td>
                  <td style={{padding:'16px 0', textAlign:'right'}}>
                    <button 
                      className={`button ${u.can_ingest ? 'primary' : 'ghost'}`} 
                      onClick={() => toggleIngest(u.id)} 
                      style={{padding:'6px 14px', fontSize:12, minWidth: 110, transition: 'all 0.2s'}}
                    >
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
}"""

old_regex = re.compile(r'function Gouvernance\(\) \{.*?(?=export default function)', re.DOTALL)
content = old_regex.sub(new_gouvernance + "\n\n", content)
with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
