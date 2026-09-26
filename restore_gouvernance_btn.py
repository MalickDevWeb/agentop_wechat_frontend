with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

old_screens = """const screens = [
  { id: 'twin', label: 'Digital Twin', icon: Bot },
  { id: 'heal', label: 'GitHub Auto-Heal', icon: GitBranch },
  { id: 'brain', label: 'Explorateur de Cerveau', icon: Search },
  { id: 'leaderboard', label: 'Leaderboard', icon: Activity },
  { id: 'integrations', label: 'Intégrations & IDE', icon: Link2 },
  { id: 'components', label: 'UI Components', icon: Code2 },
]"""

new_screens = """const screens = [
  { id: 'twin', label: 'Digital Twin', icon: Bot },
  { id: 'heal', label: 'GitHub Auto-Heal', icon: GitBranch },
  { id: 'brain', label: 'Explorateur de Cerveau', icon: Search },
  { id: 'leaderboard', label: 'Leaderboard', icon: Activity },
  { id: 'integrations', label: 'Intégrations & IDE', icon: Link2 },
  { id: 'components', label: 'UI Components', icon: Code2 },
  { id: 'gouvernance', label: 'Gouvernance Complète', icon: ShieldCheck },
]"""

content = content.replace(old_screens, new_screens)

old_admin_map = "{[screens[0],screens[4]].map"
new_admin_map = "{[screens[0], screens[4], screens[6]].map"
content = content.replace(old_admin_map, new_admin_map)

# Juste au cas où ShieldCheck n'est pas importé globalement, bien qu'il le soit dans Brain
if "ShieldCheck" not in content[:500]:
    content = content.replace("import {", "import { ShieldCheck,", 1)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
