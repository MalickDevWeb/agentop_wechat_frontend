with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Ajouter l'état des boutons dans la fonction Twin
old_twin_state = "const [auto, setAuto] = useState(true); const [configurationOpen, setConfigurationOpen] = useState(false);"
new_twin_state = """const [auto, setAuto] = useState(true); 
  const [configurationOpen, setConfigurationOpen] = useState(false);
  const [prStatus, setPrStatus] = useState<'pending'|'approved'|'rejected'>('pending');
  const [commentOpen, setCommentOpen] = useState(false);
  const [comment, setComment] = useState('');
  const [commentSent, setCommentSent] = useState(false);"""
content = content.replace(old_twin_state, new_twin_state)

# Brancher le bouton Rejeter dans Twin
old_reject = '<button className="button danger"><X size={14} /> Rejeter</button>'
new_reject = '<button className="button danger" type="button" onClick={() => setPrStatus(\'rejected\')} disabled={prStatus !== \'pending\'} style={{opacity: prStatus !== \'pending\' ? 0.5 : 1}}><X size={14} /> Rejeter</button>'
content = content.replace(old_reject, new_reject)

# Brancher le bouton Commentaire GitHub dans Twin
old_comment = '<button className="button ghost"><MessageSquare size={14} /> Générer un commentaire GitHub</button>'
new_comment = '<button className="button ghost" type="button" onClick={() => setCommentOpen(!commentOpen)} disabled={prStatus !== \'pending\'} style={{opacity: prStatus !== \'pending\' ? 0.5 : 1}}><MessageSquare size={14} /> Générer un commentaire GitHub</button>'
content = content.replace(old_comment, new_comment)

# Brancher le bouton Approuver dans Twin
old_approve = '<button className="button primary"><Check size={14} /> Approuver</button>'
new_approve = '''<button className="button primary" type="button" onClick={() => setPrStatus('approved')} disabled={prStatus !== 'pending'} style={{opacity: prStatus !== 'pending' ? 0.5 : 1}}><Check size={14} /> Approuver</button></div>
        {commentOpen && prStatus === 'pending' && <div className="review-comment"><textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Ajoutez un commentaire pour la pull request..." rows={3} style={{width:'100%',background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.1)',borderRadius:8,padding:'10px',color:'white',resize:'none',marginBottom:8}}/><button className="button primary" type="button" disabled={!comment.trim()} onClick={() => { setCommentSent(true); setCommentOpen(false) }}>Publier le commentaire</button></div>}
        {commentSent && <div className="publish-confirm" style={{color:'#4ade80',display:'flex',alignItems:'center',gap:6,padding:'8px 0'}}><Check size={15}/> Commentaire publié sur GitHub.</div>}
        {prStatus !== 'pending' && <div className="publish-confirm" style={{color: prStatus === 'approved' ? '#4ade80' : '#f87171',display:'flex',alignItems:'center',gap:6,padding:'8px 0'}}>{prStatus === 'approved' ? <><Check size={15}/> PR Approuvée !</> : <><X size={15}/> PR Rejetée.</>}</div>}
        <div style={{display:'none'}}>'''
content = content.replace(old_approve, new_approve)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Boutons branchés avec succès !")
