Aptus chatbot-bl
### python --> 3.10.15 
### User Interface Overview

In the user interface, a set of **Frequently Asked Questions (FAQs)** will be displayed by default. Additionally, users will have the following options:

- Contact the **Aptus Team**
- **Book a session**
- **Talk to AI agent**

---

Upon initiating contact with an agent, the user will be greeted with the following prompt:

> **Agent:** "Hello! To proceed, please kindly provide your name."

In the meantime, the system will load the vector store along with a **thread ID**.

Needed to include the logic to check the input limit for the user context during the chat history so that we don't get any input limit ssue - as of 10th jan 2025 - resolved using trimming


<div style="color: Green ; font-size: 1.5em; font-weight: bold;">
Scope for the Current Version BL Side (Dated 15-Jan-2025)
</div>

- **A Global Cache for FAQ's**  
- **Semantic Caching in the Current Session**  
- **Integration of MongoDB and SQLite to Store Triggers of Moderation**
