# Amazon Voice Wizard

Transform text into lifelike speech with Amazon Voice Wizard! This demo showcases Amazon Polly's text-to-speech capabilities using FastAPI and Vue.js. Customize voices, languages, and speech rates for an interactive audio experience.

## Setup

### Environment Variables

To use this project, you need to set up your AWS credentials. Follow these steps:

1. Copy the `.env.example` file to a new file named `.env`:
    ```
    cp .env.example .env
    ```

2. Open the `.env` file and edit your AWS credentials:
    ```
    AWS_ACCESS_KEY_ID=your_access_key_here
    AWS_SECRET_ACCESS_KEY=your_secret_key_here
    ```
    Replace `your_access_key_here` and `your_secret_key_here` with your actual AWS credentials.

3. Make sure to keep your `.env` file secure and never commit it to version control.

For more information on obtaining AWS credentials, visit the [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).

## Running the Application

1. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

2. Run the application using Uvicorn:
    ```
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```
    This command does the following:
    - `app:app` tells Uvicorn to use the `app` variable in the `app.py` file
    - `--host 0.0.0.0` makes the server accessible from other devices on the network
    - `--port 8000` sets the port to 8000
    - `--reload` enables auto-reloading when code changes are detected

    The application will start running and be accessible at `http://localhost:8000`.

## Using the Application

1. Ensure the FastAPI backend server is running as described above.

2. Open your web browser and go to `http://localhost:8000` or `http://<your-ip-address>:8000` if accessing from another device on the network.

3. You'll see a user interface with options to:
    - Select the language
    - Choose the gender of the voice
    - Pick a specific voice
    - Set the speech rate
    - Enter the text you want to convert to speech
    ![screenshot](./assets/chrome_R5PzILDuSw.png)

4. After entering your desired text and selecting your preferences, click the "Generate Speech" button.

5. Once the audio is generated, you can play it using the audio player at the bottom of the page or download it for later use.

## Technical Details

This application uses:
- FastAPI for the backend server
- Vue.js for the frontend user interface
- Amazon Polly for text-to-speech conversion

The FastAPI server handles requests for available voices and text-to-speech conversion, while the Vue.js frontend provides an interactive user interface for customizing and generating speech.