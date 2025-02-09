import React from "react";
import "./Chatloader.css";

export const ChatLoader = () => {
  return (
    <div className="chat-loader">
      <div className="chat-loader-content">
        <div className="bouncing-dots">
          <div className="dot" />
          <div className="dot" />
          <div className="dot" />
        </div>
        <div className="loading-lines">
          <div className="loading-line" />
          <div className="loading-line" />
        </div>
      </div>
    </div>
  );
};

export default ChatLoader;
