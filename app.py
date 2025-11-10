from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "supersecret"

# ---------------------- Menu Data ----------------------
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
            "Main Menu",
            "Exit"
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
    session["menu_level"] = "main"
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "").strip().lower()

    # ---------------- Exit / Main Menu ----------------
    if user_message in ["exit", "quit", "bye"]:
        return jsonify({"response": "Thank you for chatting! 👋", "buttons": []})

    if user_message in ["main", "menu", "main menu"]:
        session["menu_level"] = "main"
        return jsonify({"response": "Please choose a category:", "buttons": menu_data["main"]})

    # ---------------- Menu Navigation ----------------
    current_level = session.get("menu_level", "main")

    if current_level != "main" and current_level in menu_data:
        submenu = menu_data[current_level]
        for btn, ans in submenu.get("answers", {}).items():
            if user_message == btn.lower():
                return jsonify({"response": ans, "buttons": submenu["buttons"]})

    for item in menu_data["main"]:
        if user_message == item.lower():
            session["menu_level"] = item
            submenu = menu_data[item]
            return jsonify({
                "response": f"Here are details for {item}:",
                "buttons": submenu["buttons"]
            })

    # Default fallback
    return jsonify({
        "response": "I didn’t get that 🤔 Try choosing an option below ⬇️",
        "buttons": menu_data["main"]
    })


@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    session.clear()
    session["menu_level"] = "main"
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
