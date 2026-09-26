import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Vérifier si const [isAdmin, setIsAdmin] existe
if "const [isAdmin, setIsAdmin]" not in content:
    # L'ajouter juste après isDeveloper
    content = content.replace(
        "const [isDeveloper, setIsDeveloper] = useState(false);",
        "const [isDeveloper, setIsDeveloper] = useState(false);\n  const [isAdmin, setIsAdmin] = useState(false);"
    )
    # Si isDeveloper n'existe pas non plus, on le met au début du composant App/Dashboard
    if "const [isAdmin, setIsAdmin]" not in content:
        content = content.replace(
            "const [screen, setScreen] = useState",
            "const [isAdmin, setIsAdmin] = useState(false);\n  const [screen, setScreen] = useState"
        )

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
