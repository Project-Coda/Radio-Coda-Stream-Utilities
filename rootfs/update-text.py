import os, json
from flask import Flask, request

app = Flask(__name__)

FNAME = os.environ['NP_SOURCE']

@app.route('/', methods=['POST','GET'])
def index():
    with open(FNAME, "w") as f:
        req_data = request.get_json()
        if "now_playing" in req_data:
            if "song" in req_data["now_playing"]:
                if "text" in req_data["now_playing"]["song"]:
                    text = req_data["now_playing"]["song"]["text"]
                    f.write(text)

    return '{"success":"true"}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)