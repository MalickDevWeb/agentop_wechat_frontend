import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Etape A : Ajouter les states pour la modal dans ComponentHub
state_injection = """
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
"""
content = re.sub(r'(function ComponentHub.*?\{)', r'\1\n' + state_injection, content, count=1, flags=re.DOTALL)

# Etape B : Remplacer la fonction handleCreateCategory
old_handle = r'const handleCreateCategory = async \(\) => \{.*?\};'
new_handle = """
  const handleCreateCategory = () => {
    setNewCategoryName("");
    setIsCategoryModalOpen(true);
  };

  const submitCategory = async () => {
    if(!newCategoryName.trim()) return;
    const res = await fetch(`${API_URL}/components/categories`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name: newCategoryName.trim()})
    });
    if(res.ok) {
      const cat = await res.json();
      setCategories([...categories, cat]);
      setIsCategoryModalOpen(false);
    }
  };
"""
content = re.sub(old_handle, new_handle, content, flags=re.DOTALL)

# Etape C : Ajouter la popup visuelle à la fin du return de ComponentHub
modal_ui = """
      {isCategoryModalOpen && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.85)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:9999, backdropFilter:'blur(4px)'}}>
          <div className="card" style={{width: 450, padding: 30, background: '#0b1121', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'}}>
            <h3 style={{marginTop:0, marginBottom: 8, fontSize: 18, color: '#fff'}}>Nouvelle catégorie</h3>
            <p style={{color:'#91a0b5', fontSize: 14, marginBottom: 24}}>Ajoutez une catégorie pour classer les composants métiers Orange.</p>
            <input 
              type="text" 
              placeholder="Ex: Navigation, Popups, Formulaires..." 
              value={newCategoryName}
              onChange={e => setNewCategoryName(e.target.value)}
              style={{width:'100%', padding:'14px', background:'rgba(0,0,0,0.3)', border:'1px solid rgba(255,255,255,0.15)', color:'#fff', borderRadius:8, marginBottom: 24, fontSize: 15, outline: 'none'}}
              autoFocus
            />
            <div style={{display:'flex', justifyContent:'flex-end', gap: 12}}>
              <button className="button ghost" onClick={() => setIsCategoryModalOpen(false)} style={{padding: '10px 20px'}}>Annuler</button>
              <button className="button primary" onClick={submitCategory} style={{padding: '10px 20px'}}>Créer la catégorie</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
"""
# Je remplace la fin du ComponentHub par le code contenant la modale
content = re.sub(r'</div>\s*<CodeBlock code=\{\}\s*/>\s*</div>\s*</div>\s*\);\s*\}', '</div><CodeBlock code={}/></div>' + modal_ui + '\n}', content, flags=re.DOTALL)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

