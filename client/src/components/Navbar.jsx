import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link to="/" className="text-lg font-bold">
          MyApp
        </Link>
        <div className="space-x-4">
          <Link to="/users" className="hover:text-gray-300">Users</Link>
          <Link to="/proposals" className="hover:text-gray-300">Proposals</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
