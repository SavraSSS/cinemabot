# 🎬 Cinema Rec Bot

A Telegram bot for movie and TV show recommendations using the **Kinopoisk API** and **PostgreSQL** database.

## 📌 Features

- Save a user’s favorite movie  
- Show the favorite movie on request  
- Recommend random movies  
- Pick random movies by genre  
- Add reactions (👍 👎 👀) to suggested movies  
- Display movie details: description, genres, rating, and poster  

## 📦 Tech Stack

- **Python 3.11+**  
- **aiogram v3** — modern Telegram bot framework  
- **asyncpg** — async PostgreSQL driver  
- **aiohttp** — async HTTP client for Kinopoisk API  
- **PostgreSQL** — user and movie storage  

## 🛠 Bot Commands

- `/start` — register user  
- `/set_film` — set favorite movie  
- `/favorite_film` — show favorite movie  
- `/random_film` — random movie (with genre selection)  
- `/info` — project information  

## 🖼 Example

📌 User types `/random_film` and selects genre.  

The bot responds with:  

- Movie poster  
- Title + release year  
- Kinopoisk rating  
- Genres  
- Description  

…and attaches inline buttons:  
**Will watch** | **Don’t like it** | **Already watched**  

## 🚀 Roadmap

- Add filters by year and rating  
- Implement personalized recommendations based on favorite movies  
- Store liked movies in the database  
- Add statistics visualization (most liked genres, trends, etc.)  
