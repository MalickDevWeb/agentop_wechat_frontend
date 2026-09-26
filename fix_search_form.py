with open("app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

logic_old = """  const handleSearch = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchQuery.trim() !== '') {
      setIsSearching(true);
      setSearchResult(null);
      try {
        const res = await fetch(`${API_URL}/memory/prepare`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ project_id: 'mp-afritrips', prompt: searchQuery })
        });
        const data = await res.json();
        setSearchResult(data.context || "Aucune réponse trouvée.");
      } catch (err) {
        setSearchResult("Erreur lors de la recherche vectorielle.");
      }
      setIsSearching(false);
    }
  };"""

logic_new = """  const executeSearch = async (e?: any) => {
    if (e) e.preventDefault();
    if (searchQuery.trim() === '') return;
    setIsSearching(true);
    setSearchResult(null);
    try {
      const res = await fetch(`${API_URL}/memory/prepare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_id: 'mp-afritrips', prompt: searchQuery })
      });
      const data = await res.json();
      setSearchResult(data.context || "Aucune réponse trouvée.");
    } catch (err) {
      setSearchResult("Erreur lors de la recherche vectorielle.");
    }
    setIsSearching(false);
  };"""

content = content.replace(logic_old, logic_new)

ui_old = """      <div className="brain-search">
        <Sparkles size={20} />
        <input 
          placeholder="Posez une question sur l’architecture du projet... (Appuyez sur Entrée)" 
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          onKeyDown={handleSearch}
          disabled={isSearching}
        />
        <kbd>⌘ K</kbd>
      </div>"""

ui_new = """      <form className="brain-search" onSubmit={executeSearch} style={{display:'flex', alignItems:'center'}}>
        <Sparkles size={20} />
        <input 
          placeholder="Posez une question sur l'architecture..." 
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          disabled={isSearching}
          style={{flex:1, background:'transparent', border:'none', color:'white', outline:'none'}}
        />
        <button type="submit" className="button primary" disabled={isSearching} style={{padding:'6px 16px', marginLeft: 10, borderRadius: 6, fontSize: 13, height: '100%'}}>
          {isSearching ? 'Recherche...' : 'Rechercher'}
        </button>
      </form>"""

content = content.replace(ui_old, ui_new)

with open("app/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
