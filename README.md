# CineFinder: NLP-Based Content Recommendation Engine

A machine learning-based movie recommendation system that suggests similar movies using content-based filtering. The system leverages Natural Language Processing (NLP) techniques and cosine similarity to generate recommendations, and is deployed as an interactive web application using Streamlit.

---

## 🚀 Features

* 🔍 Smart movie search with suggestions
* 🎯 Top 10 similar movie recommendations
* 🎬 Movie posters using TMDB API
* ℹ️ View details (rating, cast, director, overview)
* ⚡ Fast performance using caching
* 🎨 Clean and modern UI

---

## 🧠 Machine Learning Approach

This project uses a **content-based recommendation system**, which recommends movies based on their similarity in features.

### Steps:

1. Data preprocessing and cleaning
2. Feature engineering (combining overview, genres, cast, keywords)
3. Text vectorization using Bag of Words
4. Similarity computation using cosine similarity
5. Recommendation generation based on similarity scores

---

## 🛠️ Tech Stack

* Python
* Streamlit
* scikit-learn
* Natural Language Processing (NLP)
* Cosine Similarity
* TMDB API

---

## 📂 Project Structure

```
movie-recommender/
│
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
└── README.md
```

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Live Demo:https://movie-recommender-cinefinder.streamlit.app/

---

## 💡 Future Improvements

* Implement collaborative filtering
* Improve recommendation accuracy using TF-IDF or embeddings
* Personalized user-based recommendations
* Enhanced UI/UX

---

## 👩‍💻 Author

Developed by **Drishtii**
