# dive-into-python

News Articles Sentiment Analysis

## News Articles Sentiment Analysis

## Description

This project connects to various APIs (NewsAPI and RedditAPI) and takes a search parameter and returns a list of articles and links. From there, a sentiment analysis is done using the nltk module that shows the sentiment of the search parameter over time, based on the results.

## Running the Project Locally 

Clone the repository and install requirements 
```
pip freeze -r requirements.txt
```

You will also need to set up the following:
1. Set up a local postgres database called "dive"
2. Reddit API Account - see instructions [HERE](https://www.reddit.com/wiki/api/) 
3. [NewsAPI Account](https://newsapi.org/register)

## Running the Project Locally 

Once all the requirements are completed, run as follows

Start the Server
```
cd server
python3 -m main.py
```

Run the Streamlit Client
```
cd client
python3 -m streamlit run main.py
```

## Visuals

After entering a search term, click "Refresh Data". You should see both a dataframe of recent articles, as well as a chart of sentiment over time:
![example](https://gitlab.pandadoc.com/jason.scharf/dive-into-python/-/blob/master/example.png)

## Roadmap
1. Add unit tests
2. Add additional APIs
3. Move the sentiment analysis to the server
4. Worker to automate the data update process (instead of the /update-data endpoint)
5. Fix this error "raise JSONDecodeError("Extra data", s, end)
json.decoder.JSONDecodeError: Extra data: line 1 column 5 (char 4)"