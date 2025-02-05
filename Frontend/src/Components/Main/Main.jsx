// The changes done here:
// included framer-motion has to be installed.Made it more enchancing and reponsive but few changes to be done
// made its null after it and shown whole chat history
import { useState } from "react";
import "./Main.css";
import { assets } from "../../assets/assets";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
// The function can be used to create the id in frontend and sent to backend and useeffect part
// const generateThreadId = () => {
//   return crypto.randomUUID ? crypto.randomUUID() : Date.now().toString();
// };

const Main = () => {
  const [prompt, setPrompt] = useState("");
  const [showCards, setShowCards] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([]);

  // useEffect(() => {
  //   setThreadId(generateThreadId());
  // }, []);

  const sendRequest = async () => {
    if (prompt.trim() === "") return;

    try {
      setLoading(true);
      const res = await axios.post("http://localhost:8002/prompt", { prompt });  //use the port as per the backend
      setLoading(false);

      setResult((prevResult) => [
        ...prevResult,
        { type: "user", text: prompt },
        { type: "chatbot", text: res.data.chatbot_response },
      ]);
      setPrompt("");
      setShowCards(false);
    } catch (error) {
      console.error("Error fetching response:", error);
      setLoading(false);
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
        <img src={assets.astra_icon} alt="" />
      </motion.div>

      <div className="main-container">
        <motion.div 
          className="greet"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7 }}
        >
          <span>Hello, User</span>
          <p>How may I help you today?</p>
        </motion.div>

        <AnimatePresence>
          {showCards && (
            <motion.div 
              className="cards"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {[  
                { text: "Suggest beautiful places to see on an upcoming road trip", icon: assets.compass_icon },
                { text: "Briefly summarize this concept: urban planning", icon: assets.bulb_icon },
                { text: "Brainstorm team bonding activities for our work retreat", icon: assets.message_icon },
                { text: "Improve the readability of the following code", icon: assets.code_icon }
              ].map((item, index) => (
                <motion.div 
                  key={index} 
                  className="card"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setPrompt(item.text)}
                >
                  <p>{item.text}</p>
                  <img src={item.icon} alt="" />
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {!showCards && (
          <motion.div 
            className="chat-history"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            {result.map((entry, index) => (
              <motion.div
                key={index}
                className={`chat-entry ${entry.type === "user" ? "user-entry" : "chatbot-entry"}`}
                initial={{ x: entry.type === "user" ? 50 : -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <p>{entry.text}</p>
              </motion.div>
            ))}
            {loading && (
              <motion.div 
                className="loader"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <hr />
                <hr />
                <hr />
              </motion.div>
            )}
          </motion.div>
        )}

        <motion.div 
          className="main-bottom"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7 }}
        >
          <div className="search-box">
            <input
              onChange={(e) => setPrompt(e.target.value)}
              value={prompt}
              type="text"
              placeholder="Enter a prompt here"
            />
            <div>
              <img src={assets.gallery_icon} alt="" />
              <img src={assets.mic_icon} alt="" />
              {prompt && (
                <motion.img
                  onClick={sendRequest}
                  src={assets.send_icon}
                  alt=""
                  whileHover={{ scale: 1.2 }}
                  whileTap={{ scale: 0.9 }}
                />
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Main;
