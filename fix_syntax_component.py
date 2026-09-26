with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Le bloc cassé :
bad_block = """function ComponentHub({

  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
 isDeveloper, developerTrusted, onGrantDeveloperTrust }: { isDeveloper: boolean; developerTrusted: boolean; onGrantDeveloperTrust: () => void }) {"""

good_block = """function ComponentHub({ isDeveloper, developerTrusted, onGrantDeveloperTrust }: { isDeveloper: boolean; developerTrusted: boolean; onGrantDeveloperTrust: () => void }) {
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");"""

content = content.replace(bad_block, good_block)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
