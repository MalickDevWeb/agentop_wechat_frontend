import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Implementation du Cerveau (Brain)
brain_mock = r"const \[searchQuery, setSearchQuery\] = useState\(''\)"
brain_state = """const [searchQuery, setSearchQuery] = useState('')
  const [trustedDocs, setTrustedDocs] = useState([
    { title: 'Architecture Orange Money', type: 'Architecture', date: 'Mise à jour: 12 Sept', author: 'Awa Ba' },
    { title: 'Gestion des Webhooks PayDunya', type: 'Intégration', date: 'Mise à jour: 15 Sept', author: 'Ousmane Mbaye' }
  ])
  useEffect(() => {
    fetch(`${API_URL}/memory/dashboard/chunks?project_id=mp-afritrips-v1`)
      .then(r=>r.json())
      .then(data => {
        if (data && data.chunks && data.chunks.length > 0) {
           setTrustedDocs(data.chunks.map(c => ({
              title: c.content.substring(0, 40) + '...',
              type: 'Règle IA',
              date: 'Récemment',
              author: 'AgentOps'
           })))
        }
      }).catch(e => console.log(e))
  }, [])
"""
content = re.sub(brain_mock, brain_state, content)

# 2. Remplacement dans l'affichage du Brain
content = re.sub(r"\{\s*\[\s*\{\s*title:\s*'Standardisation WXML'.*?\]\.map", "{trustedDocs.map", content, flags=re.DOTALL)


# 3. Implementation de l'Upload Cloudinary dans ComponentHub
cloud_logic = """const handlePublish = async () => {
    setIsPublishing(true)
    try {
      // Pour la démo, on simule une image si on en a pas
      let finalImageUrl = "https://res.cloudinary.com/qudmvipg/image/upload/v1700000000/placeholder.png"
      
      const res = await fetch(`${API_URL}/components/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newComponent.name || "Nouveau Composant",
          tags: newComponent.tags || "WXML",
          author: "Admin Sonatel",
          initials: "AS",
          preview: "Aperçu du composant",
          code: { WXML: newComponent.wxml || "" },
          image_url: finalImageUrl
        })
      })
      
      if(res.ok) {
        // Rafraîchir la liste
        const fresh = await fetch(`${API_URL}/components/`).then(r=>r.json())
        setComponents(fresh)
        setShowPublishModal(false)
        setNewComponent({ name: '', tags: '', wxml: '', wxss: '', js: '', json: '' })
      }
    } catch(err) {
      console.error(err)
    } finally {
      setIsPublishing(false)
    }
  }"""

if "const handlePublish" not in content:
    content = content.replace("const [isPublishing, setIsPublishing] = useState(false)", f"const [isPublishing, setIsPublishing] = useState(false)\n  {cloud_logic}")
    # Relier le bouton Publier
    content = content.replace("onClick={() => {\n                  setIsPublishing(true)\n                  setTimeout(() => {\n                    setIsPublishing(false)\n                    setShowPublishModal(false)\n                  }, 1500)\n                }}", "onClick={handlePublish}")

# 4. Affichage de l'image si elle existe
image_render = """<div className="w-16 h-16 rounded-xl bg-purple-500/20 flex items-center justify-center mr-4 flex-shrink-0 border border-purple-500/30 overflow-hidden">
                {comp.image_url ? <img src={comp.image_url} className="w-full h-full object-cover" /> : <Code2 className="w-8 h-8 text-purple-400" />}
              </div>"""

content = re.sub(r'<div className="w-16 h-16 rounded-xl bg-purple-500/20 flex items-center justify-center mr-4 flex-shrink-0 border border-purple-500/30">\s*<Code2 className="w-8 h-8 text-purple-400" />\s*</div>', image_render, content)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
