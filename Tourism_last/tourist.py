'''
import pandas as pd

# read data
reviews_df = pd.read_csv("train_main.csv")
# append the positive and negative text reviews
reviews_df["review"] = reviews_df["Negative_Review"] + reviews_df["Positive_Review"]
# create the label
reviews_df["is_bad_review"] = reviews_df["Reviewer_Score"].apply(lambda x: 1 if x < 5 else 0)
# select only relevant columns
reviews_df = reviews_df[["review", "is_bad_review"]]
reviews_df.head()
print('reviews_df',reviews_df)
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
#matplotlib inline
data = pd.read_csv("train_main.csv")
data.head()
for i in data.columns:
    print(i)
len(data)
len(data.Place_Name.unique())
data_plot = data[["Place_Name","Average_Score"]].drop_duplicates()
data_plot_avg = data_plot.plot.hist()
plt.show()

max_rating = data.Average_Score.max()
max_rating
min_rating = data.Average_Score.min()
min_rating
mean_rating = data.Average_Score.mean()
print('The mean rating is '+ str(mean_rating))
nltk.download("punkt")
pos_reviews = data.Positive_Review
neg_reviews = data.Negative_Review
print(type(pos_reviews))
pos_reviews_words = nltk.word_tokenize(pos_reviews[1]) #word_tokenize only works for text file, not whole series
#len(pos_reviews[0])
#print(pos_reviews[1])
print(pos_reviews_words) #tokenize and print the second review (the first was too short)
print(type(pos_reviews[:5]))
len(pos_reviews)

pos_reviews_wordslist = []
#for i in range(5):
for i in range(1107): #get error if put len+1 here, needed to switch from pos_reviews[1] to .iloc[1]
    pos_reviews_wordslist.append(nltk.word_tokenize(pos_reviews.iloc[i])) #tokenize text in each positive review
print(pos_reviews_wordslist[:5])
len(pos_reviews_wordslist)
type(pos_reviews_wordslist)
neg_reviews_wordslist = [] #repeat tokenization for negative reviews
#for i in range(5):
for i in range(1107): #get error if put len+1 here, needed to switch from pos_reviews[1] to .iloc[1]
    neg_reviews_wordslist.append(nltk.word_tokenize(neg_reviews.iloc[i])) #tokenize text in each negative review as alist, append that to original list
#    return pos_reviews_wordslist as a nested list with each review as a sublist
print(neg_reviews_wordslist[-5:])