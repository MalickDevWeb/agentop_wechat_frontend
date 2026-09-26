import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Le problème est qu'on a ouvert une accolade pour une condition ternary { analysisResult === '' ? ... : <> ...
# mais on ne l'a jamais fermée avant le </Panel>
# Cherchons le bloc fautif :
bad_end = "<div style={{display:'none'}}></div></></Panel>"
good_end = "<div style={{display:'none'}}></div></>}</Panel>" # on ajoute l'accolade fermante }

if bad_end in content:
    content = content.replace(bad_end, good_end)
    print("Correction JSX appliquée (ajout de l'accolade fermante du ternaire).")
else:
    print("Le marqueur n'a pas été trouvé, on va utiliser regex.")
    
with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
