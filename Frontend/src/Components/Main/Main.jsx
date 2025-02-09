import { useState, useEffect, useRef } from "react";
import { assets } from "../../assets/assets";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import ChatLoader from "../Chatloader/Chatloader";
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
  const [preview, setPreview] = useState(null);
  const [hoveredUrl, setHoveredUrl] = useState(null);
  const hoverTimeout = useRef(null);

  const fetchPreview = async (url) => {
    try {
      console.log("Fetching preview for:", url);
      setHoveredUrl(url); // Store hovered URL

      const response = await axios.get(
        "http://localhost:8001/get-link-preview",
        {
          params: { url },
        }
      );

      console.log("API Response:", response.data);
      setPreview(response.data);
    } catch (error) {
      console.error("Error fetching preview:", error);
      setPreview(null);
    }
  };

  const generateThreadId = () => {
    console.log("generateThreadId :", Math.floor(Math.random() * 1000000));
    return Math.floor(Math.random() * 1000000);
  };

  useEffect(() => {
    setThreadId(generateThreadId());
  }, []);

  const handleMouseEnter = (url) => {
    hoverTimeout.current = setTimeout(() => {
      fetchPreview(url);
    }, 500); // Wait 500ms before calling API
  };

  const handleMouseLeave = () => {
    clearTimeout(hoverTimeout.current);
    setPreview(null);
  };

  const scrollToBottom = () => {
    setTimeout(() => {
      dummyRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
    if (dummyRef.current) {
      dummyRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [result, loading]); // Run when messages update

  // const sendRequest = async () => {
  //   if (prompt.trim() === "") return;
  //   setShowSources(false);
  //   setSources([]);
  //   const userMessage = prompt;
  //   setResult((prevResult) => [
  //     ...prevResult,
  //     { type: "user", text: userMessage },
  //   ]);
  //   setShowResult(true);
  //   setLoading(true);
  //   setPrompt("");

  //   setTimeout(() => scrollToBottom(), 50);

  //   try {
  //     const res = await axios.post("http://localhost:8000/prompt", {
  //       prompt: userMessage,
  //       thread_id: threadId,
  //     });
  //     setLoading(false);
  //     const data = res.data[0] || {}; // Default to an empty object if undefined
  //     let responseText = data.chatbot_response;
  //     const isHTML = /<\/?[a-z][\s\S]*>/i.test(responseText);
  //     let accumulatedText = "";

  //     if (isHTML) {
  //       setIsHTML(true);
  //       setResult((prevResult) => [
  //         ...prevResult,
  //         { type: "chatbot", text: responseText },
  //       ]);
  //     } else {
  //       setIsHTML(false);
  //       responseText.split("").forEach((char, index) => {
  //         setTimeout(() => {
  //           accumulatedText += char;
  //           setResult((prevResult) => {
  //             // Update only the last chatbot message
  //             if (
  //               prevResult.length > 0 &&
  //               prevResult[prevResult.length - 1].type === "chatbot"
  //             ) {
  //               return [
  //                 ...prevResult.slice(0, -1), // Remove the last chatbot message
  //                 { type: "chatbot", text: accumulatedText }, // Update it with new text
  //               ];
  //             } else {
  //               return [
  //                 ...prevResult,
  //                 { type: "chatbot", text: accumulatedText },
  //               ];
  //             }
  //           });
  //           if (index === responseText.length - 1) {
  //             setTimeout(() => {
  //               scrollToBottom();
  //             }, 100);
  //           }
  //           scrollToBottom();
  //         }, index * 30); // Simulate streaming effect (50ms delay per character)
  //       });
  //     }

  //     let sourceArray = data.sources || [];
  //     setShowSources(true);
  //     if (typeof sourceArray === "string") {
  //       sourceArray = sourceArray.split(",").map((source) => source.trim());
  //     } else {
  //       setShowSources(false);
  //     }
  //     setSources((prevSource) => [
  //       ...prevSource,
  //       { type: "chatbot", text: sourceArray },
  //     ]);
  //   } catch (error) {
  //     console.error("Error fetching response:", error);
  //     setShowResult(true);
  //     setLoading(false);
  //   }
  // };

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
      const res = await axios.post("http://localhost:8000/prompt", {
        prompt: userMessage,
        thread_id: threadId,
      });
      setLoading(false);
      const data = res.data[0] || {};
      let responseText = data.chatbot_response;
      let sourceArray = data.sources || [];
      const isHTML = /<\/?[a-z][\s\S]*>/i.test(responseText);

      if (isHTML) {
        setIsHTML(true);
        setResult((prevResult) => [
          ...prevResult,
          { type: "chatbot", text: responseText },
        ]);
      } else {
        setIsHTML(false);
        let accumulatedText = "";
        let chatbotMessage = { type: "chatbot", text: "" };

        setResult((prevResult) => [...prevResult, chatbotMessage]);

        setTimeout(() => {
          let charIndex = 0;

          const interval = setInterval(() => {
            if (charIndex < responseText.length) {
              accumulatedText += responseText[charIndex];
              setResult((prevResult) => {
                let updatedResults = [...prevResult];
                let lastMessage = updatedResults[updatedResults.length - 1];

                if (lastMessage && lastMessage.type === "chatbot") {
                  lastMessage.text = accumulatedText;
                } else {
                  updatedResults.push({
                    type: "chatbot",
                    text: accumulatedText,
                  });
                }

                return [...updatedResults];
              });
              charIndex++;
            } else {
              clearInterval(interval);
              setTimeout(() => scrollToBottom(), 100);
            }
          }, 30);
        }, 100);
      }

      // Convert string to array if needed
      if (typeof sourceArray === "string") {
        sourceArray = sourceArray.split(",").map((source) => source.trim());
      }

      // Ensure it's an array and contains valid sources
      if (Array.isArray(sourceArray) && sourceArray.length > 0) {
        setSources((prevSource) => [
          ...prevSource,
          ...sourceArray.map((src) => ({ type: "chatbot", text: src })),
        ]);

        // ✅ Use a callback to ensure the correct value is set
        setShowSources(() => {
          console.log(
            "sourceArray exists, setting showSources to true:",
            sourceArray
          );
          return true;
        });
      } else {
        setShowSources(false);
        console.log("No sources found, setting showSources to false.");
      }
    } catch (error) {
      console.error("Error fetching response:", error);
      setShowResult(true);
      setLoading(false);
    }
    console.log("sendRequest :", sources);
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
                  <div
                    key={index}
                    className={`chat-wrapper ${
                      entry.type === "user" ? "user-wrapper" : "chatbot-wrapper"
                    }`}
                  >
                    {/* Chatbot Image (Left) */}
                    {entry.type === "chatbot" && (
                      <img
                        src={assets.logo_buddy}
                        alt="Chatbot"
                        className="profile-img chatbot-img"
                      />
                    )}
                    {entry.type === "user" && (
                      <img
                        src={assets.user_avatar}
                        alt="User"
                        className="profile-img user-img"
                      />
                    )}

                    {/* Chat Entry */}
                    <motion.div
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
                      {entry.type === "chatbot" &&
                        showSources &&
                        sources.length > 0 && (
                          <div className="sources">
                            <h3>Sources</h3>
                            <div className="source-boxes">
                              {sources.map((source, idx) => (
                                <div
                                  key={idx}
                                  className="source_box"
                                  onMouseEnter={() =>
                                    handleMouseEnter(source.text)
                                  }
                                  onMouseLeave={handleMouseLeave}
                                >
                                  <a
                                    href={source.text}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    Aptus Data Labs
                                  </a>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      {preview && hoveredUrl && (
                        <div className="preview-box">
                          <img
                            src={preview.image}
                            alt={preview.title}
                            className="preview-image"
                          />
                          <div>
                            <h4>{preview.title}</h4>
                            <p>{preview.description}</p>
                          </div>
                        </div>
                      )}
                      {/* Message Text */}
                      <div className="message-content">
                        {isHTML ? (
                          <div
                            dangerouslySetInnerHTML={{ __html: entry.text }}
                          />
                        ) : (
                          <ReactMarkdown>{entry.text}</ReactMarkdown>
                        )}
                      </div>
                    </motion.div>
                  </div>
                ))}
            </div>
            {loading && (
              // <motion.div
              //   className="loader"
              //   initial={{ opacity: 0 }}
              //   animate={{ opacity: 1 }}
              //   transition={{ duration: 0.5 }}
              // ></motion.div>
              <ChatLoader />
            )}
            <div ref={dummyRef} style={{ marginBottom: "100px" }} />
          </>
        )}

        <motion.div
          className="main-bottom"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7 }}
          style={{
            background: "white",
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
