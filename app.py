from flask import Flask, request, jsonify, render_template
import time, datetime, dateutil.parser
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from meraki.util import init_meraki, get_snapshot

app = Flask(__name__, static_url_path='/static')
CORS(app)

API_KEY = os.getenv("API_KEY")
ORG_ID = os.getenv("ORG_ID")

# for network Aka - Wifi 
NETWORK_ID = os.getenv("NET_ID")


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/networks/<networkId>/cameras/<camera_serial>/snapshot', methods=['GET'])
def snapshot(networkId=NETWORK_ID, camera_serial="Q2PV-2358-H3FE"):

    # get current timestamp
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    timestamp = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

    if request.data.decode() != '' and getattr(request.json, "timestamp", None):
        timestamp = request.json["timestamp"]

    snapshot_url = get_snapshot(camera_serial, timestamp, networkId)

    return jsonify({"url": snapshot_url})



@app.route('/health/')
def health(name=None):
    return "ok"


if __name__ == '__main__':
    #
    init_meraki(NETWORK_ID, MERAKI_API_KEY)

    app.run(debug=True, host='0.0.0.0', port=8088, threaded=True)
