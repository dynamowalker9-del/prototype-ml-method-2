from flask import Flask, request, jsonify, render_template
from utils.predict import predict_intent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    user_input = request.json.get("text", "")
    intent = predict_intent(user_input)

    if intent == "quiz":
        topic = ""
        if "math" in user_input.lower():
            topic = "math"
        elif "science" in user_input.lower():
            topic = "science"
        elif "python" in user_input.lower():
            topic = "python"
        else:
            topic = "general"

        quiz_bank = {
            "math": [
                {"question": "What is 5 × 6?", "options": ["11", "30", "56", "25"], "answer": "30"},
                {"question": "What is square root of 16?", "options": ["2", "4", "8", "6"], "answer": "4"},
                {"question": "Simplify:15 + (8-3)", "options": ["22", "14", "20", "36"], "answer": "20"},
                {"question": "Find the value of x if:2x=24", "options": ["12", "14", "28", "16"], "answer": "12"},
                {"question": "Find the square of side having side 6 cm", "options": ["26cm", "24cm", "18cm", "26cm"], "answer": "24"},
                {"question": "What is the LCM of 4 & 6", "options": ["12", "34", "48", "26"], "answer": "12"},
                {"question": "If 10 pens cost 50,what is the cost of1 pen", "options": ["21", "5", "8", "10"], "answer": "5"},
                {"question": "Solve:3x+7=10", "options": ["-2", "-1", "8", "6"], "answer": "-1"},
                {"question": "What is 25% of 200", "options": ["50", "54", "48", "26"], "answer": "50"},
                {"question": "what is the average of 10,20,30", "options": ["24", "14", "20", "16"], "answer": "20"},
                {"question": "Convert 0.75 into fraction", "options": ["2/3", "3/4", "5/4", "5/3"], "answer": "3/4"},
                {"question": "Find the area of a circle having radius 7cm", "options": ["221", "154", "68", "96"], "answer": "154"},
                {"question": "Convert 3/4 into decimal", "options": [".75", ".04", ".03", ".1"], "answer": ".75"},
                {"question": "Simplify 2/3 + 1/6", "options": ["2/5", "3/4", "7/8", "5/6"], "answer": "5/6"},
                {"question": "Calculate 0.45 x 1.2", "options": ["2.3", "0.54", ".28", ".16"], "answer": "0.54"},
                {"question": "If a car travels 180 km in 3 hpurs,find its speed in km/hr", "options": ["20", "54", "80", "60"], "answer": "60"},
                {"question": "If a=5&b=2 calculate (a^2+b^2)", "options": ["22", "14", "19", "16"], "answer": "29"}
            ],
            "science": [
                {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars"},
                {"question": "Which gas do plants absorb?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
                {"question": "What is the maximum amount of gas in atmosphere?", "options": ["Oxygen", "Nitrogen", "Hydrogen", "Carbo Dioxide"], "answer": "Nitrogen"},
                {"question": "What is the formula for Forcce(F)?", "options": ["F=mI", "F=ma", "F=mv", "f=IR"], "answer": "F=ma"},
                {"question": "What is the unit of Force?", "options": ["N", "G", "M", "R"], "answer": "N"},
                {"question": "What is the unit of Current?", "options": ["N", "I", "M", "G"], "answer": "I"},
                {"question": "What happens to a metal when it is heated?", "options": ["Expands", "Squizes", "no  change", "evaporates"], "answer": "Expands"},
                {"question": "Name a good conductor of electricity", "options": ["copper", "wood", "rubber", "plastic"], "answer": "copper"},
                {"question": "What is the symbol of sodium?", "options": ["Na", "Mg", "Mn", "Fe"], "answer": "Na"},
                {"question": "Which metal is in liquid form at room temperature?", "options": ["Sodium", "Mercury", "Gallium", "Iron"], "answer": "Mercury"},
                {"question": "What is the basic unit of life?", "options": ["water", "food", "wind", "sun"], "answer": "sun"},
                {"question": "Which organ pumps blood in human body?", "options": ["lungs", "heart", "pancreas", "kidney"], "answer": "heart"},
                {"question": "Which vitamin is produced in human body by sunlight?", "options": ["A", "B", "C", "D"], "answer": "D"},
                {"question": "Which part of plant performs photosynthesis?", "options": ["branch", "root", "leaf", "soot"], "answer": "leaf"},
                {"question": "Which organ helps in digestion of food?", "options": ["kidney", "intestine", "heart", "blood"], "answer": "intestine"}
            ],
            "python": [
                {"question": "What does 'len()' do in Python?", "options": ["Adds numbers", "Returns length", "Sorts list", "Prints output"], "answer": "Returns length"},
                {"question": "Which symbol is used for comments?", "options": ["//", "#", "/* */", "--"], "answer": "#"},
                {"question": "Who developed python?", "options": ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Brendan Eich"], "answer": "Guido van Rossum"}
            ],
            "general": [
                {"question": "What is the capital of India?", "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"], "answer": "Delhi"},
                {"question": "Which ocean is the largest?", "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "answer": "Pacific"}
            ]
        }

        return jsonify({
            "intent": intent,
            "topic": topic,
            "quiz": quiz_bank.get(topic, quiz_bank["general"])
        })

    elif intent == "roadmap":
        return jsonify({    
            "intent": intent,
            "roadmap": [
                "Learn Python basics",
                "Understand ML concepts",
                "Build Flask apps",
                "Train and deploy models"
            ]
        })

    else:
        return jsonify({"intent": intent})

@app.route("/log_progress", methods=["POST"])
def log_progress():
    data = request.json  # e.g., {"user": "Aditya", "score": 2, "topic": "math"}
    with open("progress_log.txt", "a") as f:
        f.write(f"{data.get('user','unknown')} | {data.get('topic','unknown')} | Score: {data.get('score',0)}\n")
    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run(debug=True)