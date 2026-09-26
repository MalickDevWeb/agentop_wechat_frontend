import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ajouter le state
if "showCommentModal" not in content:
    content = content.replace(
        "const [commenting, setCommenting] = useState(false);",
        "const [commenting, setCommenting] = useState(false);\n  const [showCommentModal, setShowCommentModal] = useState(false);"
    )

# 2. Remplacer l'alerte native par l'ouverture de la popup
content = re.sub(r'alert\(`AgentOps.*?`\);', "setShowCommentModal(true);", content, flags=re.DOTALL)

# 3. Injecter la popup avant la fin du composant CodeReview
modal_jsx = """
      {showCommentModal && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.85)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:9999, backdropFilter:'blur(4px)'}}>
          <div className="card" style={{width: 500, padding: 0, background: '#0d1117', border: '1px solid #30363d', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)', borderRadius: 12, overflow: 'hidden'}}>
            <div style={{background: '#161b22', padding: '16px 20px', borderBottom: '1px solid #30363d', display: 'flex', alignItems: 'center', gap: 10}}>
              <Bot size={20} color="#8b5cf6" />
              <span style={{color: '#c9d1d9', fontWeight: 600, fontSize: 14}}>AgentOps Copilot</span>
              <span style={{color: '#8b949e', fontSize: 12}}>a laissé un commentaire</span>
            </div>
            <div style={{padding: '24px 20px'}}>
              <p style={{color: '#c9d1d9', fontSize: 14, lineHeight: 1.6, margin: 0}}>
                Excellente initiative de passer au JWT ! Cela sécurise l'API et évite l'accès direct en base.<br/><br/>
                Le code respecte nos standards de sécurité. PR prête à être mergée. ✅
              </p>
            </div>
            <div style={{padding: '16px 20px', borderTop: '1px solid #30363d', display: 'flex', justifyContent: 'flex-end'}}>
              <button onClick={() => setShowCommentModal(false)} style={{background: '#238636', color: 'white', border: '1px solid rgba(255,255,255,0.1)', padding: '6px 16px', borderRadius: 6, fontWeight: 500, cursor: 'pointer', fontSize: 14}}>
                Fermer l'aperçu
              </button>
            </div>
          </div>
        </div>
      )}
"""

end_of_codereview = """          )}
        </div>
      </div>
    </div>
  );
}"""

new_end_of_codereview = f"""          )}}
        </div>
      </div>
{modal_jsx}
    </div>
  );
}}"""

content = content.replace(end_of_codereview, new_end_of_codereview)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)

