import { useCallback, useState } from 'react';
import './App.css';
import Search from '../search'
import Results from '../results'

function App() {
  const [searchTerms, setSearchTerms] = useState({value: '', unit: '1'});

  const handleChange = useCallback(event => {
    const name = event.target.name;
    const value = event.target.value;
    setSearchTerms(s => ({...s, [name]: value}));
  }, []);

  return (
    <div className="App">
      <h1>Numbers in context</h1>
      <Search handleChange={handleChange} />
      <Results searchTerms={searchTerms} />
    </div>
  );
}

export default App;
