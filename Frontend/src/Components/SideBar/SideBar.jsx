/* eslint-disable react/jsx-key */
import { useContext } from "react";
import "./SideBar.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGear } from "@fortawesome/free-solid-svg-icons";

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="top">
        <p className="sidebar-intro">
          Welcome to your AI assistant! Explore insights, ask questions, and
          interact with documents seamlessly. Let’s make your experience
          efficient and engaging.
        </p>
      </div>
      <div className="bottom">
        <div className="bottom-item">
          <button className="settings">
            <FontAwesomeIcon icon={faGear} color="#8cc63e" size="xl" />
            <p>Settings</p>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
