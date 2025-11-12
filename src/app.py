from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"


@app.route("/api/va", methods=["POST"])
def video_analyzer():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request body"
        })

    action = data.get("action")

    if action == "VA:FIND_SIMILAR_VIDEOS":
        print("Finding similar videos...")
        return jsonify({
            "success": True,
            "message": "",
            "data": [
                {
                    "referenceVideo": "aow05202",
                    "similarVideos": {
                        "0x0fa9ax": 0.92,
                        "ab90s9fa": 0.85,
                        "aof09sa0": 0.95
                    }
                },
                {
                    "referenceVideo": "f2fafaow",
                    "similarVideos": {
                        "jfoeia9e": 0.85,
                        "ojfs9909": 0.95
                    }
                }
            ]
        })
    elif action == "VA:ADD_VIDEO":
        video_id = data.get("videoId")
        video_file_path = data.get("videoFilePath")
        print(f"Adding video {video_id} (path={video_file_path})")
        return jsonify({
            "success": True,
            "message": "",
            "data": {
                "width": 1920,
                "height": 1080,
                "fps": 30.0,
                "duration": 120,
                "fileType": "mp4",
                "fileSize": 10485760,
                "createTime": 1698765432,
                "modifyTime": 1698765432,
                "md5": "5d41402abc4b2a76b9719d911017c592"
            }
        })
    elif action == "VA:REMOVE_VIDEO":
        video_id = data.get("videoId")
        print(f"Removing video {video_id}")
        return jsonify({
            "success": True,
            "message": ""
        })

    return jsonify({
        "success": False,
        "message": "Unknown action request"
    })


if __name__ == "__main__":
    app.run(debug=True, port=6590, host="127.0.0.1")
