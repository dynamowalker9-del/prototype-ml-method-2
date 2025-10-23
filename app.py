from flask import Flask, request, jsonify, render_template
from utils.predict import predict_intent
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    user_input = data.get("text", "")
    count = int(data.get("count", 2))  # default to 2 if not provided

    intent = predict_intent(user_input)

    if intent == "quiz":
        topic = ""
        if "math" in user_input.lower():
            topic = "math"
            if intent == "advance" in user_input.lower():
                topic = "advancem"    
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
                {"question": "Solve:3x+7=10", "options": ["-2", "1", "8", "6"], "answer": "1"},
                {"question": "What is 25% of 200", "options": ["50", "54", "48", "26"], "answer": "50"},
                {"question": "what is the average of 10,20,30", "options": ["24", "14", "20", "16"], "answer": "20"},
                {"question": "Convert 0.75 into fraction", "options": ["2/3", "3/4", "5/4", "5/3"], "answer": "3/4"},
                {"question": "Find the area of a circle having radius 7cm", "options": ["221", "154", "68", "96"], "answer": "154"},
                {"question": "Convert 3/4 into decimal", "options": [".75", ".04", ".03", ".1"], "answer": ".75"},
                {"question": "Simplify 2/3 + 1/6", "options": ["2/5", "3/4", "7/8", "5/6"], "answer": "5/6"},
                {"question": "Calculate 0.45 x 1.2", "options": ["2.3", "0.54", ".28", ".16"], "answer": "0.54"},
                {"question": "If a car travels 180 km in 3 hpurs,find its speed in km/hr", "options": ["20", "54", "80", "60"], "answer": "60"},
                {"question": "If a=5&b=2 calculate (a^2+b^2)", "options": ["22", "14", "29", "16"], "answer": "29"}
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
                {"question": "Who developed python?", "options": ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Brendan Eich"], "answer": "Guido van Rossum"},
                {"question": "What is the output of 'print(2**3)'?", "options": ["6", "8", "9", "5"], "answer": "8"},
                {"question": "Which data type is immutable?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
                {"question": "How to create a function in Python?", "options": ["func myFunc():", "def myFunc():", "function myFunc():", "create myFunc():"], "answer": "def myFunc():"},
                {"question": "What is the correct file extension for Python files?", "options": [".pyth", ".pt", ".pyt", ".py"], "answer": ".py"},
                {"question": "Which keyword is used for exception handling?", "options": ["try", "catch", "except", "final"], "answer": "try"},
                {"question": "How to insert COMMENTS in Python code?", "options": ["// This is a comment", "# This is a comment", "<!-- This is a comment -->", "/* This is a comment */"], "answer": "# This is a comment"},
                {"question": "Which method can be used to remove whitespace from the beginning or end of a string?", "options": ["strip()", "trim()", "len()", "remove()"], "answer": "strip()"},
                {"question": "What is the output of: print(type([]) is list)", "options": ["True", "False"], "answer": "True"},
                {"question": "What is the result of 5 // 2 in Python?", "options": ["2.5", "2", "3", "2.0"], "answer": "2"},
                {"question": "What does this list comprehension produce: [x*x for x in range(5)]?", "options": ["[1,4,9,16,25]", "[0,1,4,9,16]", "[0,2,4,6,8]", "[5,10,15,20,25]"], "answer": "[0,1,4,9,16]"},
                {"question": "What is the output of: a = \"5\"; b = 2; print(a * b)", "options": ["\"10\"", "\"55\"", "Error", "10"], "answer": "\"55\""},
                {"question": "Which of the following is used to make a deep copy of objects?", "options": ["copy.copy", "copy.deepcopy", "assign", "shallow_copy"], "answer": "copy.deepcopy"},
                {"question": "What does next(generator) do?", "options": ["Starts the generator", "Returns the next value or raises StopIteration", "Resets the generator", "Deletes the generator"], "answer": "Returns the next value or raises StopIteration"},
                {"question": "What is the difference between '==' and 'is'?", "options": ["'==' checks identity and 'is' checks equality", "'==' checks equality and 'is' checks identity", "Both are identical", "Neither compares values"], "answer": "'==' checks equality and 'is' checks identity"},
                {"question": "What is the output of: nums = [1,2,3,4]; print(sum(nums, 10))", "options": ["10", "20", "11", "Error"], "answer": "20"},
                {"question": "What is the output of: lst = [1,2,3]; print(lst[1:])", "options": ["[1,2]", "[2,3]", "[1,2,3]", "Error"], "answer": "[2,3]"},
                {"question": "Which module provides regular expression support in Python?", "options": ["regex", "re", "regexp", "re2"], "answer": "re"},
                {"question": "What does a generator expression return?", "options": ["list", "tuple", "iterator", "dictionary"], "answer": "iterator"},
                {"question": "Which statement ensures a file is automatically closed when done?", "options": ["try/finally", "with", "open_close", "close"], "answer": "with"}
                ],
            "general": [
                {"question": "What is the capital of India?", "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"], "answer": "Delhi"},
                {"question": "Which ocean is the largest?", "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "answer": "Pacific"},
                {"question": "Which sport primarily uses a racket, shuttlecock, and net?", "options": ["Squash", "Tennis", " Badminton", " Table tennis"], "answer": " Badminton"},
                {"question": "Who painted the Mona Lisa?", "options": ["Vincent van Gogh", " Pablo Picasso", "Leonardo da Vinci", " Claude Monet"], "answer": "Leonardo da Vinci"},
                {"question": "What is H2O commonly known as?", "options": ["Oxygen", "Hydrogen", "Water", "Carbon Dioxide"], "answer": "Water"},
                {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue Whale", "Giraffe", "Great White Shark"], "answer": "Blue Whale"},
                {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars"},
                {"question": "What is the hardest natural substance on Earth?", "options": ["Gold", "Iron", "Diamond", "Silver"], "answer": "Diamond"},
                {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"], "answer": "William Shakespeare"},
                {"question": "What is the boiling point of water?", "options": ["90°C", "100°C", "110°C", "120°C"], "answer": "100°C"}
            ],
            "advancem": [
                {"question": "Calculate the limit: lim(x→∞)(√(x²+3x)-x)", "options": ["3/2", "0", "1.5", "∞"], "answer": "3/2"},
                {"question": "Find all values of z that satisfy: z⁴+16=0", "options": ["2(1±i), -2(1±i)", "2(±1±i)", "±2(1±i)", "±2(±1±i)"], "answer": "±2(1±i)"},
                {"question": "Find eigenvalues of matrix A=[2,-1,0;-1,2,-1;0,-1,2]", "options": ["2,3,4", "0,2,4", "2±√2,2", "4,2,0"], "answer": "2±√2,2"},
                {"question": "Prove: n⁵-n is divisible by 30 for any positive integer n", "options": ["Use induction", "Use divisibility rules", "Use modular arithmetic", "All of these"], "answer": "Use modular arithmetic"},
                {"question": "Probability of rolling a die three times before getting a 6", "options": ["25/216", "125/216", "91/216", "5/6"], "answer": "125/216"},
                {"question": "Line integral ∮(x²dy-y²dx) where C is circle x²+y²=1", "options": ["0", "π", "2π", "-2π"], "answer": "2π"},
                {"question": "Sum of infinite series: Σ(n/2ⁿ) from n=1 to ∞", "options": ["1", "2", "4", "∞"], "answer": "2"},
                {"question": "Find min value of f(x,y)=x²+y² subject to x³+y³=1", "options": ["2/3", "1", "3/2", "2"], "answer": "2/3"},
                {"question": "Evaluate surface integral ∬zds where S is x+y+z=1 in first octant", "options": ["1/6", "1/3", "1/2", "1"], "answer": "1/6"}
            ],
        }

        pool = quiz_bank.get(topic, quiz_bank["general"])
        count = min(count, len(pool))  # avoid overflow
        selected_questions = random.sample(pool, count)

        return jsonify({
            "intent": intent,
            "topic": topic,
            "quiz": selected_questions
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
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO progress (user, topic, score, timestamp)
        VALUES (?, ?, ?, ?)
    """, (data["user"], data["topic"], data["score"], timestamp))
    conn.commit()
    conn.close()
    return jsonify({"status": "logged"})

@app.route("/dashboard")
def dashboard():
    print("Accessing dashboard")
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT topic, COUNT(*) as attempts, AVG(score) as avg_score
        FROM progress
        GROUP BY topic
    """)
    rows = cursor.fetchall()
    conn.close()

    data = [{"topic": r[0], "attempts": r[1], "avg_score": round(r[2], 2)} for r in rows]
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
