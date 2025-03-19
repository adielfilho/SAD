import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home/home.js"; // Página inicial
import Navbar from "./layout/navbar/navbar.js";
import TopsisFormPage from "./pages/TopsisFormPage/topsisFormPage.js";
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Define a rota inicial */}
        <Route path="/" element={<Home />} />

        <Route path="/TopsisForm" element={<TopsisFormPage />} />

      </Routes>
    </Router>
  );
}

export default App;
