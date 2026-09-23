import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Crashes — remplacer le useState avec données mock par un tableau vide
old_crashes = """const [crashes, setCrashes] = useState([['TypeError: Cannot read properties of undefined','platform-api','Il y a 8 min','PR créée automatiquement','green'],['TimeoutError: Database connection','data-pipeline','Il y a 42 min','Analyse en cours','amber'],['BuildError: Module not found','agentops-web','Il y a 2 h','Fusionnée','blue']]);"""
new_crashes = """const [crashes, setCrashes] = useState<string[][]>([]);"""
content = content.replace(old_crashes, new_crashes)

# 2. Leaderboard — remplacer les données mock par tableau vide
old_leaders = """const [leaders, setLeaders] = useState([['Marie Laurent','ML','248','+18%','Top contributor'],['Simon Bernard','SB','184','+12%','Régulier'],['Clara Dubois','CD','156','+24%','En progression'],['Alex Martin','AM','121','+8%','Contributeur']]);"""
new_leaders = """const [leaders, setLeaders] = useState<string[][]>([]);"""
content = content.replace(old_leaders, new_leaders)

# 3. Components — remplacer les données mock par tableau vide
old_comps = """const [components, setComponents] = useState([
    { name: 'Bouton Paiement Orange Money', tags: 'WXML · UI · Mobile Money', author: 'Awa Ba', initials: 'AB', preview: 'Payer 25 000 FCFA' },
    { name: 'Carte solde client', tags: 'WXML · Data · Orange Money', author: 'Ousmane Mbaye', initials: 'OM', preview: 'Solde disponible 85 400 F' },
    { name: 'Modal de confirmation', tags: 'WXML · Feedback', author: 'Marie Laurent', initials: 'ML', preview: 'Confirmer la transaction' },"""
new_comps = """const [components, setComponents] = useState<{name:string,tags:string,author:string,initials:string,preview:string}[]>(["""
content = content.replace(old_comps, new_comps)

# 4. profiles (login) — garder mais enlever les emails réels Sonatel et mettre des placeholders
content = content.replace("marie.laurent@orange.sn", "admin@votredomaine.sn")
content = content.replace("awa.ba@orange.sn", "dev@votredomaine.sn")
content = content.replace("ousmane.mbaye@orange.sn", "dev2@votredomaine.sn")

# 5. selected component par défaut — mettre vide
content = content.replace("const [selected, setSelected] = useState('Bouton Paiement Orange Money')", "const [selected, setSelected] = useState('')")

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Toutes les données mock supprimées du frontend !")
