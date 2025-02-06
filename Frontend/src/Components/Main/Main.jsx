import { useState } from "react";
import "./Main.css";
import { assets } from "../../assets/assets";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";

const Main = () => {
  const [prompt, setPrompt] = useState("");
  const [input, setInput] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [sources, setSources] = useState([]);

  const sendRequest = async () => {
    setShowResult(true);
    setLoading(true);
    if (input.trim() === "") return;
    setPrompt((prev) => [...prev, input]);
    try {
      const res = await axios.post("http://localhost:8000/prompt", {
        prompt: input,
      });
      setLoading(false);
      const data = res.data[0] || {}; // Default to an empty object if undefined
      let responseText = data.chatbot_response;
      const isHTML = /<\/?[a-z][\s\S]*>/i.test(responseText);
      let accumulatedText = "";
      if (isHTML) {
        setResult(responseText);
      } else {
        responseText.split("").forEach((char, index) => {
          setTimeout(() => {
            accumulatedText += char;
            setResult(accumulatedText);
          }, index * 50); // Simulate streaming effect (50ms delay per character)
        });
      }
      // Sources are fetched from the Backend
      let sourceArray = data.sources || [];
      if (typeof sourceArray === "string") {
        sourceArray = sourceArray.split(",").map((source) => source.trim()); // Split on commas if it's a string
      }
      setInput("");
      setSources(sourceArray); // Update sources
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
              <FontAwesomeIcon icon={faUser} color="#8cc63e" size="xl" />
              <p>{prompt}</p>
            </div>
            <div className="result-data">
              <img
                src={assets.logo_buddy}
                width={"100px"}
                height={"40px"}
                alt=""
              />
              {loading ? (
                <div className="loader"></div>
              ) : (
                <div className="result-text">
                  <h3>Sources</h3>
                  <div className="sources">
                    {sources.length > 0 ? (
                      sources.map((source, index) => (
                        <div key={index} className="source_box">
                          <a
                            href={source}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Aptus Data Labs
                          </a>
                        </div>
                      ))
                    ) : (
                      <p>No sources available</p>
                    )}
                  </div>
                  <p dangerouslySetInnerHTML={{ __html: result }}></p>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="main-bottom">
          <div className="search-box">
            <input
              onChange={(e) => setInput(e.target.value)}
              value={input}
              type="text"
              placeholder="Enter a prompt here "
            />
            <div>
              <img src={assets.gallery_icon} alt="" />
              <img src={assets.mic_icon} alt="" />
              {input ? (
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
