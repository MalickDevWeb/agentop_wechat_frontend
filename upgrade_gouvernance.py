import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

new_gouvernance = """function Gouvernance() {
  const [allUsers, setAllUsers] = useState<any[]>([
    { id: 'usr_1', name: 'Papa Malick TEUW', email: 'malickteuw.devweb@gmail.com', role: 'ADMIN', perms: { submit: true, auto_learn: true, publish: true } },
    { id: 'usr_2', name: 'Marie Fall', email: 'marie.fall@orange-sonatel.com', role: 'DEV', perms: { submit: true, auto_learn: false, publish: false } },
    { id: 'usr_3', name: 'Amadou Diop', email: 'amadou.diop@orange-sonatel.com', role: 'DEV', perms: { submit: true, auto_learn: false, publish: true } },
    { id: 'usr_4', name: 'Ousmane Sow', email: 'ousmane.sow@orange-sonatel.com', role: 'DEV', perms: { submit: false, auto_learn: false, publish: false } }
  ]);

  const togglePerm = (clerkId: string, permKey: string) => {
    setAllUsers(prev => prev.map(u => {
      if (u.id === clerkId) {
        return { ...u, perms: { ...u.perms, [permKey]: !u.perms[permKey] } };
      }
      return u;
    }));
  };

  return (
    <div className="content">
      <Header eyebrow="SÉCURITÉ & GOUVERNANCE" title="Contrôle des Accès (RBAC)" desc="Gérez la matrice des droits d'interaction avec l'IA et de déploiement pour votre équipe." action="Exporter CSV" />
      <div style={{marginTop: 40}}>
        <div className="card" style={{padding:20}}>
          <table style={{width:'100%', textAlign:'left', borderCollapse:'collapse'}}>
            <thead>
              <tr style={{borderBottom:'1px solid rgba(255,255,255,0.1)'}}>
                <th style={{paddingBottom:14, color:'#91a0b5', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.05em'}}>Développeur Sonatel</th>
                <th style={{paddingBottom:14, color:'#91a0b5', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.05em'}}>Rôle</th>
                <th style={{paddingBottom:14, textAlign:'right', color:'#91a0b5', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.05em'}}>Matrice des Permissions (IA & DevOps)</th>
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
                    <div style={{display:'flex', justifyContent:'flex-end', gap: 8}}>
                      <button 
                        onClick={() => togglePerm(u.id, 'submit')} 
                        style={{padding:'6px 12px', fontSize:11, borderRadius: 6, transition: 'all 0.2s', background: u.perms.submit ? 'rgba(35, 134, 54, 0.2)' : 'transparent', border: u.perms.submit ? '1px solid #238636' : '1px solid rgba(255,255,255,0.1)', color: u.perms.submit ? '#3fb950' : '#8b949e', cursor: 'pointer'}}
                        title="Autoriser à proposer du code à l'IA"
                      >
                        {u.perms.submit ? '✓ Proposer à l\'IA' : '✕ Proposer à l\'IA'}
                      </button>
                      
                      <button 
                        onClick={() => togglePerm(u.id, 'auto_learn')} 
                        style={{padding:'6px 12px', fontSize:11, borderRadius: 6, transition: 'all 0.2s', background: u.perms.auto_learn ? 'rgba(139, 92, 246, 0.2)' : 'transparent', border: u.perms.auto_learn ? '1px solid #8b5cf6' : '1px solid rgba(255,255,255,0.1)', color: u.perms.auto_learn ? '#c4b5fd' : '#8b949e', cursor: 'pointer'}}
                        title="Autoriser l'apprentissage direct de l'IA sans validation du Lead Dev"
                      >
                        {u.perms.auto_learn ? '✓ Apprentissage Direct' : '✕ Apprentissage Direct'}
                      </button>

                      <button 
                        onClick={() => togglePerm(u.id, 'publish')} 
                        style={{padding:'6px 12px', fontSize:11, borderRadius: 6, transition: 'all 0.2s', background: u.perms.publish ? 'rgba(59, 130, 246, 0.2)' : 'transparent', border: u.perms.publish ? '1px solid #3b82f6' : '1px solid rgba(255,255,255,0.1)', color: u.perms.publish ? '#93c5fd' : '#8b949e', cursor: 'pointer'}}
                        title="Autoriser à merger en production"
                      >
                        {u.perms.publish ? '✓ Publication Prod' : '✕ Publication Prod'}
                      </button>
                    </div>
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

