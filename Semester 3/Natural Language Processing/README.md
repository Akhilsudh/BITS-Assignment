# Profession News Recommender App

## This NLP assignment submission is by Akhil S - 2021MT12054

Assignment:
===========
Proposed solution will recommend real time news based on user professional profile.
Steps:
1. Enter your Educational details(Degree, University)
2. Enter your most recent experience(Organization Name, Experience description)
3. Enter your skills
4. Implement a content based recommendation system which will recommend news based on above entered data in real time. [6 marks]
5. Convert the solution in FastAPI endpoint.[4 marks]

Prerequisites:
==============
1. Make sure that the requirements mentioned in requirements.txt is installed, this can be done by running the following:

```bash
 pip install -r requirements.txt
```

2. Make sure that tfidf.py file is in the same path as the app.py file

Running the app:
================
1. After the prerequisites are met, we need to run the app.py

```bash
 python app.py
```

> NOTE: This app can take more time than usually when run for the first time since code tries to download stop words from nltk.


2. Go to http://127.0.0.1:8000/docs, the end point for the assignment is "/assignment".
3. You can try this api out by clicking "Try it out" button
4. Provide the Education, Experience and Skills and hit execute
5. This API will return a list of objects where each object has the Title, PublishedDate and URL for the news article

Screenshots and samples:
============
1. Swagger UI for API:
![image](https://user-images.githubusercontent.com/9346768/202389378-2fe0c99b-65ac-4aa2-9b30-ae09ea5e986f.png)

2. API endpoint result with sample data on UI
![image](https://user-images.githubusercontent.com/9346768/202388767-f4308099-02f9-4e64-a8b6-dd5bbf7c6c73.png)

3. Sample output from data provided to API
```json
[
  {
    "Title": "Are SaaS And Software-Defined Operating Platforms Compatible? - Forbes",
    "PublishedDate": "Wed, 16 Nov 2022 15:47:51 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMid2h0dHBzOi8vd3d3LmZvcmJlcy5jb20vc2l0ZXMvcGV0ZXJiZW5kb3JzYW11ZWwvMjAyMi8xMS8xNi9hcmUtc2Fhcy1hbmQtc29mdHdhcmUtZGVmaW5lZC1vcGVyYXRpbmctcGxhdGZvcm1zLWNvbXBhdGlibGUv0gEA?oc=5"
  },
  {
    "Title": "Spatial Leverages Years of Immersive Audio Experience Design to Develop Spatial Space Kit, a Simple, Scalable Hardware and Software Solution - Business Wire",
    "PublishedDate": "Wed, 16 Nov 2022 14:00:00 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiwwFodHRwczovL3d3dy5idXNpbmVzc3dpcmUuY29tL25ld3MvaG9tZS8yMDIyMTExNjAwNTM5My9lbi9TcGF0aWFsLUxldmVyYWdlcy1ZZWFycy1vZi1JbW1lcnNpdmUtQXVkaW8tRXhwZXJpZW5jZS1EZXNpZ24tdG8tRGV2ZWxvcC1TcGF0aWFsLVNwYWNlLUtpdC1hLVNpbXBsZS1TY2FsYWJsZS1IYXJkd2FyZS1hbmQtU29mdHdhcmUtU29sdXRpb27SAQA?oc=5"
  },
  {
    "Title": "Full-Stack Developers: Surge In Demand and The Reason Behind It - Youth Incorporated",
    "PublishedDate": "Tue, 08 Nov 2022 08:00:00 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiVmh0dHBzOi8veW91dGhpbmNtYWcuY29tL2Z1bGwtc3RhY2stZGV2ZWxvcGVycy1zdXJnZS1pbi1kZW1hbmQtYW5kLXRoZS1yZWFzb24tYmVoaW5kLWl00gFaaHR0cHM6Ly95b3V0aGluY21hZy5jb20vZnVsbC1zdGFjay1kZXZlbG9wZXJzLXN1cmdlLWluLWRlbWFuZC1hbmQtdGhlLXJlYXNvbi1iZWhpbmQtaXQvYW1w?oc=5"
  },
  {
    "Title": "Why Millennials are Crazy about Full-stack Web Developer Jobs? - Analytics Insight",
    "PublishedDate": "Fri, 28 Oct 2022 07:00:00 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiX2h0dHBzOi8vd3d3LmFuYWx5dGljc2luc2lnaHQubmV0L3doeS1taWxsZW5uaWFscy1hcmUtY3JhenktYWJvdXQtZnVsbC1zdGFjay13ZWItZGV2ZWxvcGVyLWpvYnMv0gEA?oc=5"
  },
  {
    "Title": "Top 10 Google Colab Alternatives for Machine Learning Engineers in 2023 - Analytics Insight",
    "PublishedDate": "Mon, 14 Nov 2022 10:34:44 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiaWh0dHBzOi8vd3d3LmFuYWx5dGljc2luc2lnaHQubmV0L3RvcC0xMC1nb29nbGUtY29sYWItYWx0ZXJuYXRpdmVzLWZvci1tYWNoaW5lLWxlYXJuaW5nLWVuZ2luZWVycy1pbi0yMDIzL9IBAA?oc=5"
  },
  {
    "Title": "Putting chiral perturbation theory to the test - Advanced Science News",
    "PublishedDate": "Wed, 16 Nov 2022 08:29:21 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiU2h0dHBzOi8vd3d3LmFkdmFuY2Vkc2NpZW5jZW5ld3MuY29tL3B1dHRpbmctY2hpcmFsLXBlcnR1cmJhdGlvbi10aGVvcnktdG8tdGhlLXRlc3Qv0gEA?oc=5"
  },
  {
    "Title": "IIT Kanpur Invites Applications for Two Free Online Courses on Data Science - DATAQUEST",
    "PublishedDate": "Thu, 17 Nov 2022 06:00:29 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMiZGh0dHBzOi8vd3d3LmRxaW5kaWEuY29tL2lpdC1rYW5wdXItaW52aXRlcy1hcHBsaWNhdGlvbnMtZm9yLXR3by1mcmVlLW9ubGluZS1jb3Vyc2VzLW9uLWRhdGEtc2NpZW5jZS_SAWhodHRwczovL3d3dy5kcWluZGlhLmNvbS9paXQta2FucHVyLWludml0ZXMtYXBwbGljYXRpb25zLWZvci10d28tZnJlZS1vbmxpbmUtY291cnNlcy1vbi1kYXRhLXNjaWVuY2UvYW1wLw?oc=5"
  },
  {
    "Title": "IIT Madras to offer course in advanced quantum computing - The Hindu",
    "PublishedDate": "Wed, 16 Nov 2022 10:53:00 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMieWh0dHBzOi8vd3d3LnRoZWhpbmR1LmNvbS9uZXdzL2NpdGllcy9jaGVubmFpL2lpdC1tYWRyYXMtdG8tb2ZmZXItY291cnNlLWluLWFkdmFuY2VkLXF1YW50dW0tY29tcHV0aW5nL2FydGljbGU2NjE0NDIxOS5lY2XSAQA?oc=5"
  },
  {
    "Title": "Chennai Startup’s Electric Two-Wheelers Zip Across Africa, Raise $50 Million Funding - The Better India",
    "PublishedDate": "Mon, 07 Nov 2022 08:00:00 GMT",
    "URL": "https://news.google.com/__i/rss/rd/articles/CBMifGh0dHBzOi8vd3d3LnRoZWJldHRlcmluZGlhLmNvbS8zMDIxODcvY2hlbm5haS1zdGFydHVwLWVsZWN0cmljLXZlaGljbGUtdHdvLXdoZWVsZXJzLWluLWFmcmljYS1lbGVjdHJpYy1hdXRvcy1hbmQtZS1tb2JpbGl0eS_SAQA?oc=5"
  }
]
```

---
This project can be found in https://github.com/Akhilsudh/BITS-Assignment/tree/master/Semester%203/Natural%20Language%20Processing
