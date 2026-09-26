import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Le problème : `function ComponentHub({ isDeveloper ... }) {` a été cassé par le regex.
# Je vais chercher exactement "function ComponentHub" et reconstruire le bloc proprement.

# Je vais récupérer la ligne où ComponentHub est défini.
lines = content.split('\n')
for i, line in enumerate(lines):
    if "const [isCategoryModalOpen" in line:
        pass # c'est la ligne injectée au mauvais endroit

# Plutôt que de bricoler les lignes, je vais recharger le fichier depuis le git log et appliquer la diff proprement,
# ou simplement utiliser regex pour nettoyer les useState au milieu des props.

content_clean = re.sub(r'function ComponentHub\(\{\s*isDeveloper.*?const \[isCategoryModalOpen.*?useState\(\"\"\);', 
                       'function ComponentHub({ isDeveloper, developerTrusted, onGrantDeveloperTrust }: any) {\n  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);\n  const [newCategoryName, setNewCategoryName] = useState("");', 
                       content, flags=re.DOTALL)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content_clean)
