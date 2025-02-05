/* eslint-disable react/jsx-key */
import { useContext } from "react";
import "./SideBar.css";
import { assets } from "../../assets/assets";
import { Context } from "../../context/context";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGear, faPlus } from "@fortawesome/free-solid-svg-icons";

function Sidebar() {
  // const { onSent, prevPrompts, setRecentPrompt, newChat } = useContext(Context);
  // const loadPrompt = async (prompt) => {
  //   setRecentPrompt(prompt);
  //   await onSent(prompt);
  // };

  return (
    <div className="sidebar">
      <div className="top">
        <div>
          <button className="new-chat">
            <FontAwesomeIcon icon={faPlus} color="#8cc63e" size="lg" />
            <p>New Chat</p>
          </button>
        </div>
        {/* <div className="recent">
          <p className="recent-title">Recent</p>
          {prevPrompts.map((item, index) => {
            return (
              <div onClick={() => loadPrompt(item)} className="recent-entry">
                <img src={assets.message_icon} alt="" />
                <p>{item.slice(0, 18)} ...</p>
              </div>
            );
          })}
        </div> */}
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
