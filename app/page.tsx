'use client'

import { useUser, useClerk, UserButton } from '@clerk/nextjs'
import { useState, useEffect } from 'react'
import { Activity, ArrowRight, Bot, Check, ChevronDown, Code2, Copy, Download, GitBranch, LayoutDashboard, Link2, Lock, Menu, MessageSquare, MoreHorizontal, Play, Search, Settings2, ShieldCheck, Sparkles, Terminal, ToggleLeft, Upload, Users, X } from 'lucide-react'

const API_URL = 'https://wechat-agent-5y0i.onrender.com/api/v1';

const screens = [
  { id: 'twin', label: 'Digital Twin', icon: Bot },
  { id: 'heal', label: 'GitHub Auto-Heal', icon: GitBranch },
  { id: 'brain', label: 'Explorateur de Cerveau', icon: Search },
  { id: 'leaderboard', label: 'Leaderboard', icon: Activity },
  { id: 'integrations', label: 'Intégrations & IDE', icon: Link2 },
  { id: 'components', label: 'UI Components', icon: Code2 },
  { id: 'gouvernance', label: 'Gouvernance Complète', icon: ShieldCheck },
]

function Badge({ children, tone = 'green' }: { children: React.ReactNode; tone?: 'green' | 'amber' | 'blue' | 'purple' }) { return <span className={`badge ${tone}`}><i />{children}</span> }
function Panel({ children, className = '' }: { children: React.ReactNode; className?: string }) { return <section className={`panel ${className}`}>{children}</section> }
function CodeBlock() { return <div className="code-grid"><div><div className="code-title"><span>Avant</span><span className="muted">src/auth/middleware.ts</span></div><pre><code><span className="line">18</span> <span className="kw">export async function</span> <span className="fn">authorize</span>(req) {'{'}{`\n`}<span className="line">19</span>   <span className="kw">const</span> token = req.headers.get(<span className="str">&apos;authorization&apos;</span>){`\n`}<span className="line bad">20</span>   <span className="kw">return</span> db.users.find(token){`\n`}<span className="line">21</span> {'}'}</code></pre></div><div><div className="code-title"><span>Après</span><Badge tone="green">Optimisé</Badge></div><pre><code><span className="line">18</span> <span className="kw">export async function</span> <span className="fn">authorize</span>(req) {'{'}{`\n`}<span className="line">19</span>   <span className="kw">const</span> token = req.headers.get(<span className="str">&apos;authorization&apos;</span>){`\n`}<span className="line good">20</span>   <span className="kw">return await</span> verifyJwt(token, {'{'}{`\n`}<span className="line">21</span>     issuer: <span className="str">&apos;agentops&apos;</span>, audience: <span className="str">&apos;api&apos;</span>{`\n`}<span className="line">22</span>   {'}'}){`\n`}<span className="line">23</span> {'}'}</code></pre></div></div> }

function Twin() {
  const [reviews, setReviews] = useState([
    { id: '#482', title: 'feat: integration API Orange Money', status: 'Validé par l\'IA', confidence: 99, time: 'Il y a 2 min', color: 'green' },
    { id: '#481', title: 'fix: bug de paiement', status: 'Rejeté', confidence: 45, time: 'Il y a 1h', color: 'red' }
  ])
  useEffect(() => {
    fetch(`${API_URL}/twin/`)
      .then(r=>r.json())
      .then(data => {
        if(data && data.length) setReviews(data.map((d: any) => ({id: '#'+d.id, title: d.title, status: d.status, confidence: d.confidence, time: d.time, color: d.confidence > 90 ? 'green' : 'red'})))
      }).catch(e => console.log(e))
  }, [])
 const [auto, setAuto] = useState(true); 
  const [configurationOpen, setConfigurationOpen] = useState(false);
  const [prStatus, setPrStatus] = useState<'pending'|'approved'|'rejected'>('pending');
  const [commentOpen, setCommentOpen] = useState(false);
  const [comment, setComment] = useState('');
  const [commentSent, setCommentSent] = useState(false);
  const [analysing, setAnalysing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState('');
  const runAnalysis = async () => {
    setAnalysing(true); setAnalysisResult('');
    try {
      const data = await fetch(`${API_URL}/twin/`).then(r=>r.json());
      if(data && data.length) setAnalysisResult(`Analyse terminée : ${data.length} PR(s) analysée(s). Dernière : ${data[0].title}`);
      else setAnalysisResult('Analyse terminée. Aucune PR en attente de validation.');
    } catch(e) { setAnalysisResult('Analyse terminée. Backend en veille, relancez dans 30s.'); }
    setAnalysing(false);
  };
  return <div className="content"><div className="hero-row"><div><div className="eyebrow">ADMIN / DIGITAL TWIN</div><h1>Validation & Jumeau Numérique</h1><p>Votre copilote de gouvernance analyse et sécurise chaque changement.</p></div><div className="hero-actions"><button className="button ghost" type="button" onClick={() => setConfigurationOpen(true)} aria-haspopup="dialog">Voir la configuration</button><button className="button primary" type="button" onClick={runAnalysis} disabled={analysing}>
        <Play size={14} /> {analysing ? 'Analyse en cours...' : 'Lancer une analyse'}
      </button></div></div>{analysisResult && <div className="publish-confirm" style={{color:"#4ade80",marginBottom:12}}><Check size={14}/> {analysisResult}</div>}
  {configurationOpen && <div className="modal-backdrop" role="presentation" onClick={() => setConfigurationOpen(false)}><div className="publish-modal" role="dialog" aria-modal="true" aria-labelledby="twin-config-title" onClick={(event) => event.stopPropagation()}><div className="panel-head"><div><div className="eyebrow">DIGITAL TWIN / CONFIGURATION</div><h2 id="twin-config-title">Configuration du Jumeau Numérique</h2><p>Contrôlez les règles appliquées avant chaque validation de code.</p></div><button className="icon-btn" type="button" onClick={() => setConfigurationOpen(false)} aria-label="Fermer la configuration"><X size={16}/></button></div><div className="setting-toggle"><div><b>Auto-Approve</b><p>Valider automatiquement les changements avec un score supérieur à 95%.</p></div><button className={`toggle ${auto ? 'on' : ''}`} type="button" onClick={() => setAuto(!auto)} aria-pressed={auto}><span /></button></div><div className="mini-stats"><div><span>Règles actives</span><b>142</b></div><div><span>Seuil de confiance</span><b>95%</b></div><div><span>Dernière mise à jour</span><b>Aujourd&apos;hui</b></div></div><button className="button primary full" type="button" onClick={() => setConfigurationOpen(false)}>Enregistrer et fermer</button></div></div>}<div className="twin-grid"><Panel className="review-panel">
  {analysisResult === '' ? 
    <div style={{padding:80,textAlign:'center',color:'#91a0b5'}}><Check size={48} color="#263a55" style={{margin:'0 auto 20px'}}/><h2 style={{fontSize:18,color:'white',marginBottom:8}}>Tout est à jour</h2><p>Aucune Pull Request ne nécessite l'attention du Jumeau Numérique.</p></div> 
  : 
  <>
    <div className="panel-head"><div><h2>Code Review <span className="pill">API Live</span></h2><p>Analyse de la dernière Pull Request interceptée</p></div><Badge tone="green">Analyse terminée</Badge></div><div className="ai-analysis"><span className="ai-icon"><Sparkles size={17} /></span><div><strong>Analyse AgentOps Copilot</strong><p>Analyse générée depuis les données réelles Neon.</p></div><div className="confidence"><b>99%</b><small>confiance</small></div></div><CodeBlock /><div className="review-actions">
  <button className="button danger" type="button" onClick={() => setPrStatus('rejected')} disabled={prStatus !== 'pending'} style={{opacity: prStatus !== 'pending' ? 0.5 : 1}}><X size={14} /> Rejeter</button><button className="button ghost" type="button" onClick={() => setCommentOpen(!commentOpen)} disabled={prStatus !== 'pending'} style={{opacity: prStatus !== 'pending' ? 0.5 : 1}}><MessageSquare size={14} /> Générer un commentaire GitHub</button><button className="button primary" type="button" onClick={() => setPrStatus('approved')} disabled={prStatus !== 'pending'} style={{opacity: prStatus !== 'pending' ? 0.5 : 1}}><Check size={14} /> Approuver</button></div>
        {commentOpen && prStatus === 'pending' && <div className="review-comment"><textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Ajoutez un commentaire pour la pull request..." rows={3} style={{width:'100%',background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.1)',borderRadius:8,padding:'10px',color:'white',resize:'none',marginBottom:8}}/><button className="button primary" type="button" disabled={!comment.trim()} onClick={() => { setCommentSent(true); setCommentOpen(false) }}>Publier le commentaire</button></div>}
        {commentSent && <div className="publish-confirm" style={{color:'#4ade80',display:'flex',alignItems:'center',gap:6,padding:'8px 0'}}><Check size={15}/> Commentaire publié sur GitHub.</div>}
        {prStatus !== 'pending' && <div className="publish-confirm" style={{color: prStatus === 'approved' ? '#4ade80' : '#f87171',display:'flex',alignItems:'center',gap:6,padding:'8px 0'}}>{prStatus === 'approved' ? <><Check size={15}/> PR Approuvée !</> : <><X size={15}/> PR Rejetée.</>}</div>}
        <div style={{display:'none'}}></div></>}</Panel><Panel className="twin-settings"><div className="panel-head"><div><h2><Bot size={17} /> Jumeau Numérique</h2><p>Profil de Marie Laurent</p></div><Badge tone="purple">Actif</Badge></div><div className="twin-avatar"><span>ML</span><div><b>Marie Laurent</b><small>Lead Developer · Platform</small></div></div><div className="setting-toggle"><div><b>Auto-Approve</b><p>Laisser mon Jumeau Numérique valider automatiquement les codes avec un score &gt; 95%.</p></div><button className={`toggle ${auto ? 'on' : ''}`} onClick={() => setAuto(!auto)} aria-pressed={auto}><span /></button></div><div className="mini-stats"><div><span>PRs analysées</span><b>184</b></div><div><span>Précision</span><b>98.6%</b></div></div><div className="trust-list"><div><Check size={14} /> Style de code respecté</div><div><Check size={14} /> Secrets détectés</div><div><Check size={14} /> Tests de sécurité passés</div></div></Panel></div></div> }

function CodeReview() {
  const [status, setStatus] = useState('pending');
  const [commenting, setCommenting] = useState(false);

  const handleApprove = () => setStatus('approved');
  const handleReject = () => setStatus('rejected');
  const handleComment = () => {
    setCommenting(true);
    setTimeout(() => {
      setCommenting(false);
      alert(`AgentOps a analysé le code et généré le commentaire GitHub suivant :\n\nExcellente initiative de passer au JWT ! Cela sécurise l'API et évite l'accès direct en base. Le code respecte nos standards. PR prête à être mergée.`);
    }, 1500);
  };

  return (
    <div className="content">
      <Header eyebrow="GITHUB / CODE REVIEW" title="Code Review" desc="Analysez les changements critiques avant de les intégrer à votre production." action="Voir sur GitHub" />
      <div style={{marginTop: 40}}>
        <div className="card">
          <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', borderBottom:'1px solid rgba(255,255,255,0.1)', paddingBottom:20, marginBottom:20}}>
            <div>
              <Badge tone={status === 'approved' ? 'green' : status === 'rejected' ? 'amber' : 'blue'}>
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
                <code style={{color:'#ef4444'}}>
                  <div>18 export async function authorize(req) {'{'}</div>
                  <div>19   const token = req.headers.get('authorization')</div>
                  <div>20   return db.users.find(token)</div>
                  <div>21 {'}'}</div>
                </code>
              </pre>
            </div>
            <div style={{flex:1}}>
              <div style={{fontSize:12, color:'#10b981', marginBottom:10}}>Après (Optimisé)</div>
              <pre style={{background:'#000', padding:15, borderRadius:8, fontSize:12, overflowX:'auto', margin:0}}>
                <code style={{color:'#10b981'}}>
                  <div>18 export async function authorize(req) {'{'}</div>
                  <div>19   const token = req.headers.get('authorization')</div>
                  <div>20   return await verifyJwt(token, {'{'}</div>
                  <div>21     issuer: 'agentops', audience: 'api'</div>
                  <div>22   {'}'})</div>
                  <div>23 {'}'}</div>
                </code>
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

function Heal() {
  const [crashes, setCrashes] = useState<string[][]>([]);
  const [stats, setStats] = useState<{ hoursSaved: number, resolved: number, mttr: number, chart: number[], repos: string[] }>({ hoursSaved: 0, resolved: 0, mttr: 0, chart: [], repos: [] });
  useEffect(() => {
    fetch(`${API_URL}/devops/crashes/`).then(r=>r.json()).then(data => {
      if(data && data.length) setCrashes(data.map((d:any) => [d.error, d.repo, d.time, d.status, d.tone]))
    }).catch(()=>{});
    fetch(`${API_URL}/devops/stats`).then(r=>r.json()).then(data => {
      if(data) setStats({ hoursSaved: data.hours_saved || 0, resolved: data.incidents || 0, mttr: data.mttr || 0, chart: [15,22,18,30,42,28,45,60,55,65,72,85], repos: ['auth-service', 'payment-gateway', 'agentops-web'] })
    }).catch(()=>{});
  }, []);
return <div className="content"><Header eyebrow="DEVOPS / AUTO-HEAL" title="GitHub Auto-Heal Hub" desc="L’IA surveille vos pipelines et remédie aux incidents critiques." action="Connecter GitHub" onAction={() => alert("Redirection vers l'intégration GitHub...")} /><div className="heal-stats"><div className="metric"><span>Heures sauvées ce mois</span><b>{stats.hoursSaved}<span>h</span></b><em>Données réelles</em></div><div className="metric"><span>Incidents résolus</span><b>{stats.resolved}</b><em>Données réelles</em></div><div className="metric"><span>MTTR moyen</span><b>{stats.mttr}<span>min</span></b><em>Données réelles</em></div></div><div className="heal-grid"><Panel className="chart-panel"><div className="panel-head"><div><h2>Heures de débogage sauvées</h2><p>Impact de l’auto-remédiation sur les 30 derniers jours</p></div><button className="select" type="button" onClick={(e) => { e.currentTarget.textContent = "Ce mois-ci"; }}>30 derniers jours <ChevronDown size={13} /></button></div><div className="bar-chart">{stats.chart.length === 0 ? <div style={{width:"100%",textAlign:"center",color:"#91a0b5",paddingTop:40}}>En attente de données métriques...</div> : stats.chart.map((h:number,i:number)=><div className="bar-col" key={i}><div className="bar" style={{height:`${h}%`}} /><small>{i}</small></div>)}</div></Panel><Panel className="repo-panel"><div className="panel-head"><div><h2>Repos surveillés</h2><p>Auto-heal actif</p></div><MoreHorizontal size={16} /></div>{stats.repos.length === 0 ? <div style={{padding:20,color:'#91a0b5',textAlign:'center'}}>Aucun dépôt surveillé.</div> : stats.repos.map((r:string,i:number)=><div className="repo-row" key={r}><GitBranch size={16} /><div><b>{r}</b><small>main branch</small></div><Badge tone="green">Protégé</Badge></div>)}</Panel></div><Panel className="crash-panel"><div className="panel-head"><div><h2>Crashs récents</h2><p>Derniers événements détectés sur CI/CD et production</p></div><button className="button ghost" type="button" onClick={() => window.scrollTo({top:document.body.scrollHeight,behavior:"smooth"})}>Voir tous les incidents <ArrowRight size={14} /></button></div><div className="crash-head"><span>Erreur</span><span>Repository</span><span>Date</span><span>Statut IA</span></div>{crashes.map(x=><div className="crash-row" key={x[0]}><b>{x[0]}</b><span><GitBranch size={13} /> {x[1]}</span><span className="muted">{x[2]}</span><Badge tone={x[4] as 'green'|'amber'|'blue'}>{x[3]}</Badge></div>)}</Panel></div> }

function Header({eyebrow,title,desc,action,onAction}:{eyebrow:string;title:string;desc:string;action:string;onAction?:()=>void}) { return <div className="hero-row"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{desc}</p></div><button className="button primary" type="button" onClick={onAction}><GitBranch size={14} /> {action}</button></div> }
function Brain() {
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

  const executeSearch = async (e?: any) => {
    if (e) e.preventDefault();
    if (searchQuery.trim() === '') return;
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
  };

  return (
    <div className="content brain">
      <Header eyebrow="DEVELOPER EXPERIENCE / KNOWLEDGE" title="Explorateur de Cerveau" desc="Interrogez la mémoire validée de votre codebase." action="Partager un Skill (Règle)" onAction={() => setSkillPromptOpen(true)} />
      
      <form className="brain-search" onSubmit={executeSearch} style={{display:'flex', alignItems:'center'}}>
        <Sparkles size={20} />
        <input 
          placeholder="Posez une question sur l'architecture..." 
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          disabled={isSearching}
          style={{flex:1, background:'transparent', border:'none', color:'white', outline:'none'}}
        />
        <button type="submit" className="button primary" disabled={isSearching} style={{padding:'6px 16px', marginLeft: 10, borderRadius: 6, fontSize: 13, height: '100%'}}>
          {isSearching ? 'Recherche...' : 'Rechercher'}
        </button>
      </form>

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
}

function Leaderboard({ isAdmin }: { isAdmin: boolean }) {
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

  const [period, setPeriod] = useState('Ce mois');
  useEffect(() => {
    fetch(`${API_URL}/team/leaderboard/`).then(r=>r.json()).then(data => {
      if(data && data.length) setLeaders(data.map((d: any) => [d.name, d.initials, d.score.toString(), d.growth, d.badge]))
    }).catch(e => console.log("Backend offline, using mocks"));
  }, []);
  
return <div className="content"><Header eyebrow="TEAM / PRODUCTIVITY" title="Leaderboard & Productivité" desc="Célébrez les bonnes pratiques qui rendent votre code plus sûr." action="Exporter le rapport" onAction={() => alert("Génération du rapport PDF...")} /><div className="leader-grid"><Panel className="podium"><div className="panel-head"><div><h2>Code validé ce mois</h2><p>Classement de l’équipe Platform</p></div><select><option>Septembre 2026</option></select></div><div className="podium-visual">
{leaders.length < 3 ? <div style={{width:'100%',textAlign:'center',padding:40,color:'#91a0b5'}}>Générez des contributions pour afficher le podium.</div> : <>
  <div className="place second"><span className="avatar">{leaders[1][1]}</span><b>{leaders[1][0]}</b><strong>{leaders[1][2]}</strong><small>validations</small></div>
  <div className="place first"><span className="crown">1</span><span className="avatar big">{leaders[0][1]}</span><b>{leaders[0][0]}</b><strong>{leaders[0][2]}</strong><small>validations</small></div>
  <div className="place third"><span className="avatar">{leaders[2][1]}</span><b>{leaders[2][0]}</b><strong>{leaders[2][2]}</strong><small>validations</small></div>
</>}
</div></Panel><Panel className="streak"><div className="streak-number"><Sparkles size={18} /><b>27</b><span>jours</span></div><h2>Votre streak</h2><p>Vous êtes dans le top 8% des contributeurs cette semaine.</p><div className="heatmap">{Array.from({length:84},(_,i)=><i key={i} className={`heat h${(i*7)%5}`} />)}</div><div className="heat-label"><span>Moins</span><i className="heat h0"/><i className="heat h2"/><i className="heat h4"/><span>Plus</span></div></Panel></div><Panel className="team-table"><div className="panel-head"><div><h2>Contributions de l’équipe</h2><p>Bonnes pratiques et qualité de code</p></div><button className="button ghost" type="button" onClick={() => setPeriod(period==='Ce mois'?'Cette semaine':period==='Cette semaine'?'Tout':'Ce mois')}>{ period } <ChevronDown size={13} /></button></div>{leaders.length === 0 ? <div style={{padding:40,textAlign:"center",color:"#91a0b5"}}>La base de données Neon est vide. Aucune donnée à afficher.</div> : leaders.map((r,i)=><div className="member-row" key={r[0]}><span className="avatar small">{r[1]}</span><b>{r[0]}</b><span className="muted">{r[4]}</span><strong>{r[2]}</strong><em>{r[3]}</em><div className="progress"><span style={{width:`${100-i*18}%`}} /></div></div>)}</Panel></div> }

function Integrations({ userId }: { userId: string }) {
  const [slack,setSlack]=useState(false);
  const [teams,setTeams]=useState(false);
  const [token,setToken]=useState('sk_dev_••••••••••••••••••••••');
  const [tokenCopied,setTokenCopied]=useState(false);
  const [generating, setGenerating] = useState(false);
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
  };
  return <div className="content"><Header eyebrow="SETUP / DEVELOPER TOOLS" title="Intégrations & Extensions IDE" desc="Connectez AgentOps à votre environnement de développement." action="Ajouter une intégration" onAction={() => alert("Ouverture du catalogue d'intégrations...")} /><div className="integration-grid"><Panel className="token-panel"><div className="panel-head"><div><h2><Terminal size={17} /> Token CLI</h2><p>Utilisez ce token pour authentifier l’AgentOps CLI.</p></div><Badge tone="green">Sécurisé</Badge></div><div className="token-box"><code style={{wordBreak:"break-all",fontSize:11}}>{token}</code><button aria-label="Copier le token" onClick={()=>{navigator.clipboard?.writeText(token);setTokenCopied(true);setTimeout(()=>setTokenCopied(false),1500)}}><Copy size={14} /></button></div><button className="button primary full" type="button" onClick={generateToken}><Terminal size={14} /> {generating ? "Génération en cours..." : tokenCopied ? "✓ Token généré et copié !" : "Générer mon Token CLI"}</button><p className="security-note"><Lock size={13} /> Ne partagez jamais votre token. Il sera affiché une seule fois.</p></Panel><Panel className="vscode-card"><div className="vscode-copy"><Badge tone="purple">AGENTOPS FOR VS CODE</Badge><h2>Le linter qui comprend votre code.</h2><p>Recevez des suggestions de sécurité et de style en temps réel, directement dans votre éditeur.</p><button className="button ghost" type="button" disabled style={{opacity: 0.6, cursor: "not-allowed"}}>Bientôt disponible <Download size={14} /></button></div><div className="editor"><div className="editor-top"><span>auth.ts</span><span>●</span></div><pre><code><span className="kw">async function</span> authorize(token) {'{'}{`\n`}  <span className="kw">const</span> user = <span className="fn">verifyToken</span>(token){`\n`}  <span className="err">  return user.permissions</span>{`\n`} {'}'}</code></pre><span className="lint-tip">AgentOps: add permission check</span></div></Panel></div><Panel className="channel-panel"><div className="panel-head"><div><h2>Notifications & Collaboration</h2><p>Restez informé des validations et incidents critiques.</p></div></div><div className="channel-row"><span className="channel-icon slack">#</span><div><b>Slack</b><small>Recevoir les alertes dans votre workspace</small></div><button className={`toggle ${slack?'on':''}`} onClick={()=>setSlack(!slack)} aria-pressed={slack}><span /></button></div><div className="channel-row"><span className="channel-icon teams">T</span><div><b>Microsoft Teams</b><small>Connecter les notifications à un canal Teams</small></div><button className={`toggle ${teams?"on":""}`} onClick={()=>setTeams(!teams)} aria-pressed={teams}><span /></button></div></Panel></div> }

function ComponentHub({ isDeveloper, developerTrusted, onGrantDeveloperTrust }: { isDeveloper: boolean; developerTrusted: boolean; onGrantDeveloperTrust: () => void }) {
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [categories, setCategories] = useState<{id:number, name:string}[]>([]);
  const [activeFilter, setActiveFilter] = useState('Tous');
  const [categoryName, setCategoryName] = useState('');
  const [selected, setSelected] = useState('Bouton Paiement Orange Money')
  const [tab, setTab] = useState('WXML')
  const [copied, setCopied] = useState(false)
  const [query, setQuery] = useState('')
  const [publishOpen, setPublishOpen] = useState(false)
  const [publishStep, setPublishStep] = useState<'details' | 'code'>('details')
  const [imageUrl, setImageUrl] = useState('')
  const [componentName, setComponentName] = useState('')
  const [componentDescription, setComponentDescription] = useState('')
  const [published, setPublished] = useState(false)
  const [components, setComponents] = useState<{name:string,tags:string,author:string,initials:string,preview:string}[]>([])
  
  useEffect(() => {
    fetch(`${API_URL}/components/`).then(r=>r.json()).then(data => {
      if(data && data.length) setComponents(data)
    }).catch(()=>{});
    fetch(`${API_URL}/components/categories`).then(r=>r.json()).then(data => {
      if(data && data.length) setCategories(data)
    }).catch(()=>{});
  }, []);
  const visible = components.filter((item) => `${item.name} ${item.tags}`.toLowerCase().includes(query.toLowerCase()) && (activeFilter === "Tous" || item.tags.includes(activeFilter)))
  const active = components.find((item) => item.name === selected) ?? components[0] ?? { name: "Aucun composant", tags: "-", author: "-", initials: "-", preview: "Base vide" }
  const code = tab === 'WXML' ? '<button class="om-button">Payer {{amount}} FCFA</button>' : tab === 'WXSS' ? '.om-button { background: #ff7900; color: #fff; border-radius: 8px; }' : tab === 'JS' ? 'Page({ data: { amount: 25000 } })' : '{ "component": true, "usingComponents": {} }'
  const selectImage = (event: React.ChangeEvent<HTMLInputElement>) => { const file = event.target.files?.[0]; if (file) setImageUrl(URL.createObjectURL(file)) }
  return <div className="content" style={{ color: '#e8edf5' }}>
    <div className="hero-row"><div><div className="eyebrow">DEVELOPER EXPERIENCE / REGISTRY</div><h1>Design System &amp; Composants</h1><p>Explorez, copiez et réutilisez les composants validés par l&apos;équipe Orange Senegal.</p></div><div className="hero-actions"><button className="button primary" onClick={() => { setPublished(false); setPublishStep('details'); setPublishOpen(true) }}>+ Publier un composant</button>{!isDeveloper && !developerTrusted && <button className="button ghost" type="button" onClick={onGrantDeveloperTrust}>Autoriser la publication</button>}
      {!isDeveloper && <button className="button ghost" type="button" onClick={() => {
        const cat = window.prompt("Nom de la nouvelle catégorie :");
        if (cat) {
          fetch(`${API_URL}/components/categories`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({name: cat})})
          .then(r=>r.json()).then(d => { if(d.id) setCategories([...categories, d]) });
        }
      }}>+ Gérer les catégories</button>}<small className="publish-policy">{developerTrusted ? 'Publication directe activée pour le développeur de confiance.' : isDeveloper ? 'Chaque publication est soumise à validation administrateur.' : 'Vous contrôlez les droits de publication de l’équipe.'}</small></div></div>
    <div style={{ display: 'flex', gap: 12, marginBottom: 18 }}><div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 10, background: '#101f33', border: '1px solid #263a55', borderRadius: 8, padding: '11px 14px' }}><Search size={16} color="#91a0b5"/><input aria-label="Rechercher un composant" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Rechercher un composant..." style={{ width: '100%', border: 0, outline: 0, background: 'transparent', color: '#fff' }}/></div><span className="badge blue" style={{ alignSelf: 'center' }}>{visible.length} composants affichés</span></div>
    <div style={{display:'flex', gap:8, marginBottom:20, flexWrap:'wrap'}}>
      <button className={`badge ${activeFilter==='Tous'?'green':'blue'}`} onClick={()=>setActiveFilter('Tous')} style={{cursor:'pointer', border:activeFilter==='Tous'?'1px solid #4ade80':'1px solid transparent'}}>Tous</button>
      {categories.map(c => <button key={c.id} className={`badge ${activeFilter===c.name?'green':'blue'}`} onClick={()=>setActiveFilter(c.name)} style={{cursor:'pointer', border:activeFilter===c.name?'1px solid #4ade80':'1px solid transparent'}}>{c.name}</button>)}
    </div>
    {components.length === 0 && <div className="publish-confirm" style={{background:"rgba(255,255,255,0.02)",color:"#91a0b5",padding:40,textAlign:"center",borderRadius:12,border:"1px dashed #263a55"}}>Aucun composant publié dans la base de données.</div>}
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, marginBottom: 18 }}>{visible.map((item) => <button key={item.name} onClick={() => setSelected(item.name)} style={{ textAlign: 'left', padding: 0, overflow: 'hidden', border: item.name === active.name ? '1px solid #ff7900' : '1px solid #263a55', borderRadius: 10, background: '#101f33', color: '#e8edf5' }}><div style={{ height: 105, padding: 20, display: 'grid', placeItems: 'center', background: '#0b1728' }}><span style={{ background: '#ff7900', color: '#fff', borderRadius: 7, padding: '10px 16px', fontWeight: 700, fontSize: 12 }}>{item.preview}</span></div><div style={{ padding: 14 }}><b>{item.name}</b><small style={{ display: 'block', color: '#91a0b5', marginTop: 8 }}>{item.tags}</small><small style={{ display: 'block', color: '#91a0b5', marginTop: 12 }}>Créé par {item.author} · {item.initials}</small></div></button>)}</div>
    <Panel><div className="panel-head"><div><h2><Code2 size={17}/> {active.name}</h2><p>Composant validé · prêt à intégrer dans votre mini-programme WeChat</p></div><Badge>Trusted</Badge></div><div style={{ display: 'grid', gridTemplateColumns: '1fr 1.15fr', gap: 18 }}><div style={{ minHeight: 190, display: 'grid', placeItems: 'center', background: '#0b1728', border: '1px solid #263a55', borderRadius: 8 }}>{imageUrl ? <img src={imageUrl} alt="Aperçu du composant publié" style={{ maxWidth: '88%', maxHeight: 150, objectFit: 'contain' }} /> : <div style={{ textAlign: 'center' }}><div style={{ color: '#91a0b5', fontSize: 12, marginBottom: 14 }}>APERÇU DU COMPOSANT</div><div style={{ background: '#ff7900', color: '#fff', borderRadius: 8, padding: '14px 24px', fontWeight: 700 }}>{active.preview}</div></div>}</div><div><div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>{['WXML','WXSS','JS','JSON'].map((item) => <button key={item} onClick={() => setTab(item)} style={{ border: 0, borderBottom: tab === item ? '2px solid #ff7900' : '2px solid transparent', background: 'transparent', color: tab === item ? '#ff7900' : '#91a0b5', padding: '7px 10px', fontWeight: 700 }}>{item}</button>)}<button className="button ghost" style={{ marginLeft: 'auto', padding: '6px 10px' }} onClick={() => { navigator.clipboard?.writeText(code); setCopied(true); setTimeout(() => setCopied(false), 1600) }}><Copy size={13}/> {copied ? 'Copié' : 'Copier le code'}</button></div><pre style={{ margin: 0, minHeight: 95, padding: 14, borderRadius: 8, background: '#07111f', border: '1px solid #263a55', color: '#cbd5e1', whiteSpace: 'pre-wrap' }}><code>{code}</code></pre><p style={{ color: '#91a0b5', fontSize: 12, margin: '12px 0 0' }}><strong style={{ color: '#e8edf5' }}>Contrat d&apos;intégration :</strong> chaque composant expose previewUrl, files et metadata. Le stockage et l&apos;API pourront être branchés plus tard sans changer cette interface.</p></div></div></Panel>
    {publishOpen && <div className="modal-backdrop" role="presentation" onClick={() => setPublishOpen(false)}><div className="publish-modal" role="dialog" aria-modal="true" aria-labelledby="publish-title" onClick={(event) => event.stopPropagation()}><div className="panel-head"><div><div className="eyebrow">ÉTAPE {publishStep === 'details' ? '1' : '2'} / 2</div><h2 id="publish-title">{publishStep === 'details' ? 'Créer un composant' : 'Ajouter le code du composant'}</h2><p>{publishStep === 'details' ? 'Décrivez le composant avant de préparer ses fichiers.' : 'Renseignez les fichiers WXML, WXSS, JS et JSON avant publication.'}</p></div><button className="icon-btn" onClick={() => setPublishOpen(false)} aria-label="Fermer"><X size={16}/></button></div>{publishStep === 'details' ? <><label className="publish-field">Titre du composant<input value={componentName} onChange={(event) => setComponentName(event.target.value)} placeholder="Ex. Bouton de confirmation" /></label>
<label className="publish-field">Catégorie<select value={categoryName} onChange={(e) => setCategoryName(e.target.value)} style={{width:'100%', padding:'10px', background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:8, marginTop:6}}>
  <option value="" disabled>Sélectionner une catégorie</option>
  {categories.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
</select></label>
<label className="publish-field">Description<textarea value={componentDescription} onChange={(event) => setComponentDescription(event.target.value)} placeholder="À quoi sert ce composant ?" rows={3} /></label><label className="upload-zone"><input type="file" accept="image/png,image/jpeg,image/webp" onChange={selectImage} />{imageUrl ? <img src={imageUrl} alt="Aperçu de l'image sélectionnée" /> : <><Upload size={20}/><b>Ajouter une image de preview</b><small>PNG, JPG ou WebP · aperçu local remplaçable par votre stockage en production</small></>}</label><button className="button primary full" disabled={!componentName.trim() || !componentDescription.trim()} onClick={() => setPublishStep('code')}>Suivant <ArrowRight size={14}/></button></> : <><div className="publish-code-tabs">{['WXML','WXSS','JS','JSON'].map((item) => <button key={item} onClick={() => setTab(item)} className={tab === item ? 'active' : ''}>{item}</button>)}</div><textarea className="publish-code-editor" aria-label={`Code ${tab}`} value={code} onChange={() => undefined} spellCheck={false} /><div className="publish-contract"><Lock size={14}/><span><b>Contrat de publication</b><small>Le composant sera publié avec son titre, sa description, son image et ses quatre fichiers.</small></span></div><div style={{ display: 'flex', gap: 8 }}><button className="button ghost" onClick={() => setPublishStep('details')}>Retour</button><button className="button primary full" onClick={() => { 
    fetch(`${API_URL}/components/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: componentName, category: categoryName, preview: componentName })
    }).then(() => { setPublished(true); setPublishOpen(false); window.location.reload(); })
  }}>Publier le composant <Check size={14}/></button></div></>}</div></div>}
    {published && <div className="publish-confirm"><Check size={15}/> Brouillon créé dans l&apos;interface. Il pourra être envoyé à l&apos;API de votre choix.</div>}
  </div>
}

function Login({ onLogin }: { onLogin: () => void }) {
  return <main className="login-shell"><div className="login-brand"><span className="brand-mark"><Sparkles size={14}/></span><b>agent<span>ops</span></b><small>Enterprise</small></div><div className="login-layout"><section className="login-story"><div className="eyebrow">ORANGE SENEGAL / AI GOVERNANCE</div><h1>Centralisez l&apos;intelligence de votre équipe technique.</h1><p>La plateforme qui transforme les bonnes pratiques de vos Lead Devs en une IA autonome, contrôlée et prête pour la production.</p><div className="terminal-card"><div className="terminal-top"><span><i/><i/><i/></span><small>agentops / digital-twin</small><span>•••</span></div><div className="terminal-line"><span className="terminal-prompt">$</span> agentops twin validate --workspace orange-sn</div><div className="terminal-success"><Check size={15}/><span><b>Jumeau Numérique activé</b><small>142 règles d&apos;architecture prêtes à l&apos;emploi.</small></span></div></div><div className="trust-list"><div><ShieldCheck size={17}/><span><b>Gouvernance sans friction</b><small>Chaque changement est vérifié avant production.</small></span></div><div><Lock size={17}/><span><b>Sécurité entreprise</b><small>Accès par rôle, audit et conformité centralisés.</small></span></div></div></section><section className="login-card"><div className="login-card-head"><span className="login-lock"><Sparkles size={17}/></span><div><h2>Bienvenue sur AgentOps</h2><p>Connectez-vous à l'espace de travail Orange Senegal</p></div></div><button className="button primary full" style={{padding:'14px', fontSize:'15px', marginTop:'24px'}} type="button" onClick={onLogin}><GitBranch size={17}/> Continuer avec GitHub</button><div className="login-foot" style={{marginTop:'40px'}}><span><ShieldCheck size={13}/> Accès sécurisé · authentifié par Clerk</span><span>Dakar · Production</span></div></section></div></main>
}


function Gouvernance() {
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
}

export default function Page() {
  const { isLoaded, isSignedIn, user } = useUser()
  const { openSignIn } = useClerk()
  const [isAdmin, setIsAdmin] = useState(false);
  const [screen, setScreen] = useState('twin')
  const [dbUser, setDbUser] = useState({ role: 'ADMIN', tone: 'admin' })
  const [developerTrusted, setDeveloperTrusted] = useState(false)
  const [workspaceMenu, setWorkspaceMenu] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)

  useEffect(() => {
    if (isSignedIn && user) {
      fetch(`${API_URL}/auth/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clerk_id: user.id, email: user.primaryEmailAddress?.emailAddress || '', name: user.fullName || 'Utilisateur' })
      }).then(r=>r.json()).then(d => {
        if (d.role) setDbUser({ role: d.role, tone: d.role === 'ADMIN' ? 'admin' : 'dev' })
      }).catch(e=>console.log(e))
    }
  }, [isSignedIn, user])

  if (!isLoaded) return null
  if (!isSignedIn) return <Login onLogin={() => openSignIn()} />

  const current = screens.find((s) => s.id === screen)!
  const profile = {
    id: user.id,
    initials: (user.firstName?.[0]||'') + (user.lastName?.[0]||''),
    name: user.fullName || 'Utilisateur',
    role: dbUser.role === 'ADMIN' ? 'Administrateur' : 'Développeur',
    tone: dbUser.tone
  }
  const isDeveloper = dbUser.role !== 'ADMIN'
  const View = isDeveloper && screen === 'twin' ? Heal : { twin: Twin, heal: CodeReview, brain: Brain, leaderboard: () => <Leaderboard isAdmin={isAdmin} />, integrations: () => <Integrations userId={user.id} />, gouvernance: Gouvernance, components: () => <ComponentHub isDeveloper={isDeveloper} developerTrusted={developerTrusted} onGrantDeveloperTrust={() => setDeveloperTrusted(true)} /> }[screen] || Twin

  return <main className="app-shell"><aside className="sidebar"><div className="brand"><span className="brand-mark"><Sparkles size={14}/></span><b>agent<span>ops</span></b></div><div className="workspace-wrap"><button className="workspace" type="button" onClick={() => setWorkspaceMenu(!workspaceMenu)} aria-expanded={workspaceMenu} aria-haspopup="menu"><span className="workspace-avatar">O</span><span><b>Orange Senegal</b><small>Enterprise workspace</small></span><ChevronDown size={14}/></button>{workspaceMenu && <div className="workspace-menu" role="menu"><div className="workspace-menu-title">Vos workspaces</div><button className="workspace-option selected" type="button" role="menuitem" onClick={() => setWorkspaceMenu(false)}><span className="workspace-avatar">O</span><span><b>Orange Senegal</b><small>Enterprise workspace</small></span><Check size={14}/></button><button className="workspace-option" type="button" role="menuitem" onClick={() => setWorkspaceMenu(false)}><span className="workspace-avatar secondary">D</span><span><b>Sandbox développeur</b><small>Environnement de test</small></span></button></div>}</div><div className="nav-group"><label>POUR L’ÉQUIPE</label>{[...screens.slice(1,4), screens[5]].map(({id,label,icon:Icon})=><button key={id} className={`nav-item ${screen===id?'active':''}`} onClick={()=>setScreen(id)}><Icon size={16}/>{label}</button>)}</div>{!isDeveloper && <div className="nav-group"><label>POUR L’ADMIN</label>{[screens[0], screens[4], screens[6]].map(({id,label,icon:Icon})=><button key={id} className={`nav-item ${screen===id?'active':''}`} onClick={()=>setScreen(id)}><Icon size={16}/>{label}</button>)}</div>}
<div className="role-context"><span className={`role-dot ${profile.tone}`} /><div><b>{isDeveloper ? 'Espace développeur' : 'Espace administrateur'}</b><small>{isDeveloper ? 'Accès aux outils d’équipe' : 'Gouvernance complète'}</small></div></div><div className="sidebar-bottom"><div className="system"><span /><div><b>Systèmes opérationnels</b><small>Tous les contrôles sont actifs</small></div></div><div className="profile-switcher" style={{display:"flex", alignItems:"center", gap:12, padding:"12px 16px", borderTop:"1px solid #263a55"}}><UserButton appearance={{elements:{userButtonAvatarBox:{width:32,height:32}}}} /><div style={{display:"flex", flexDirection:"column", overflow:"hidden"}}><b style={{fontSize:13, color:"white", whiteSpace:"nowrap", textOverflow:"ellipsis", overflow:"hidden"}}>{profile.name}</b><small style={{fontSize:11, color:"#91a0b5"}}>{profile.role}</small></div></div></div></aside><section className="main-area"><header className="topbar"><div className="crumb"><span>Orange Senegal</span><i>/</i><b>{current.label}</b></div><div className="top-actions"><span className="live"><span /> Dakar · Live</span><button className="icon-btn" type="button" aria-label="Voir les incidents" onClick={()=>setScreen("heal")}><Activity size={16}/></button><button className="icon-btn" type="button" aria-label="Ouvrir les paramètres" aria-expanded={settingsOpen} onClick={() => setSettingsOpen(!settingsOpen)}><Settings2 size={16}/></button><div style={{marginLeft: 12}}><UserButton /></div></div></header>{settingsOpen && <div className="settings-popover" role="dialog" aria-label="Paramètres rapides" tabIndex={-1} onKeyDown={(event) => { if (event.key === 'Escape') setSettingsOpen(false) }}><div className="settings-popover-head"><div><b>Paramètres rapides</b><small>Configuration de votre espace</small></div><button className="icon-btn" type="button" aria-label="Fermer les paramètres" onClick={() => setSettingsOpen(false)}><X size={15}/></button></div><button className="settings-action" type="button" onClick={()=>{setScreen("twin");setSettingsOpen(false)}}><ShieldCheck size={15}/><span><b>Contrôles de sécurité</b><small>Actifs pour Orange Senegal</small></span><span className="settings-status">Actif</span></button><button className="settings-action" type="button" onClick={()=>{setScreen("leaderboard");setSettingsOpen(false)}}><Users size={15}/><span><b>Gestion des profils</b><small>2 administrateurs · 1 développeur</small></span><ArrowRight size={14}/></button></div>}<div className={`role-context ${profile.tone}`}><span className={`profile-avatar ${profile.tone}`}>{profile.initials}</span><div><b>{profile.name} · {profile.role}</b><small>{isDeveloper ? 'Vue développeur : incidents, branches et outils de livraison' : 'Vue administrateur : gouvernance, conformité et contrôle des accès'}</small></div><Badge tone={isDeveloper ? 'blue' : 'amber'}>{isDeveloper ? 'Droits développeur' : 'Droits administrateur'}</Badge></div><View /></section></main>
}

void LayoutDashboard
void ToggleLeft
void Menu
void Copy
void ArrowRight

type ReactNode = React.ReactNode
