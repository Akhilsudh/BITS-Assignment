import feedparser
import uvicorn
from tfidf import tfidf
from fastapi import FastAPI

description = """
### Submission by Akhil S - 2021MT12054

## What is this?
These API enpoints were created as part of the Natural Language Processing assignment for BITS Pilani WILP program.

## How does it work?
These endpoints give a list of news articles when given details such as education, profession and skill set. The logic works in a such a way that it considers the provided information as documents and passed to the custom implemented tf-idf algorithm which gives us keywords out of them. These keywords help us in acquiring news from Google News RSS feeds which is returned to the user.

#### Get Details -> tf-idf -> keywords -> Google News RSS -> User result

"""

tags_metadata = [
    {
        "name": "Assignment end point",
        "description": "End point created for the purpose of the assignment."
    },
    {
        "name": "Test end points",
        "description": "End points created to test basic functions."
    }
]

app = FastAPI(
        title="Profession News Recommender App",
        description=description,
        openapi_tags=tags_metadata, 
        redoc_url=None
    )

def scrapeNews(keywords):
    result = []
    print(keywords)
    keywords.reverse()
    print(keywords)
    for i in range(len(keywords) - 1):
        feed = feedparser.parse("https://news.google.com/rss/search?q={}%20{}&hl=en-IN&gl=IN&ceid=IN:en".format(keywords[i], keywords[i+1])).entries
        print(keywords[i] + " " + keywords[i+1])
        if(len(feed) > 0):
            result.append({
                "Title": feed[0].title,
                "PublishedDate": feed[0].published,
                "URL": feed[0].link
            })
        else:
            print("No news for this pair")    
    return result

@app.get('/assignment', tags=["Assignment end point"])
def assignment(Education, Experience, Skills):
    """
     ### This end point returns relevent news based on the details provided as the API parameters
     #### The parameters are:
     - **Education:** Provide education details such as degree and university name.
     - **Experience:** Provide job experience description along with details such as company worked for and the position held.
     - **Skills:** Provide a list of professional skills.
    """
    obj = tfidf()
    keywords = obj.extractKeywords(Education, Experience, Skills, 10)
    return scrapeNews(keywords)
    # return {'result': scrapeNews(keywords)}

@app.get('/', tags=["Test end points"])
def index():
    return {'result': 'API server is working'}

@app.get('/testSKlearn', tags=["Test end points"])
def test_sklearn(deg, qual, skills):
    obj = tfidf()
    keywords = obj.skLearnTest(deg, qual, skills, 10)
    return {'result': scrapeNews(keywords)}

@app.get('/testGoogleRSS', tags=["Test end points"])
def testGoogleRSS():
    feed = feedparser.parse("https://news.google.com/rss/search?q=pizza&hl=en-IN&gl=IN&ceid=IN:en").entries
    result = []
    for entry in feed:
        result.append(entry.link)
    return {'result': result}

@app.get('/positivetest', tags=["Test end points"])
def negativeTest():
    keywords = ["pineapple", "pizza"]
    return {'result': scrapeNews(keywords)}

@app.get('/negativetest', tags=["Test end points"])
def negativeTest():
    keywords = ["asdfkljahsdfkahkhafd", "asdfkljahsdfkahkhafd"]
    return {'result': scrapeNews(keywords)}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)