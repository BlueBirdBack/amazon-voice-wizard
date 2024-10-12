"""FastAPI-based server for text-to-speech conversion using Amazon Polly."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError


app = FastAPI()

# Create a client using the credentials and region defined in the adminuser
# section of the AWS credentials and configuration files
session = Session(region_name="us-east-1")
polly = session.client("polly")

AUDIO_FORMATS = {
    "ogg_vorbis": "audio/ogg",
    "mp3": "audio/mpeg",
    "pcm": "audio/wave; codecs=1",
}

CHUNK_SIZE = 1024


class Voice(BaseModel):
    """Represents a voice option for text-to-speech conversion."""

    Gender: str
    Id: str
    LanguageCode: str
    LanguageName: str
    Name: str


@app.get("/")
async def read_root():
    """Serve the index.html file."""
    return FileResponse("index.html")


@app.get("/voices")
async def get_voices():
    """Retrieve and return the list of available voices from Amazon Polly."""
    voices = []
    params = {}

    while True:
        try:
            response = polly.describe_voices(**params)
        except (BotoCoreError, ClientError) as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

        voices.extend(response.get("Voices", []))

        if "NextToken" in response:
            params = {"NextToken": response["NextToken"]}
        else:
            break

    return voices


@app.get("/read")
async def read_text(
    text: str = Query(...),
    voiceId: str = Query(...),
    outputFormat: str = Query(...),
    speed: str = Query("100%"),
    engine: str = Query("neural"),
):
    """Convert text to speech using Amazon Polly and stream the audio."""
    if not text or not voiceId or outputFormat not in AUDIO_FORMATS:
        raise HTTPException(status_code=400, detail="Invalid parameters")

    speed_mapping = {
        "xxx-slow": "10%",
        "xx-slow": "25%",
        "x-slow": "50%",
        "slow": "75%",
        "medium": "100%",
        "fast": "125%",
        "x-fast": "150%",
        "xx-fast": "175%",
        "xxx-fast": "200%",
    }

    ssml_speed = speed_mapping.get(speed, speed)
    ssml_text = (
        f'<speak><prosody rate="{ssml_speed}" volume="+20dB">{text}</prosody></speak>'
    )

    try:
        response = polly.synthesize_speech(
            Text=ssml_text,
            TextType="ssml",
            VoiceId=voiceId,
            OutputFormat=outputFormat,
            Engine=engine,
        )
    except (BotoCoreError, ClientError) as err:
        if "InvalidSsmlException" in str(err):
            try:
                response = polly.synthesize_speech(
                    Text=text,
                    VoiceId=voiceId,
                    OutputFormat=outputFormat,
                    Engine="neural",
                )
            except (BotoCoreError, ClientError) as fallback_err:
                raise HTTPException(
                    status_code=500, detail=str(fallback_err)
                ) from fallback_err
        else:
            raise HTTPException(status_code=500, detail=str(err)) from err

    def generate():
        stream = response.get("AudioStream")
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            yield chunk

    return StreamingResponse(generate(), media_type=AUDIO_FORMATS[outputFormat])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
