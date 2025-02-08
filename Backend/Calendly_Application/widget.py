book_appointment_widget ='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fix Appointment Widget</title>
    <style>
        .appointment-widget {
            border-radius: 12px;
            background-color: #e0f7fa; /* Light cyan background */
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            max-width: 350px;
            text-align: center; /* Center align text */
            font-size: 0.95em;
            margin: 20px auto; /* Centering the widget */
        }

        h2 {
            font-size: 1.6em;
            color: #00796b; /* Dark teal */
            margin-bottom: 15px;
            font-weight: bold;
        }

        p {
            margin: 10px 0;
            color: #555; /* Grey text */
        }

        #appointment-btn {
            display: inline-block;
            background-color: #00796b; /* Dark teal */
            border: 0px;
            color: #ffffff; /* White text */
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1em;
            transition: background-color 0.3s;
            margin-top: 15px;
        }

        #appointment-btn:hover {
            background-color: #0062a5; /* Darker teal on hover */
        }
    </style>
</head>
<body>

    <div class="appointment-widget">
        <h2>Book an Appointment</h2>
        <p>We value your time! Schedule a hassle-free appointment with us and let’s discuss how we can help you.</p>
        <a id="appointment-btn" href= "https://calendly.com/aptusdatalabs" target="_blank">Fix Appointment</a>
    </div>
</body>
</html>
'''