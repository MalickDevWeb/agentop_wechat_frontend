with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Bouton "Télécharger l'extension" (correction de l'apostrophe typographique)
content = content.replace(
    '<button className="button ghost">Télécharger l’extension <Download size={14} /></button>',
    '<button className="button ghost" type="button" onClick={()=>window.open("https://marketplace.visualstudio.com/items?itemName=agentops.agentops-vscode","_blank")}>Télécharger l’extension <Download size={14} /></button>'
)

# 2. Bouton filtre "30 derniers jours" dans Heal
content = content.replace(
    '<button className="select">30 derniers jours <ChevronDown size={13} /></button>',
    '<button className="select" type="button" onClick={(e) => { e.currentTarget.textContent = "Ce mois-ci"; }}>30 derniers jours <ChevronDown size={13} /></button>'
)

# 3. Composant Header : Ajouter le support de l'événement onClick
content = content.replace(
    'function Header({eyebrow,title,desc,action}:{eyebrow:string;title:string;desc:string;action:string}) { return <div className="hero-row"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{desc}</p></div><button className="button primary"><GitBranch size={14} /> {action}</button></div> }',
    'function Header({eyebrow,title,desc,action,onAction}:{eyebrow:string;title:string;desc:string;action:string;onAction?:()=>void}) { return <div className="hero-row"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{desc}</p></div><button className="button primary" type="button" onClick={onAction}><GitBranch size={14} /> {action}</button></div> }'
)

# 4. Assigner des onAction pertinents aux Headers
content = content.replace(
    'action="Connecter GitHub" />',
    'action="Connecter GitHub" onAction={() => alert("Redirection vers l\'intégration GitHub...")} />'
)
content = content.replace(
    'action="Partager une règle" />',
    'action="Partager une règle" onAction={() => { const ev = new CustomEvent("navigate",{detail:"integrations"}); window.dispatchEvent(ev); }} />'
)
content = content.replace(
    'action="Exporter le rapport" />',
    'action="Exporter le rapport" onAction={() => alert("Génération du rapport PDF...")} />'
)
content = content.replace(
    'action="Ajouter une intégration" />',
    'action="Ajouter une intégration" onAction={() => alert("Ouverture du catalogue d\'intégrations...")} />'
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Derniers boutons connectés !")
