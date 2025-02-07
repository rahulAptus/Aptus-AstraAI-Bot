import os
import webbrowser

def schedule_meeting(user_query: str):
    """
    This function opens a specific HTML page in the default web browser for scheduling meeting.
    
    Parameters:
        user_query (str): The query string from the user.
    """
    print("[INFO]: User Query:", user_query)
    print(f"[INFO]: --> Tool call --> schedule_meeting running...")

    html_file_path = os.path.abspath(".index.html")  # 
    
    # Opening the HTML file in the default web browser
    webbrowser.open(f"file://{html_file_path}")
    print("[INFO]: HTML page opened successfully.")


if __name__ == "__main__":
    query = "I want to fix a meeting with your company to see the demo."
    schedule_meeting(query)
