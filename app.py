from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import boto3
import io
import base64
import os

app = Flask(__name__)


@app.route('/transcripts/<video_id>', methods=['GET'])
def get_transcripts(video_id):
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    polly_client = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='ap-northeast-2'
    ).client('polly')

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['ko'])

    transcript_parts = transcript.fetch()
    transcript_data = []
    for part in transcript_parts:
        text = part['text']
        start = part['start']
        duration = part['duration']

        # Use Amazon Polly to synthesize speech
        response = polly_client.synthesize_speech(
            OutputFormat='mp3',
            Text=text,
            VoiceId='Seoyeon'
        )
        # Create an in-memory file
        audio_stream = io.BytesIO()
        audio_stream.write(response['AudioStream'].read())
        audio_stream.seek(0)

        # This will give you the byte data
        audio_bytes = audio_stream.getvalue()

        # If you need base64 representation
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        transcript_data.append({
            'text': text,
            'start': start,
            'duration': duration,
            'audio': audio_base64
        })

    return jsonify({
        'transcripts': transcript_data
    })


if __name__ == "__main__":
    app.run(port=5000)
