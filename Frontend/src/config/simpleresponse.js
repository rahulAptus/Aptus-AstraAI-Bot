async function runChat(prompt) {
  if (prompt.toLowerCase() == "hi") {
    const response = "Hello,How are you?";
    console.log(response);
    return response;
  } else if (prompt.toLowerCase() == "can you tell how to reduce my weight?") {
    const response =
      "To reduce your weight, you can try to exercise regularly,<br/>eat a balanced diet, and stay hydrated.<br/> You can also try to lose some weight by exercising or eating healthier foods.";
    console.log(response);
    return response;
  } else {
    const response = "I am sorry, I am not able to understand your query.";
    console.log(response);
    return response;
  }
}

export default runChat;
