with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Enlever React. devant useState et useEffect
content = content.replace("React.useState<any[]>", "useState<any[]>")
content = content.replace("React.useEffect(()", "useEffect(()")

# 2. Ajouter l'action obligatoire sur le Header de la gouvernance
old_header = 'Header eyebrow="SÉCURITÉ & ACCÈS" title="Gouvernance Complète" desc="Gérez les développeurs, leurs droits d\'ingestion et de publication." />'
new_header = 'Header eyebrow="SÉCURITÉ & ACCÈS" title="Gouvernance Complète" desc="Gérez les développeurs, leurs droits d\'ingestion et de publication." action="Exporter CSV" />'

content = content.replace(old_header, new_header)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
