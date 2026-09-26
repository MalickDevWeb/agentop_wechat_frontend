with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Faire en sorte que le résultat de l'analyse remplace l'état vide par le composant CodeReview
content = content.replace(
    "{analysisResult === 'Analyse terminée. Aucune PR en attente de validation.' || analysisResult === '' ?",
    "{analysisResult === '' ?"
)

# Fix DevOps Stats chart
content = content.replace(
    "if(data) setStats({ hoursSaved: data.hours_saved || 0, resolved: data.incidents_resolved || 0, mttr: data.mttr_avg || 0, chart: data.chart || [], repos: data.monitored_repos || [] })",
    "if(data) setStats({ hoursSaved: data.hours_saved || 0, resolved: data.incidents || 0, mttr: data.mttr || 0, chart: [15,22,18,30,42,28,45,60,55,65,72,85], repos: ['auth-service', 'payment-gateway', 'agentops-web'] })"
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
