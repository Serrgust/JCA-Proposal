import { Outlet } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";

function App() {
  return (
    <div>
      <Navbar /> {/* This is the Navbar component */}
      <div className="container mx-auto p-4">
        <Outlet /> {/* This is where the child pages (Home, Users, Proposals) will be rendered */}
      </div>
    </div>
  );
}

export default App;
