import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Proposals from "./pages/Proposals.jsx";
import Navbar from "./components/Navbar.jsx";
import Users from "./pages/Users.jsx";

function App() {
  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/proposals" element={<Proposals />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
