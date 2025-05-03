import './App.css';
import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Scrape_Page from './components/scrape_page/Scrape_Page.tsx';
import Embed_Page from './components/embed_page/Embed_Page.tsx';
import Query_Page from './components/query_page/Query_Page.tsx';

function App() {
    useEffect(() => {
      document.title = "Player Recognition";
    }, []);

    return (
      <Router>
        <Routes>
          <Route path="/" element={<Scrape_Page />} />
          <Route path="/embed" element={<Embed_Page />} />
          <Route path="/query" element={<Query_Page />} />
        </Routes>
    </Router>
    )
}

export default App
