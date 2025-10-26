from flask import Flask, render_template, request, jsonify, session
import os, re

app = Flask(__name__)
app.secret_key = "supersecret"

# ---------------------- Validation Patterns ----------------------
EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^\d{10}$"
NAME_REGEX = r"^[A-Za-z ]+$"

# ---------------------- Menu Buttons & Answers ----------------------
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


@app.route("/")
def home():
    session.clear()
    session["registration_step"] = "name"  # Start registration
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # ---------------- Registration Flow ----------------
    if "registration_step" in session:
        step = session["registration_step"]

        # ✅ Name Validation
        if step == "name":
            if not re.match(NAME_REGEX, user_message):
                return jsonify({"response": "Please enter a valid name (letters only):", "buttons": []})
            session["user_name"] = user_message
            session["registration_step"] = "email"
            return jsonify({"response": "Great! Now please enter your Email ID:", "buttons": []})

        # ✅ Email Validation
        elif step == "email":
            if not re.match(EMAIL_REGEX, user_message):
                return jsonify({"response": "❌ Invalid email! Please enter a valid email address:", "buttons": []})
            session["user_email"] = user_message
            session["registration_step"] = "phone"
            return jsonify({"response": "Thanks! Finally enter your Phone Number (10 digits):", "buttons": []})

        # ✅ Phone Validation
        elif step == "phone":
            if not re.match(PHONE_REGEX, user_message):
                return jsonify({"response": "❌ Invalid phone number! Please enter 10 digits only:", "buttons": []})
            session["user_phone"] = user_message
            session.pop("registration_step")
            session["menu_level"] = "main"

            return jsonify({
                "response": f"🎉 Welcome {session['user_name']}!\nHow can I help you today?",
                "buttons": menu_data["main"]
            })

    # ---------------- Main Menu & Chat Flow ----------------
    search_text = user_message.lower()

    if search_text in ["exit", "quit", "bye"]:
        return jsonify({"response": "Thank you for chatting! 👋", "buttons": []})

    if search_text in ["main", "menu", "main menu"]:
        session["menu_level"] = "main"
        return jsonify({
            "response": "Please choose a category:",
            "buttons": menu_data["main"]
        })

    current_level = session.get("menu_level", "main")

    # Submenu answers
    if current_level != "main":
        submenu = menu_data.get(current_level, {})
        for btn, ans in submenu.get("answers", {}).items():
            if search_text in btn.lower():
                return jsonify({"response": ans, "buttons": submenu["buttons"]})

    # Top-level menu click
    for item in menu_data["main"]:
        if search_text in item.lower():
            session["menu_level"] = item
            submenu = menu_data[item]
            return jsonify({
                "response": f"Here are details for {item}:",
                "buttons": submenu["buttons"]
            })

    return jsonify({
        "response": "I didn't get that 🤔\nTry choosing an option below ⬇️",
        "buttons": menu_data["main"]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
