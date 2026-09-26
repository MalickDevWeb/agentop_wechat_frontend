with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Type strict pour le State DevOps
content = content.replace(
    "const [stats, setStats] = useState({ hoursSaved: 0, resolved: 0, mttr: 0, chart: [], repos: [] });",
    "const [stats, setStats] = useState<{ hoursSaved: number, resolved: number, mttr: number, chart: number[], repos: string[] }>({ hoursSaved: 0, resolved: 0, mttr: 0, chart: [], repos: [] });"
)

# 2. Correction des `any` implicites dans les Fetch (Leaderboard)
content = content.replace(
    "setLeaders(data.map(d => [d.name,",
    "setLeaders(data.map((d: any) => [d.name,"
)

# 3. Correction des `any` implicites dans les Fetch (Twin)
content = content.replace(
    "setReviews(data.map(d => ({id:",
    "setReviews(data.map((d: any) => ({id:"
)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
