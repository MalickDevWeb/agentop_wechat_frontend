import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. On s'assure que useEffect est importé
if "import { useState, useEffect }" not in content:
    content = content.replace("import { useState }", "import { useState, useEffect }")

# 2. Ajout de l'URL de base de l'API
if "const API_URL" not in content:
    content = content.replace("const screens =", "const API_URL = 'http://localhost:8000/api/v1';\n\nconst screens =")

# 3. Composant Leaderboard
leader_mock = r"\{\[\['Marie Laurent','ML','248','\+18%','Top contributor'\],\['Simon Bernard','SB','184','\+12%','Régulier'\],\['Clara Dubois','CD','156','\+24%','En progression'\],\['Alex Martin','AM','121','\+8%','Contributeur'\]\]\.map\(\(r,i\)=>"
leader_state = """
  const [leaders, setLeaders] = useState([['Marie Laurent','ML','248','+18%','Top contributor'],['Simon Bernard','SB','184','+12%','Régulier'],['Clara Dubois','CD','156','+24%','En progression'],['Alex Martin','AM','121','+8%','Contributeur']]);
  useEffect(() => {
    fetch(`${API_URL}/team/leaderboard`).then(r=>r.json()).then(data => {
      if(data && data.length) setLeaders(data.map(d => [d.name, d.initials, d.score.toString(), d.growth, d.badge]))
    }).catch(e => console.log("Backend offline, using mocks"));
  }, []);
  
"""
if "const [leaders" not in content:
    content = content.replace("function Leaderboard() { return <div", f"function Leaderboard() {{{leader_state}return <div")
    content = re.sub(leader_mock, "{leaders.map((r,i)=>", content)


# 4. Composant Heal (Crashes)
crashes_mock = r"\{\[\['TypeError: Cannot read properties of undefined','platform-api','Il y a 8 min','PR créée automatiquement','green'\],\['TimeoutError: Database connection','data-pipeline','Il y a 42 min','Analyse en cours','amber'\],\['BuildError: Module not found','agentops-web','Il y a 2 h','Fusionnée','blue'\]\]\.map\(x=>"
crashes_state = """
  const [crashes, setCrashes] = useState([['TypeError: Cannot read properties of undefined','platform-api','Il y a 8 min','PR créée automatiquement','green'],['TimeoutError: Database connection','data-pipeline','Il y a 42 min','Analyse en cours','amber'],['BuildError: Module not found','agentops-web','Il y a 2 h','Fusionnée','blue']]);
  useEffect(() => {
    fetch(`${API_URL}/devops/crashes`).then(r=>r.json()).then(data => {
      if(data && data.length) setCrashes(data.map(d => [d.error, d.repo, d.time, d.status, d.tone]))
    }).catch(e => console.log("Backend offline, using mocks"));
  }, []);
"""
if "const [crashes" not in content:
    content = content.replace("function Heal() { return <div", f"function Heal() {{{crashes_state}return <div")
    content = re.sub(crashes_mock, "{crashes.map(x=>", content)


# 5. Composant ComponentHub
components_mock_search = r"const components = \[\n\s*\{ name: 'Bouton Paiement Orange Money'.*?\n\s*\]"
components_mock_replace = """const [components, setComponents] = useState([
    { name: 'Bouton Paiement Orange Money', tags: 'WXML · UI · Mobile Money', author: 'Awa Ba', initials: 'AB', preview: 'Payer 25 000 FCFA' },
    { name: 'Carte solde client', tags: 'WXML · Data · Orange Money', author: 'Ousmane Mbaye', initials: 'OM', preview: 'Solde disponible 85 400 F' },
    { name: 'Modal de confirmation', tags: 'WXML · Feedback', author: 'Marie Laurent', initials: 'ML', preview: 'Confirmer la transaction' },
  ])
  
  useEffect(() => {
    fetch(`${API_URL}/components`).then(r=>r.json()).then(data => {
      if(data && data.length) setComponents(data)
    }).catch(e => console.log("Backend offline, using mocks"));
  }, []);"""
if "setComponents" not in content:
    content = re.sub(components_mock_search, components_mock_replace, content, flags=re.DOTALL)


with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Tous les composants ont été connectés à l'API !")
