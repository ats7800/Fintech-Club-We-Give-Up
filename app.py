from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Loading The training data that I created
x_train = pd.read_csv("outputxNew.csv").to_numpy()
y_train = pd.read_csv("outputyNew.csv").to_numpy()
newY_train = y_train[::200]

num_samples = 20
num_timesteps = 200
num_features = 7

# Reshaping for input
reshaped_input_data = np.zeros((num_samples, num_timesteps, num_features))
for i in range(num_samples):
    reshaped_input_data[i] = x_train[i*num_timesteps:(i+1)*num_timesteps]

input_data = reshaped_input_data
target_data = newY_train

# Define  LSTM model
modelLSTM = Sequential()
modelLSTM.add(LSTM(64, input_shape=(200, 7)))  # 200 time steps, 7 features
modelLSTM.add(Dense(1))  # Output layer with single node for regression

modelLSTM.compile(optimizer='adam', loss='mean_squared_error')
modelLSTM.fit(input_data, target_data, epochs=2, batch_size=1)



# Loading The pretrained  FinBert Model especially trained for financial sentiment analysis:
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

modelFin = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
nlpFin = pipeline("sentiment-analysis", model=modelFin, tokenizer=tokenizer)

# Loading the massive dataset of twitter tweet history about stock companies
mergedFile = pd.read_csv("merged_file.csv")
apple = pd.read_csv("AAPL.csv")
apple['Date'] = pd.to_datetime(apple['Date'])

# Convert date column to string format with "yyyy-mm-dd" format
apple['Date'] = apple['Date'].dt.strftime('%Y-%m-%d')


# initiating flask for hosting
from flask import Flask, request, url_for, redirect, render_template, jsonify
from flask_cors import CORS
import time


app = Flask(__name__)
CORS(app)


# Pickle could not load for some technical problems hence I have decide to initiate and fit the model in file itself
# model = pickle.load(open('  LSTM-Final.pkl', 'rb'))


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/sentiment')
def sentiment():
    return render_template("index2.html")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.get_json()
    print(data)
    targetDate = data['date']
    tragetName = data['stock']

    # Taking date uptil one week before the target 
    target_date = pd.to_datetime(targetDate)
    one_week_before = target_date - timedelta(days=7)
    one_week_before = one_week_before.strftime('%Y-%m-%d')
    start_value = one_week_before
    end_value = targetDate

    # parting the data 
    resultPart = mergedFile[(mergedFile['post_date'] >= start_value) & (mergedFile['post_date'] <= end_value)]
    resultCompany = resultPart[resultPart['ticker_symbol'] == tragetName]

    # Because of the obvious limitations i decided to take highest retweetet tweets only i.e, top 200 only
    resultCompany = resultCompany.sort_values('retweet_num', ascending=False)
    resultCompany = resultCompany.head(200)

    # creating arrays of retweet, comments, likes and days before target, which will act as input for second model, that is, prediction
    tweetsOb = resultCompany['body'].values
    retweetsOb = resultCompany['retweet_num'].values
    commentOb = resultCompany['comment_num'].values
    likeOb = resultCompany['like_num'].values
    # How many days before the target Date:
    daysOb = [(datetime.strptime(targetDate, "%Y-%m-%d")-datetime.strptime(date2, "%Y-%m-%d")).days for date2 in resultCompany['post_date']]

    # Taking waeighted sum only to display on the dashboard
    retSum = sum(retweetsOb)
    retweetsObW = retweetsOb/retSum
    comSum = sum(commentOb)
    commentObW = commentOb/comSum
    likeSum = sum(likeOb)
    likeObW = likeOb/likeSum
    weights = [x + y + z for x, y, z in zip(retweetsObW, commentObW, likeObW)]
    sum(weights)

    # all 200 tweets get analysed by finBert
    sentiResult = nlpFin(tweetsOb.tolist())

    # one hot encoding the values to prepare for input in LSTM
    labels = [{"positive":0,"neutral":0,"negative":0} for i in sentiResult]
    i =0

    for obj in sentiResult:
        (labels[i])[obj['label']] = obj['score']
        i=i+1

    # also making meaning of score to display on dashboard
    score = [0 for i in sentiResult]
    i =0
    for el in sentiResult:
        if el['label'] == 'positive':
            score[i] = (el['score'])
        elif el['label'] == 'negative':
            score[i] = -(el['score'])
        i=i+1
    # weighted avg
    avgSenti = sum([weight*scoreVal for weight,scoreVal in zip(weights,score)])/3

    # creating input data for LSTM model which has 7 params - 3 hot encodes sentiments, retweets,comments,likes, days posted before the target
    xComp = [[a['positive'],a['neutral'],a['negative'],b,c,d,e] for a,b,c,d,e in zip(labels, retweetsOb, commentOb, likeOb, daysOb)]    
    x_test = [xComp]
    pred = modelLSTM.predict(x_test)
    prediction = float(pred[0][0])
    print(prediction)

    one_day_later = pd.to_datetime(target_date) + pd.DateOffset(days=1)
    five_days_earlier = pd.to_datetime(target_date) - pd.DateOffset(days=5)
    filtered_apple = apple[(apple['Date'] <= one_day_later.strftime('%Y-%m-%d')) & (apple['Date'] >= five_days_earlier.strftime('%Y-%m-%d'))]
    high = float((filtered_apple.tail(1)['Close'].values[0]))
    low = float((filtered_apple.head(1)['Open'].values[0]))
    dell = (high - low)/low


    return jsonify({"stock score":(avgSenti+1)*5 , "Pred":prediction, "Dell":dell })

        

# analysing the sentiment for displaying:
@app.route('/sentiPredict', methods=['POST', 'GET'])
def sentiPredict():
    data = request.get_json()
    print(data['senti'])
    sentence = data['senti']
    sentences = [sentence]
    pred = nlpFin(sentences)
    score = pred[0]['score']
    label = pred[0]['label']
    print(pred)
    if label=='negative':
        score = -score
    elif label == 'positive':
        score = score
    else:
        score = 0

    score = (score+1)*5
    return jsonify({"stock score": score})


@app.route('/predict', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == '__main__':
    app.run(debug=False)


