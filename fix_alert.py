import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer toute l'alerte problématique par une version sécurisée avec backticks (` `)
new_alert = "alert(`AgentOps a analysé le code et généré le commentaire GitHub suivant :\\n\\nExcellente initiative de passer au JWT ! Cela sécurise l'API et évite l'accès direct en base. Le code respecte nos standards. PR prête à être mergée.`);"

# Remplacer tout ce qui ressemble à alert("AgentOps... jusqu'au point-virgule
content = re.sub(r'alert\("AgentOps.*?\);', new_alert, content, flags=re.DOTALL)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
