import { useCallback, useState } from 'react';
import './App.css';
import Search from '../search'
import Results from '../results'
import Title from '../title'
import Footer from '../footer'

function App() {
  const [searchTerms, setSearchTerms] = useState({value: '0', unit: 'none'});

  const handleChange = useCallback(event => {
    const name = event.target.name;
    const value = event.target.value;
    setSearchTerms(s => ({...s, [name]: value}));
  }, []);

  return (
    <div className="App">
      <Title />
      <Search handleChange={handleChange} />
      <Results searchTerms={searchTerms} />
      <Footer />
    </div>
  );
}

export default App;
