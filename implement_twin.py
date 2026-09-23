import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Implémentation du Twin
twin_state = """const [reviews, setReviews] = useState([
    { id: '#482', title: 'feat: integration API Orange Money', status: 'Validé par l\\'IA', confidence: 99, time: 'Il y a 2 min', color: 'green' },
    { id: '#481', title: 'fix: bug de paiement', status: 'Rejeté', confidence: 45, time: 'Il y a 1h', color: 'red' }
  ])
  useEffect(() => {
    fetch(`${API_URL}/twin/`)
      .then(r=>r.json())
      .then(data => {
        if(data && data.length) setReviews(data.map(d => ({id: '#'+d.id, title: d.title, status: d.status, confidence: d.confidence, time: d.time, color: d.confidence > 90 ? 'green' : 'red'})))
      }).catch(e => console.log(e))
  }, [])
"""

if "fetch(`${API_URL}/twin/`)" not in content:
    content = content.replace("function Twin() {", f"function Twin() {{\n  {twin_state}")
    # Remplacer la map
    content = re.sub(r"\{\s*\[\s*\{\s*id:\s*'#482'.*?\]\.map", "{reviews.map", content, flags=re.DOTALL)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
