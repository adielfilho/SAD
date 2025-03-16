import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home/home.js"; // Página inicial
import AppTopsis from "./App";   // Página principal do TOPSIS

function App() {
  return (
    <Router>
      <Routes>
        {/* Define a rota inicial */}
        <Route path="/" element={<Home />} />

        {/* Define a rota para o cálculo do TOPSIS */}
        <Route path="/topsis" element={<AppTopsis />} />
      </Routes>
    </Router>
  );
}

export default App;
