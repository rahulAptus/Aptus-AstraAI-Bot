import "./SideBar.css";
import { motion } from "framer-motion";
// import { assets } from "../../assets/assets";
import { FaRobot } from "react-icons/fa"; // AI Assistant Icon

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
                <h2 className="title">
                    <FaRobot className="ai-icon" /> AI Assistant
                </h2>
            </div>

            {/* Sidebar Introduction */}
            <div className="top">
                <p className="sidebar-intro">
                    Welcome to your AI-powered workspace! Ask questions, analyze documents, and gain insights effortlessly.
                </p>
            </div>

            {/* Key Features Section */}
            <h2 className="features-title">Key Features</h2>
            <ul className="features">
                <motion.li whileHover={{ scale: 1.05 }} className="feature-item">
                    <span className="icon">💬</span> <strong>Smart Conversations</strong>
                </motion.li>
                <motion.li whileHover={{ scale: 1.05 }} className="feature-item">
                    <span className="icon">📚</span> <strong>Deep Document Analysis</strong>
                </motion.li>
                <motion.li whileHover={{ scale: 1.05 }} className="feature-item">
                    <span className="icon">🔐</span> <strong>Secure & Private</strong>
                </motion.li>
                <motion.li whileHover={{ scale: 1.05 }} className="feature-item">
                    <span className="icon">⚡</span> <strong>Instant Answers</strong>
                </motion.li>
            </ul>

            {/* Call to Action Button */}
            <div className="cta">
                <button className="try-btn" > Try AI Now</button>
            </div>

            {/* Footer Section */}
            <div className="footer">
                <p className="version">Version <strong>1.0.0</strong></p>
                <p>© 2025 AI Assistant. All rights reserved.</p>
            </div>
        </motion.div>
    );
}

export default Sidebar;
