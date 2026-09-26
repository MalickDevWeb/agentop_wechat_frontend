with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

target = '<button className="button ghost" type="button" onClick={()=>window.open("https://marketplace.visualstudio.com/items?itemName=agentops.agentops-vscode","_blank")}>Télécharger l’extension <Download size={14} /></button>'

# Remplacement par un bouton désactivé "Bientôt disponible"
replacement = '<button className="button ghost" type="button" disabled style={{opacity: 0.6, cursor: "not-allowed"}}>Bientôt disponible <Download size={14} /></button>'

if target in content:
    content = content.replace(target, replacement)
else:
    # Au cas où le formatage a légèrement bougé
    import re
    content = re.sub(
        r'<button[^>]*?Télécharger l’extension.*?</button>', 
        replacement, 
        content
    )

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

