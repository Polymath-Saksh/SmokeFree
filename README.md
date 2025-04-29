# SmokeFree

SmokeFree is a Django-based web application to help users quit smoking by tracking cravings, providing AI-powered coaching, and supporting team-based motivation.

## Features

- Log and visualize cravings (intensity, triggers, location, notes)
- Personalized dashboard with statistics and craving heatmap
- AI-powered quit coach chat (Azure OpenAI GPT-4o-mini)
- Team creation and leaderboard
- AI-generated personalized strategies and motivational quotes

## Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/Polymath-Saksh/smokefree.git
   cd SmokeFree_Collective
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   -Create a `.env` file in the root directory and add your environment variables:

   ```
   # POSTGRES Config
   POSTGRES_HOST=<POSTGRES_HOST>
   POSTGRES_PORT=5432
   POSTGRES_USER=<POSTGRES_USER>
   POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
   POSTGRES_DB=<POSTGRES_DB>

    #AZURE Config
    AZURE_ENDPOINT=<API_ENDPOINT>
    AZURE_API_KEY= <API_KEY>
    AZURE_MODEL_NAME= <MODEL_NAME>

    AZURE_SENDER_ADDRESS = <Sender_Email_Address>
    AZURE_EMAIL_CONNECTION_STRING = <Connection_String>

    GOOGLE_MAPS_API_KEY = <GOOGLEMAPS_API_KEY>
   ```

- Make sure to replace the placeholders with your actual credentials.
- For Azure OpenAI, you can find your API key and endpoint in the Azure portal.
- For Azure Communication Services, set up an email sender and connection string in the Azure portal.
- For PostgreSQL, ensure you have a running instance and the credentials are correct.
- For Google Maps, ensure you have a valid API key.

4. **Apply migrations:**

```

python manage.py migrate

```

5. **Create a superuser (optional) for admin portal access:**

```

python manage.py createsuperuser

```

6. **Run the development server:**

```

python manage.py runserver

```

## Usage

- Register and log in to start tracking cravings.
- Use the dashboard to view your stats and craving locations.
- Chat with the AI Quit Coach for support and advice.
- Join or create teams for group motivation.

## Tech Stack

- Django 5.x
- PostgreSQL
- Azure OpenAI (GPT-4o-mini)
- Google Maps API
- Bootstrap 5

## Collaborators

- [Saksham Kumar](https://github.com/PolymathSaksh)
- [Rhythm Narang](https://github.com/RhythmNarang1)
- [Vaishnavi Ahire](https://github.com/VaishnaviAhire)

## License

[MIT License](LICENSE)
