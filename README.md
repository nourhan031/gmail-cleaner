# Gmail Cleaner

A Python script that cleans up your Gmail inbox by automatically deleting emails that are older than a year.

## Features

- **Search and Delete**: Searches for emails older than a year and moves them to the trash.
- **User Confirmation**: Asks for user confirmation before performing deletion.
- **Automatic Authentication**: Handles OAuth2 authentication with Gmail API.

## Prerequisites

- Gmail API credentials 

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/nourhan031/gmail-cleaner.git
    cd gmail-cleaner
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Gmail API credentials:**

    - Go to the [Google Cloud Console](https://console.developers.google.com/).
    - Enable the Gmail API.
    - Create OAuth 2.0 Client IDs credentials.
    - Download the `client_secret.json` file and place it in the project directory.

## Usage

1. **Run the script:**

    ```sh
    python main.py
    ```

2. **Authenticate:**
    - On the first run, the script will open a browser window for you to log in to your Google account and authorize the application.
    - After authentication, a `token.json` file will be created to store the access and refresh tokens.

3. **Confirm deletion:**
    - The script will ask for your confirmation before deleting the emails.
