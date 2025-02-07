import { useState, useEffect, useRef } from "react";
import { assets } from "../../assets/assets";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import "./Main.css";

const Main = () => {
  const [prompt, setPrompt] = useState("");
  const [isHTML, setIsHTML] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([]);
  const [sources, setSources] = useState([]);
  const [showSources, setShowSources] = useState(false);
  const [threadId, setThreadId] = useState(0);
  const chatContainerRef = useRef(null);
  const dummyRef = useRef(null); // Reference for auto-scroll

  const generateThreadId = () => {
    return Math.floor(Math.random() * 1000000);
  };

  useEffect(() => {
    setThreadId(generateThreadId());
  }, []);

  const scrollToBottom = () => {
<<<<<<< HEAD
    setTimeout(() => {
      dummyRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
=======
    if (dummyRef.current) {
      dummyRef.current.scrollIntoView({ behavior: "smooth",block: "end"});
    }
>>>>>>> ff59af8f693d5bb8c3ec245430590b81b004f899
  };
  

  useEffect(() => {
    scrollToBottom();
  }, [result, loading]); // Run when messages update

 
  

  // useEffect(() => {
  //   setTimeout(scrollToBottom, 200); // Small delay to ensure message renders first
  // }, [result, loading]);

  const sendRequest = async () => {
    if (prompt.trim() === "") return;
    setShowSources(false);
    setSources([]);
    const userMessage = prompt;
    setResult((prevResult) => [
      ...prevResult,
      { type: "user", text: userMessage },
    ]);
    setShowResult(true);
    setLoading(true);
    setPrompt("");

    setTimeout(() => scrollToBottom(), 50);

    try {
      const res = await axios.post("http://localhost:8020/prompt", {
        prompt: userMessage,
        thread_id: threadId,
      });
      setLoading(false);
      const data = res.data[0] || {}; // Default to an empty object if undefined
      let responseText = data.chatbot_response;
      const isHTML = /<\/?[a-z][\s\S]*>/i.test(responseText);
      let accumulatedText = "";

      if (isHTML) {
        setIsHTML(true);
        setResult((prevResult) => [
          ...prevResult,
          { type: "chatbot", text: responseText },
        ]);
      } else {
        setIsHTML(false);
        responseText.split("").forEach((char, index) => {
          setTimeout(() => {
            accumulatedText += char;
            setResult((prevResult) => {
              // Update only the last chatbot message
              if (
                prevResult.length > 0 &&
                prevResult[prevResult.length - 1].type === "chatbot"
              ) {
                return [
                  ...prevResult.slice(0, -1), // Remove the last chatbot message
                  { type: "chatbot", text: accumulatedText }, // Update it with new text
                ];
              } else {
                return [
                  ...prevResult,
                  { type: "chatbot", text: accumulatedText },
                ];
              }
            });
            // if (index === responseText.length - 1) {
            //   setTimeout(() => {
            //     scrollToBottom();
            //   }, 100);}
            scrollToBottom();
          }, index * 50); // Simulate streaming effect (50ms delay per character)
        });
      }

      let sourceArray = data.sources || [];
      setShowSources(true);
      if (typeof sourceArray === "string") {
        sourceArray = sourceArray.split(",").map((source) => source.trim());
      } else {
        setShowSources(false);
      }
      setSources((prevSource) => [
        ...prevSource,
        { type: "chatbot", text: sourceArray },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setShowResult(true);
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendRequest();
    }
  };

  return (
    <div className="main">
      <motion.div
        className="nav"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <img src={assets.astra_icon} alt="Astra-Logo" />
      </motion.div>

      <div className="main-container" ref={chatContainerRef}>
        {!showResult ? (
          <>
            <motion.div
              className="greet"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.7 }}
            >
              <span>Hello, User</span>
              <p>How may I help you today?</p>
            </motion.div>

            <motion.div
              className="cards"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {[
                {
                  text: "Give me a brief description about Aptus Data Labs",
                  icon: assets.compass_icon,
                },
                {
                  text: "What are the Projects covered by the Aptus Data Labs",
                  icon: assets.bulb_icon,
                },
                {
                  text: "What are the products developed by the Aptus Data Labs",
                  icon: assets.message_icon,
                },
                {
                  text: "Book a meeting with Aptus Data Labs for further information",
                  icon: assets.code_icon,
                },
              ].map((item, index) => (
                <motion.div
                  key={index}
                  className="card"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setPrompt(item.text)}
                >
                  <p>{item.text}</p>
                  <img src={item.icon} alt="Icon" />
                </motion.div>
              ))}
            </motion.div>
          </>
        ) : (
          <>
            <div
              className="chat-history"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              {Array.isArray(result) &&
                result.map((entry, index) => (
                  <motion.div
                    key={index}
                    className={`chat-entry ${
                      entry.type === "user" ? "user-entry" : "chatbot-entry"
                    }`}
                    initial={{
                      x: entry.type === "user" ? 50 : -50,
                      opacity: 0,
                    }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.5 }}
                  >
                    {/* Profile Image */}
                    <img
                      src={
                        entry.type === "user"
                          ? assets.user_avatar
                          : assets.logo_buddy
                      }
                      alt={entry.type === "user" ? "User" : "Chatbot"}
                      className="profile-img"
                    />

                    {/* Message Text */}
                    <div className="message-content">
                      {isHTML ? (
                        <div dangerouslySetInnerHTML={{ __html: entry.text }} />
                      ) : (
                        // Render as Markdown
                        <ReactMarkdown>{entry.text}</ReactMarkdown>
                      )}
                      {showSources && sources.length > 0 && (
                        <div className="sources">
                          <h3>Sources</h3>
                          {sources.map((source, idx) => (
                            <div key={idx} className="source_box">
                              <a
                                href={source}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                {source}
                              </a>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
            </div>
            {/* Loading Indicator */}
            {loading && (
              <motion.div
                className="loader"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
<<<<<<< HEAD
              ></motion.div>
            )}
            <div ref={dummyRef} />
=======
                style={{
                  maxHeight: "calc(100vh - 150px)",
                }}
              >
                {Array.isArray(result) &&
                  result.map((entry, index) => (
                    <motion.div
                      key={index}
                      className={`chat-entry ${
                        entry.type === "user" ? "user-entry" : "chatbot-entry"
                      }`}
                      initial={{
                        x: entry.type === "user" ? 50 : -50,
                        opacity: 0,
                      }}
                      animate={{ x: 0, opacity: 1 }}
                      transition={{ duration: 0.5 }}
                    >
                      {/* Profile Image */}
                      <img
                        src={
                          entry.type === "user"
                            ? assets.user_avatar
                            : assets.logo_buddy
                        }
                        alt={entry.type === "user" ? "User" : "Chatbot"}
                        className="profile-img"
                      />

                      {/* Message Text */}
                      <div className="message-content">
                        {isHTML ? (
                          <div
                            dangerouslySetInnerHTML={{ __html: entry.text }}
                          />
                        ) : (
                          // Render as Markdown
                          <ReactMarkdown>{entry.text}</ReactMarkdown>
                        )}
                        {showSources && sources.length > 0 && (
                          <div className="sources">
                            <h3>Sources</h3>
                            {sources.map((source, idx) => (
                              <div key={idx} className="source_box">
                                <a
                                  href={source}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                >
                                  {source}
                                </a>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
              </div>
              {/* Loading Indicator */}
              {loading && (
                <motion.div
                  className="loader"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                ></motion.div>
              )}
            </div >
            <div ref={dummyRef} style={{ marginBottom: "100px" }}  />
>>>>>>> ff59af8f693d5bb8c3ec245430590b81b004f899
          </>
        )}

        <motion.div
          className="main-bottom"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7 }}
          style={{
            position: "fixed",
            bottom: 0,
            background: "white",
            padding: "0.5rem",
            boxShadow: "none",
            zIndex: 10,
          }}
        >
          <div className="search-box">
            <input
              onChange={(e) => setPrompt(e.target.value)}
              value={prompt}
              type="text"
              placeholder="Chat with Astra - Where Innovation Meets Conversation"
              onKeyDown={handleKeyPress}
            />
            <div>
              {prompt ? (
                <motion.img
                  onClick={sendRequest}
                  src={assets.send_icon}
                  alt="Send-Button"
                  whileHover={{ scale: 1.2 }}
                  whileTap={{ scale: 0.9 }}
                />
              ) : null}
            </div>
          </div>
          <div className="bottom-info">
            <p>
              {" "}
              AstraAI may display inaccurate info, including about people, so
              double-check its responses.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Main;
