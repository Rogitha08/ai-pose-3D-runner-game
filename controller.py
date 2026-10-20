from flask import Flask, request, jsonify
from flask_cors import CORS
import pyautogui
import time

app = Flask(__name__)
CORS(app)

# ------------------------------------------------
# SETTINGS
# ------------------------------------------------

CONFIDENCE_DELAY = 0.35

last_action = ""
last_action_time = 0


# ------------------------------------------------
# SEND KEY
# ------------------------------------------------

def send_key(key):

    global last_action
    global last_action_time

    now = time.time()

    # Prevent the same pose from sending
    # hundreds of keys every second
    if (
        key == last_action
        and now - last_action_time < CONFIDENCE_DELAY
    ):
        return

    pyautogui.press(key)

    last_action = key
    last_action_time = now

    print("KEY SENT:", key)


# ------------------------------------------------
# POSE API
# ------------------------------------------------

@app.route("/pose", methods=["POST"])
def pose():

    try:

        data = request.get_json()

        pose = data.get("pose", "")
        confidence = float(
            data.get("confidence", 0)
        )

        print(
            "POSE:",
            pose,
            "CONFIDENCE:",
            round(confidence * 100, 1),
            "%"
        )

        # Safety threshold
        if confidence < 0.70:

            return jsonify({
                "success": False,
                "message": "Low confidence"
            })


        pose = pose.upper().strip()


        # ----------------------------------------
        # SUBWAY SURFERS CONTROLS
        # ----------------------------------------

        if pose == "LEFT":

            send_key("left")


        elif pose == "RIGHT":

            send_key("right")


        elif pose == "JUMP":

            send_key("up")


        elif pose == "DOWN":

            send_key("down")


        elif pose == "CENTER":

            # CENTER does not need a key.
            print("CENTER - no key")


        else:

            return jsonify({
                "success": False,
                "message": "Unknown pose"
            })


        return jsonify({
            "success": True,
            "pose": pose
        })


    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ------------------------------------------------
# TEST ENDPOINT
# ------------------------------------------------

@app.route("/test", methods=["GET"])
def test():

    return jsonify({
        "status": "Pose controller is running"
    })


# ------------------------------------------------
# START SERVER
# ------------------------------------------------

if __name__ == "__main__":

    print("")
    print("===================================")
    print(" AI POSE SUBWAY SURFERS CONTROLLER")
    print("===================================")
    print("")
    print("Server running on:")
    print("http://127.0.0.1:5000")
    print("")
    print("Keep this window open.")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )