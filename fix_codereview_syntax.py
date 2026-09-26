import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

old_regex = re.compile(r'function CodeReview\(\) \{.*?(?=function \w+\(|export default)', re.DOTALL)

new_code = """function CodeReview() {
  const [status, setStatus] = useState('pending');
  const [commenting, setCommenting] = useState(false);

  const handleApprove = () => setStatus('approved');
  const handleReject = () => setStatus('rejected');
  const handleComment = () => {
    setCommenting(true);
    setTimeout(() => {
      setCommenting(false);
      alert("AgentOps a analysé le code et généré le commentaire GitHub suivant :\\n\\n'Excellente initiative de passer au JWT ! Cela sécurise l\\'API et évite l\\'accès direct en base. Le code respecte nos standards. PR prête à être mergée.'");
    }, 1500);
  };

  return (
    <div className="content">
      <Header eyebrow="GITHUB / CODE REVIEW" title="Code Review" desc="Analysez les changements critiques avant de les intégrer à votre production." action="Voir sur GitHub" />
      <div style={{marginTop: 40}}>
        <div className="card">
          <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', borderBottom:'1px solid rgba(255,255,255,0.1)', paddingBottom:20, marginBottom:20}}>
            <div>
              <Badge tone={status === 'approved' ? 'green' : status === 'rejected' ? 'red' : 'blue'}>
                {status === 'approved' ? '✓ PR Approuvée et Mergée' : status === 'rejected' ? '✕ PR Rejetée' : "En attente d'approbation"}
              </Badge>
              <h2 style={{marginTop:15, marginBottom:5, fontSize:18}}>PR #482 <span style={{fontWeight:'normal', color:'#91a0b5'}}>feat: rotate authentication middleware</span></h2>
              <div style={{fontSize:12, color:'#91a0b5'}}>Analyse terminée • Il y a 2 minutes</div>
            </div>
            <div style={{textAlign:'right'}}>
              <div style={{fontSize:24, fontWeight:'bold', color:'#10b981'}}>99%</div>
              <div style={{fontSize:12, color:'#91a0b5'}}>confiance</div>
            </div>
          </div>
          
          <div style={{background:'rgba(255,255,255,0.03)', padding:15, borderRadius:8, marginBottom:20}}>
            <b style={{fontSize:14, color:'#fff', display: 'flex', alignItems: 'center', gap: 8}}>✨ Analyse AgentOps Copilot</b>
            <p style={{fontSize:13, color:'#91a0b5', marginTop:5, marginBottom:0}}>Le changement renforce la vérification JWT et supprime un accès direct à la base de données. Le code est sûr et performant.</p>
          </div>

          <div style={{display:'flex', gap:20, marginBottom:30}}>
            <div style={{flex:1}}>
              <div style={{fontSize:12, color:'#91a0b5', marginBottom:10}}>Avant (src/auth/middleware.ts)</div>
              <pre style={{background:'#000', padding:15, borderRadius:8, fontSize:12, overflowX:'auto', margin:0}}>
                <code style={{color:'#ef4444'}}>{`18 export async function authorize(req) {
19   const token = req.headers.get('authorization')
20   return db.users.find(token)
21 }`}</code>
              </pre>
            </div>
            <div style={{flex:1}}>
              <div style={{fontSize:12, color:'#10b981', marginBottom:10}}>Après (Optimisé)</div>
              <pre style={{background:'#000', padding:15, borderRadius:8, fontSize:12, overflowX:'auto', margin:0}}>
                <code style={{color:'#10b981'}}>{`18 export async function authorize(req) {
19   const token = req.headers.get('authorization')
20   return await verifyJwt(token, {
21     issuer: 'agentops', audience: 'api'
22   })
23 }`}</code>
              </pre>
            </div>
          </div>

          {status === 'pending' && (
            <div style={{display:'flex', gap:15, justifyContent:'flex-end'}}>
              <button className="button ghost" onClick={handleReject}>Rejeter</button>
              <button className="button ghost" onClick={handleComment}>{commenting ? "Génération par l'IA..." : "Générer un commentaire GitHub"}</button>
              <button className="button primary" onClick={handleApprove}>Approuver la PR</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

"""

match = old_regex.search(content)
if match:
    # On remplace par concaténation pour éviter les soucis de parsing de re.sub sur les \\n
    new_content = content[:match.start()] + new_code + content[match.end():]
    with open("app/page.tsx", "w", encoding="utf-8") as f:
        f.write(new_content)
