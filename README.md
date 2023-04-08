# Fintech-Club-We-Give-Up

**Problem Statement

Skills - NLP, UI/UX, WebD

You are an analyst at a HFT named ABC Capital and you have observed that nowadays quant algo is giving inaccurate predictions. Your boss has asked you to use sentiment analysis for predicting stock performance. You are required to create a NLP based market sentiment meter for NASDAQ stocks using social media posts of normal users. We recommend you to use twitter’s open API to do this.

Dataset (Use for plotting the prices) - https://drive.google.com/file/d/1Mf_SJlZVHWIokY5YD0DjaMAIr3sVNQUb/view?usp=sharing

**_Deliverables- 

Create a model for sentiment analysis
Provide a user friendly frontend (Input- Stock symbol, Output- sentiment score out of 10)

**_Brownie points- 

Check your model’s accuracy by backtesting your prediction
Compare your model’s past performance with actual stock prices movement
Additional input such as time frame can added.

Evaluation
We will take 5 stocks (Out of  and compare your model’s accuracy with our prediction for those stocks.
20% UI/UX
10% ppt
10% Architecture
30% accuracy of the model 
30% ML code 


**Approach towards solving the problem:

In this problem we first thought to access the twitter's data using twitter developer id on which we could train our model for sentiment analysis. Twitter used to provide data for tweets of past 7 days. Unfortunately due the last month's policy changes in twitter the developers would no longer be getting access of data for free. Now developers need to pay 100 USD for the same. So we had to change our approach.**

Since we did not have the recent data of twitter so we started looking for the older ones. Luckily we got one consisting of tweets related to 5 companies starting from 2015 to 2020. We did the data preprocessing then we moved on to the sentiment analaysis. We successfully did sentiment analysis on that data. Further we trained a regression model using sentiment score of tweets and their metadata like no of retweets, comments, likes, etc. We used that regression model to predict the changes in stock market. Or see the influence of tweets on stock market. 

We are simultaneously making a website on which we will deploy all of it. On that website the user can give inputs in two of the ways. First it can pick up any date and the website will do the sentiment analysis of past 7 days from that day of all the companies and will tell that on the next day whether the price will go up or down. The other way is to give a tweet as an input on the website related to any company and the website will do the sentiment analysis of that tweet.

The website will also predict the stock price for the next day.

Our idea is to use two machine learning models connected with each other. The first one is for sentiment analysis of the tweets and the second one is for to use that sentiment score and predict the stock prices.

The UI will be user friendly.



