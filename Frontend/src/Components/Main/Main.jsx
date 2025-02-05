import { useState } from "react";
import "./Main.css";
import { assets } from "../../assets/assets";
import axios from "axios";

const Main = () => {
  const [prompt, setPrompt] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");

  const sendRequest = async () => {
    try {
      const res = await axios.post("http://localhost:8000/prompt", {
        prompt: prompt,
      });
      setShowResult(true);
      setLoading(false);
      console.log("Response from backend:", res.data);
      setResult(res.data.chatbot_response); // Set the chatbot response directly
    } catch (error) {
      console.error("Error fetching response:", error);
      setShowResult(true);
      setLoading(false);
    }
  };

  return (
    <div className="main">
      <div className="nav">
        <img src={assets.astra_icon} alt="" />
      </div>
      <div className="main-container">
        {!showResult ? (
          <>
            <div className="greet">
              <span>Hello, User</span>
              <p>How may I help you today?</p>
            </div>
            <div className="cards">
              <div className="card">
                <p>Suggest beautiful places to see on an upcoming road trip</p>
                <img src={assets.compass_icon} alt="" />
              </div>
              <div className="card">
                <p>Briefly summarize this concept: urban planning</p>
                <img src={assets.bulb_icon} alt="" />
              </div>
              <div className="card">
                <p>Brainstorm team bonding activities for our work retreat</p>
                <img src={assets.message_icon} alt="" />
              </div>
              <div className="card">
                <p>Improve the readability of the following code</p>
                <img src={assets.code_icon} alt="" />
              </div>
            </div>
          </>
        ) : (
          <div className="result">
            <div className="result-title">
              <img src={assets.user_icon} alt="" />
              <p>{prompt}</p>
            </div>
            <div className="result-data">
              <img src={assets.gemini_icon} alt="" />
              {loading ? (
                <div className="loader">
                  <hr />
                  <hr />
                  <hr />
                </div>
              ) : (
                <p dangerouslySetInnerHTML={{ __html: result }}></p>
              )}
            </div>
          </div>
        )}

        <div className="main-bottom">
          <div className="search-box">
            <input
              onChange={(e) => setPrompt(e.target.value)}
              value={prompt}
              type="text"
              placeholder="Enter a prompt here "
            />
            <div>
              <img src={assets.gallery_icon} alt="" />
              <img src={assets.mic_icon} alt="" />
              {prompt ? (
                <img
                  onClick={() => sendRequest()}
                  src={assets.send_icon}
                  alt=""
                />
              ) : null}
            </div>
          </div>
          <p className="bottom-info">
            Gemiini may display inaccurate info, including about people, so
            double-click its responses. Your privacy and Gemini Apps
          </p>
        </div>
      </div>
    </div>
  );
};

export default Main;
