import "./SideBar.css";
import { motion } from "framer-motion";
import { assets } from "../../assets/assets";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"; // Font Awesome Icon
import {
  faBolt,
  faComment,
  faFile,
  faShieldHalved,
} from "@fortawesome/free-solid-svg-icons"; // Font Awesome Icon

function Sidebar() {
  return (
    <motion.div
      className="sidebar"
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {/* Logo Section with AI Icon */}
      <div className="logo">
        <img src={assets.astra_icon} />
      </div>

      {/* Sidebar Introduction */}
      <div className="top">
        <p className="sidebar-intro">
          Welcome to your AI-powered workspace! Ask questions, analyze
          documents, and gain insights effortlessly.
        </p>
      </div>

      {/* Key Features Section */}
      <h2 className="features-title">Key Features</h2>
      <div className="features">
        <motion.div whileHover={{ scale: 1.05 }} className="feature-item">
          <FontAwesomeIcon icon={faComment} size="lg" color="#0062a5" />
          <h4>Smart Conversations</h4>
        </motion.div>
        <motion.div whileHover={{ scale: 1.05 }} className="feature-item">
          <FontAwesomeIcon icon={faFile} size="lg" color="#0062a5" />
          <h4>Deep Document Analysis</h4>
        </motion.div>
        <motion.div whileHover={{ scale: 1.05 }} className="feature-item">
          <FontAwesomeIcon icon={faShieldHalved} size="lg" color="#0062a5" />
          <h4>Secure and Private</h4>
        </motion.div>
        <motion.div whileHover={{ scale: 1.05 }} className="feature-item">
          <FontAwesomeIcon icon={faBolt} size="lg" color="#0062a5" />
          <h4>Faster Response Time </h4>
        </motion.div>
      </div>

      {/* Call to Action Button */}
      <div className="cta">
        <button className="try-btn"> Try AI Now</button>
      </div>

      {/* Footer Section */}
      <div className="footer">
        <p className="version">
          Version <strong>1.0.0</strong>
        </p>
        <p>© 2025 AI Assistant. All rights reserved.</p>
      </div>
    </motion.div>
  );

export default Sidebar;
