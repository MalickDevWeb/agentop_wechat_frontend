with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("'✓ Proposer à l'IA'", '"✓ Proposer à l\'IA"')
content = content.replace("'✕ Proposer à l'IA'", '"✕ Proposer à l\'IA"')

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
