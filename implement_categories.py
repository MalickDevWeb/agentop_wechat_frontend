import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ajouter le state des catégories dans ComponentHub
old_hub_start = "function ComponentHub({ isDeveloper, developerTrusted, onGrantDeveloperTrust }: { isDeveloper: boolean; developerTrusted: boolean; onGrantDeveloperTrust: () => void }) {"

new_hub_start = """function ComponentHub({ isDeveloper, developerTrusted, onGrantDeveloperTrust }: { isDeveloper: boolean; developerTrusted: boolean; onGrantDeveloperTrust: () => void }) {
  const [categories, setCategories] = useState<{id:number, name:string}[]>([]);
  const [activeFilter, setActiveFilter] = useState('Tous');
  const [categoryName, setCategoryName] = useState('');"""

content = content.replace(old_hub_start, new_hub_start)

# 2. Fetch categories on load
old_fetch = """useEffect(() => {
    fetch(`${API_URL}/components/`).then(r=>r.json()).then(data => {
      if(data && data.length) setComponents(data)
    }).catch(e => console.log("Backend offline, using mocks"));
  }, []);"""

new_fetch = """useEffect(() => {
    fetch(`${API_URL}/components/`).then(r=>r.json()).then(data => {
      if(data && data.length) setComponents(data)
    }).catch(()=>{});
    fetch(`${API_URL}/components/categories`).then(r=>r.json()).then(data => {
      if(data && data.length) setCategories(data)
    }).catch(()=>{});
  }, []);"""

content = content.replace(old_fetch, new_fetch)

# 3. Mettre à jour la constante "visible" pour utiliser le activeFilter
content = content.replace(
    'const visible = components.filter((item) => `${item.name} ${item.tags}`.toLowerCase().includes(query.toLowerCase()))',
    'const visible = components.filter((item) => `${item.name} ${item.tags}`.toLowerCase().includes(query.toLowerCase()) && (activeFilter === "Tous" || item.tags.includes(activeFilter)))'
)

# 4. Ajouter les boutons de filtres au-dessus de la grille
filter_ui = """</div>
    <div style={{display:'flex', gap:8, marginBottom:20, flexWrap:'wrap'}}>
      <button className={`badge ${activeFilter==='Tous'?'green':'blue'}`} onClick={()=>setActiveFilter('Tous')} style={{cursor:'pointer', border:activeFilter==='Tous'?'1px solid #4ade80':'1px solid transparent'}}>Tous</button>
      {categories.map(c => <button key={c.id} className={`badge ${activeFilter===c.name?'green':'blue'}`} onClick={()=>setActiveFilter(c.name)} style={{cursor:'pointer', border:activeFilter===c.name?'1px solid #4ade80':'1px solid transparent'}}>{c.name}</button>)}
    </div>
    {components.length === 0"""

content = content.replace("</div>\n    {components.length === 0", filter_ui)

# 5. Ajouter le bouton d'administration de catégorie
admin_button = """{!isDeveloper && !developerTrusted && <button className="button ghost" type="button" onClick={onGrantDeveloperTrust}>Autoriser la publication développeur</button>}"""
new_admin_button = """{!isDeveloper && !developerTrusted && <button className="button ghost" type="button" onClick={onGrantDeveloperTrust}>Autoriser la publication</button>}
      {!isDeveloper && <button className="button ghost" type="button" onClick={() => {
        const cat = window.prompt("Nom de la nouvelle catégorie :");
        if (cat) {
          fetch(`${API_URL}/components/categories`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({name: cat})})
          .then(r=>r.json()).then(d => { if(d.id) setCategories([...categories, d]) });
        }
      }}>+ Gérer les catégories</button>}"""

content = content.replace(admin_button, new_admin_button)

# 6. Modifier le formulaire de création de composant (Step 1)
# Remplacer la zone du titre/description pour inclure la catégorie
old_publish_form = """<label className="publish-field">Titre du composant<input value={componentName} onChange={(event) => setComponentName(event.target.value)} placeholder="Ex. Bouton de confirmation" /></label><label className="publish-field">Description<textarea value={componentDescription} onChange={(event) => setComponentDescription(event.target.value)} placeholder="À quoi sert ce composant ?" rows={3} /></label>"""

new_publish_form = """<label className="publish-field">Titre du composant<input value={componentName} onChange={(event) => setComponentName(event.target.value)} placeholder="Ex. Bouton de confirmation" /></label>
<label className="publish-field">Catégorie<select value={categoryName} onChange={(e) => setCategoryName(e.target.value)} style={{width:'100%', padding:'10px', background:'rgba(255,255,255,0.05)', color:'white', border:'1px solid rgba(255,255,255,0.1)', borderRadius:8, marginTop:6}}>
  <option value="" disabled>Sélectionner une catégorie</option>
  {categories.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
</select></label>
<label className="publish-field">Description<textarea value={componentDescription} onChange={(event) => setComponentDescription(event.target.value)} placeholder="À quoi sert ce composant ?" rows={3} /></label>"""

content = content.replace(old_publish_form, new_publish_form)

# 7. Inclure la catégorie lors de la publication API (Click Publier)
content = content.replace(
    'setPublished(true); setPublishOpen(false) }}>Publier le composant',
    """
    fetch(`${API_URL}/components/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: componentName, category: categoryName, preview: componentName })
    }).then(() => { setPublished(true); setPublishOpen(false); window.location.reload(); })
  }}>Publier le composant"""
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
