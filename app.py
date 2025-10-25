from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "supersecret"


menu_data = {
    "main": [
        "About UJustBe",
        "Enrollment & Activation",
        "Contribution & Recognition",
        "Referrals & Business Growth",
        "Meetings & Events",
        "Culture & Values",
        "Support & Contact",
        "Exit"
    ],

    "About UJustBe": {
        "buttons": [
            "What is UJustBe?",
            "Who can join UJustBe?",
            "What is an Orbiter?",
            "CosmOrbiters & MentOrbiters",
            "Main Menu"
        ],
        "answers": {
            "What is UJustBe?": "UJustBe is a collaborative ecosystem where individuals and businesses (Orbiters) share knowledge, referrals, and opportunities to grow together. 🪐",
            "Who can join UJustBe?": "Anyone who believes in authentic connections and mutual contribution — professionals, entrepreneurs, and organizations.",
            "What is an Orbiter?": "Orbiters are active members of the UJustBe Universe who contribute through referrals, sharing knowledge, and engaging in community activities.",
            "CosmOrbiters & MentOrbiters": "CosmOrbiters are listed businesses that receive referrals.\nMentOrbiters are senior contributors who mentor and support others."
        }
    },

    "Enrollment & Activation": {
        "buttons": [
            "How can I become an Orbiter?",
            "UJustBe Business Cycle",
            "What happens after enrollment?",
            "Enrollment vs Activation",
            "Main Menu"
        ],
        "answers": {
            "How can I become an Orbiter?": "Start by filling the UJustBe Enrollment Form. Once assessed & approved, you move to activation and begin contributing!",
            "UJustBe Business Cycle": "There are 10 stages:\nProspect Identification → Prospect Assessment → Experience Center → Pre-Orbiter Assessment → Enrollment → Activation → Business Listing → Acceleration → CCAO → Quantum Leap.",
            "What happens after enrollment?": "After enrollment, complete activation steps like profile setup, attending Monthly Meeting, and contributing referrals.",
            "Enrollment vs Activation": "Enrollment = Decision to join.\nActivation = When you start contributing and participating."
        }
    },

    "Contribution & Recognition": {
        "buttons": [
            "What are CC Points?",
            "How do I earn CC Points?",
            "Types of Recognition",
            "Main Menu"
        ],
        "answers": {
            "What are CC Points?": "CC Points are awarded for contributions like referrals, meetings, mentoring, and community engagement.",
            "How do I earn CC Points?": "Participate in meetings, share referrals, mentor others, and contribute ideas to earn recognition.",
            "Types of Recognition": "⭐ Contributor of the Week\n🔥 Most Active Contributing Orbiter\n🪐 MentOrbiter with Most Connects\n💎 Top Contributor in Popular Areas"
        }
    },

    "Referrals & Business Growth": {
        "buttons": [
            "How do referrals work?",
            "Can I list my business?",
            "Benefits of CosmOrbiter",
            "Main Menu"
        ],
        "answers": {
            "How do referrals work?": "Orbiters share authentic referrals with each other, building trusted business opportunities within the community.",
            "Can I list my business?": "Yes! After activation, list your business as a CosmOrbiter for visibility and inbound referrals.",
            "Benefits of CosmOrbiter": "✅ Business visibility\n✅ Referral opportunities\n✅ Event participation\n✅ Recognition as a top CosmOrbiter"
        }
    },

    "Meetings & Events": {
        "buttons": [
            "What are Monthly Meetings?",
            "How to attend Monthly Meetings?",
            "What is an E2A Session?",
            "Main Menu"
        ],
        "answers": {
            "What are Monthly Meetings?": "Monthly Meetings include updates, recognition, business presentations, and education sessions.",
            "How to attend Monthly Meetings?": "Invites are shared via WhatsApp or Email. Attendance is marked through HRMS or meeting link.",
            "What is an E2A Session?": "E2A (Empower to Act) sessions are awareness programs focusing on health, wealth, and wellbeing."
        }
    },

    "Culture & Values": {
        "buttons": [
            "Core Value",
            "Other Values",
            "Culture Philosophy",
            "Main Menu"
        ],
        "answers": {
            "Core Value": "Adaptive 💫 — The foundation of our culture.",
            "Other Values": "Caring, Fairness, Responsible, Integrity, Authentic, Selfless, Trust, Openness, Communication, Inclusive, Bold.",
            "Culture Philosophy": "We want a world of happy faces 😊 where Orbiters contribute, connect, and grow together meaningfully."
        }
    },

    "Support & Contact": {
        "buttons": [
            "Contact Support",
            "Share an Idea",
            "Recover Login Details",
            "Main Menu"
        ],
        "answers": {
            "Contact Support": "📞 8928660399 / 9326062258\n📧 support@ujustbe.com",
            "Share an Idea": "Share ideas with your MentOrbiter or use the 'Share Your Contribution' section.",
            "Recover Login Details": "Use HRMS 'Forgot Password' or contact Support Team for help."
        }
    }
}



# ---------------------- Routes ----------------------
@app.route("/")
def home():
    session.clear()
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    search_text = user_message.lower()

    # Initialize session
    if "menu_level" not in session:
        session["menu_level"] = "main"

    # Exit → Ask for rating
    if search_text in ["exit", "quit", "bye"]:
        session["menu_level"] = "main"
        session["awaiting_rating"] = True
        return jsonify({
            "response": "👋 Thanks for chatting with UJBot! Please rate your experience (1–5 stars).",
            "buttons": []
        })

    # Rating flow
    if session.get("awaiting_rating") and user_message in ["1","2","3","4","5"]:
        session.pop("awaiting_rating")
        if int(user_message) < 3:
            session["awaiting_feedback"] = True
            return jsonify({"response": "⭐ You rated less than 3 stars. Could you please give us your feedback?", "buttons":[]})
        return jsonify({"response": f"⭐ Thank you for rating us {user_message} stars!", "buttons":[]})

    # Feedback flow
    if session.get("awaiting_feedback"):
        session.pop("awaiting_feedback")
        return jsonify({"response": "🙏 Thank you for your feedback! We'll work to improve.", "buttons":[]})

    # Main Menu
    if search_text in ["main", "menu", "main menu"]:
        session["menu_level"] = "main"
        return jsonify({
            "response": "🌠 Hello there! Welcome back to the UJustBe Universe. Please choose an option:",
            "buttons": menu_data["main"]
        })

    current_level = session.get("menu_level", "main")

    if current_level != "main":
        submenu = menu_data.get(current_level, {})
        for btn, ans in submenu.get("answers", {}).items():
            
            if search_text in btn.lower() or search_text in ans.lower():
                return jsonify({
                    "response": ans,
                    "buttons": submenu["buttons"]
                })

    # 2️⃣ Check top-level menu selection
    for item in menu_data["main"]:
        if search_text in item.lower():
            session["menu_level"] = item
            return jsonify({
                "response": f"Here are the options for {item}:",
                "buttons": menu_data[item]["buttons"]
            })

    if current_level == "main":
        return jsonify({
            "response": "🤔 I didn’t quite get that. Type 'Main Menu' to see options.",
            "buttons": []
        })

   
    submenu = menu_data.get(current_level, {})
    return jsonify({
        "response": "🤔 I didn’t quite get that. Please choose one of the options below or type a keyword:",
        "buttons": submenu.get("buttons", [])
    })


    # Handle submenu question match
    if current_level != "main":
        submenu = menu_data.get(current_level, {})
        if user_message in submenu.get("answers", {}):
            return jsonify({"response": submenu["answers"][user_message], "buttons": submenu["buttons"]})

    # Handle top-level menu selection
    if user_message in menu_data:
        session["menu_level"] = user_message
        return jsonify({
            "response": f"Here are the options for {user_message}:",
            "buttons": menu_data[user_message]["buttons"]
        })
        # ✅ Keyword search for main and submenu options
    search_text = user_message.lower()

    # Search in main menu items
    for item in menu_data["main"]:
        if search_text in item.lower():
            session["menu_level"] = item
            return jsonify({
                "response": f"Here are the options for {item}:",
                "buttons": menu_data[item]["buttons"]
            })

    # Search inside submenu button labels
    if current_level != "main":
        submenu = menu_data.get(current_level, {})
        for btn in submenu.get("buttons", []):
            if search_text in btn.lower():
                # If match found & answer exists → show answer
                if btn in submenu.get("answers", {}):
                    return jsonify({
                        "response": submenu["answers"][btn],
                        "buttons": submenu["buttons"]
                    })


    

# ✅ FINAL FALLBACK — If nothing matched above
        return jsonify({
    "response": (
        "Hmm… I’m not sure I understood that yet 🤔\n\n"
        "Would you like to go back to the main menu or connect with the Support Team?\n\n"
        "🔙 Back to Main Menu\n"
        "📞 Contact Support"
    ),
    "buttons": ["Main Menu", "Contact Support"]
})


if __name__ == "__main__":
    app.run(debug=True)
