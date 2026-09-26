import re

with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const [showCommentModal, setShowCommentModal] = useState(false);", "const [showCommentModal, setShowCommentModal] = useState(false);\n  const [reviewText, setReviewText] = useState('');")

old_handle_comment = '''  const handleComment = () => {
    setCommenting(true);
    setTimeout(() => {
      setCommenting(false);
      setShowCommentModal(true);
    }, 1500);
  };'''

new_handle_comment = '''  const handleComment = async () => {
    setCommenting(true);
    try {
      const res = await fetch('https://wechat-agent-5y0i.onrender.com/api/v1/devops/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pr_id: "482", code_diff: "+ const token = req.headers.jwt;\\n- const token = req.query.token;\\n+ // FIXME: JWT_SECRET hardcoded for testing\\n+ const secret = 'super-secret-key';" })
      });
      const data = await res.json();
      setReviewText(data.review || "Revue terminée.");
    } catch (e) {
      setReviewText("🤖 **AgentOps (Mode Hors-Ligne)**\\n\\nLa revue n'a pas pu être effectuée (erreur réseau).");
    }
    setCommenting(false);
    setShowCommentModal(true);
  };'''
content = content.replace(old_handle_comment, new_handle_comment)

old_modal_content = '''<p style={{color: '#c9d1d9', fontSize: 14, lineHeight: 1.6, margin: 0}}>
                Excellente initiative de passer au JWT ! Cela sécurise l'API et évite l'accès direct en base.<br/><br/>
                Le code respecte nos standards de sécurité. PR prête à être mergée. ✅
              </p>'''

new_modal_content = '''<div style={{color: '#c9d1d9', fontSize: 14, lineHeight: 1.6, margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word', maxHeight: '50vh', overflowY: 'auto'}}>
                {reviewText}
              </div>'''
content = content.replace(old_modal_content, new_modal_content)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
