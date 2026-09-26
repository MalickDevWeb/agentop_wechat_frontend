import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Je cherche le bouton "Gouvernance complète" pour voir vers où il pointe
# Et je le remplace pour qu'il pointe vers setScreen('gouvernance')
content = re.sub(r'onClick=\{\(\)\s*=>\s*setScreen\(\'leaderboard\'\)\}.*?Gouvernance complète', 
                 r"onClick={() => setScreen('gouvernance')}> <Shield size={16}/> Gouvernance complète", 
                 content)

# Au cas où l'icône diffère :
content = re.sub(r'onClick=\{\(\)\s*=>\s*setScreen\([\'"]leaderboard[\'"]\)\}([^>]*?>[^>]*?Gouvernance complète)',
                 r"onClick={() => setScreen('gouvernance')}\1",
                 content)

# Autre tentative de nettoyage large s'il pointe vers autre chose :
content = re.sub(r'<button className=\{`nav-item \$\{screen===[\'"]gouvernance[\'"]\?[\'"]active[\'"]:[\'"][\'"]\}`\} onClick=\{\(\)=>setScreen\([\'"][^\'"]+[\'"]\)\}([^>]*?>[^>]*?Gouvernance complète)',
                 r'<button className={`nav-item ${screen===\'gouvernance\'?\'active\':\'\'}`} onClick={()=>setScreen(\'gouvernance\')}\1',
                 content)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

