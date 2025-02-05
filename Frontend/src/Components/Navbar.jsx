import "./navbar.css";
export default function Navbar() {
  return (
    <div>
      <nav className="navbar-main">
        <div className="navbar-logo">
          <span>
            Astra<span>AI</span>
          </span>
        </div>
        <div className="navbar-link">
          <button type="button" className="navbar-button">
            Get Started
          </button>
        </div>
      </nav>
    </div>
  );
}
