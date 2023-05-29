from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcripts/<video_id>', methods=['GET'])
def get_transcripts(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['ko'])
    return jsonify(transcript.fetch())

if __name__ == "__main__":
    app.run(port=5000)
