from flask import Flask, render_template,request,session,flash
import pandas as pd
import numpy as np
from flask_table import Table, Col
import csv
import sqlite3 as sql
import os


#building flask table for showing recommendation results
class Results(Table):
    id = Col('Id', show=False)
    title = Col('Recommendation List')

app = Flask(__name__)
app.static_folder = 'static'
#Welcome Page
@app.route('/')
def home():
   return render_template('home.html')


@app.route('/gohome')
def homepage():
    return render_template('index.html')


@app.route('/signup')
def new_user():
   return render_template('signup1.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("gendb.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("login.html")
            con.close()

@app.route('/login')
def user_login():
   return render_template("login.html")

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':
            usrname=request.form['username']
            passwd = request.form['password']

            with sql.connect("gendb.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM user where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        #session['logged_in'] = True
                        return render_template('rating.html')
                    else:
                        flash("Invalid user credentials")
                        return render_template('login.html')
#Rating Page
@app.route("/rating", methods=["GET", "POST"])
def rating():
    if request.method=="POST":
        return render_template('recommendation.html')
    return render_template('rating.html')

#Results Page
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == 'POST':
        #reading the original dataset
        '''
        movies = pd.read_csv('movies.csv')

        #separating genres for each movie
        movies = pd.concat([movies, movies.genres.str.get_dummies(sep='|')], axis=1)

        #dropping variables to have a dummy 1-0 matrix of movies and their genres
        ## IMAX is not a genre, it is a specific method of filming a movie, thus removed
        ###we do not need movieId for this project
        categories = movies.drop(['title', 'genres', 'IMAX', 'movieId'], axis=1)

        #initializing user preference list which will contain user ratings
        preferences = []

        #reading rating values given by user in the front-end
        Action = request.form.get('Action')
        Adventure = request.form.get('Adventure')
        Animation = request.form.get('Animation')
        Children = request.form.get('Children')
        Comedy = request.form.get('Comedy')
        Crime = request.form.get('Crime')
        Documentary = request.form.get('Documentary')
        Drama = request.form.get('Drama')
        Fantasy = request.form.get('Fantasy')
        FilmNoir = request.form.get('FilmNoir')
        Horror = request.form.get('Horror')
        Musical = request.form.get('Musical')
        Mystery = request.form.get('Mystery')
        Romance = request.form.get('Romance')
        SciFi = request.form.get('SciFi')
        Thriller = request.form.get('Thriller')
        War = request.form.get('War')
        Western = request.form.get('Western')

        #inserting each rating in a specific position based on the movie-genre matrix
        preferences.insert(0, int(Action))
        preferences.insert(1,int(Adventure))
        preferences.insert(2,int(Animation))
        preferences.insert(3,int(Children))
        preferences.insert(4,int(Comedy))
        preferences.insert(5,int(Crime))
        preferences.insert(6,int(Documentary))
        preferences.insert(7,int(Drama))
        preferences.insert(8,int(Fantasy))
        preferences.insert(9,int(FilmNoir))
        preferences.insert(10,int(Horror))
        preferences.insert(11,int(Musical))
        preferences.insert(12,int(Mystery))
        preferences.insert(13,int(Romance))
        preferences.insert(14,int(SciFi))
        preferences.insert(15,int(War))
        preferences.insert(16,int(Thriller))
        preferences.insert(17,int(Western))
        '''

        #from flask import Flask, render_template, request, session, flash
        #from flask import Flask, render_template, request, session, flash
        import pandas as pd
        import numpy as np
        from flask_table import Table, Col
        import csv
        import sqlite3 as sql
        import os
        trips_df = pd.read_csv('train_main.csv', usecols=['TourId', 'Place_Name'],
                               dtype={'TourId': 'int32', 'Place_Name': 'str'})
        rating_df = pd.read_csv('rating1.csv', usecols=['userId', 'TourId', 'rating'],
                                dtype={'userId': 'int32', 'TourId': 'int32', 'rating': 'float32'})
        trips_df.head()
        rating_df.head()
        df = pd.merge(rating_df, trips_df, on='TourId')
        df.head()
        combine_trip_rating = df.dropna(axis=0, subset=['Place_Name'])
        trip_ratingCount = (combine_trip_rating.
                            groupby(by=['Place_Name'])['rating'].
                            count().
                            reset_index().
                            rename(columns={'rating': 'totalRatingCount'})
                            [['Place_Name', 'totalRatingCount']]
                            )
        trip_ratingCount.head()
        rating_with_totalRatingCount = combine_trip_rating.merge(trip_ratingCount, left_on='Place_Name',
                                                                 right_on='Place_Name',
                                                                 how='left')
        rating_with_totalRatingCount.head()
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        print(trip_ratingCount['totalRatingCount'].describe())
        popularity_threshold = 50
        rating_popular_trip = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
        rating_popular_trip.head()
        rating_popular_trip.shape
        trip_features_df = rating_popular_trip.pivot_table(index='Place_Name', columns='TourId',
                                                           values='rating').fillna(0)
        trip_features_df.head()

        from scipy.sparse import csr_matrix

        trip_features_df_matrix = csr_matrix(trip_features_df.values)

        from sklearn.neighbors import NearestNeighbors
        x = [0, 0, 0, 0]
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(trip_features_df_matrix)
        trip_features_df.shape
        query_index = np.random.choice(trip_features_df.shape[0])
        print(query_index)
        distances, indices = model_knn.kneighbors(trip_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=4)
        trip_features_df.head()
        for i in range(0, len(distances.flatten())):
            if i == 0:
                print('Recommendations for {0}:\n'.format(trip_features_df.index[query_index]))
            else:
                print('{0}: {1}, with distance of {2}:'.format(i, trip_features_df.index[indices.flatten()[i]],
                                                               distances.flatten()[i]))
                x[i] = trip_features_df.index[indices.flatten()[i]]

        print('x', x)
        prediction33 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
        prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
        prediction55 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'
        if x[1] =='Mangalore' or 'Udupi' or 'Uttara Kannada':

            prediction33 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'
        elif x[2] == 'Mysore' or 'Bangalore' or 'Ooty':
             prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
        elif x[3] == 'Mysore' or 'Udupi' or 'Bangalore':
            prediction55 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
        else:
            prediction33 = 'Beautiful city with so many tourist attraction, which attract thousands of travellers all around the world '
            prediction44 = 'Each tourist attraction in this place promises a unique and lively experience that will leave you in awe for many days to come'
            prediction55 = 'One of the cleanest cities in India, This Place is an important business center and is known for its amazing beaches, seaports and a diverse culture.'


        return render_template('resultpred.html', prediction=x[1],prediction3 = prediction33, prediction1=x[2], prediction4=prediction44, prediction2=x[3], prediction5= prediction55)

        #This funtion will get each movie score based on user's ratings through dot product


@app.route('/predictinfo')
def predictin():
   return render_template('info.html')

@app.route('/predict',methods = ['POST', 'GET'])
def predcrop():
    if request.method == 'POST':
        x = [0,0,0]
        comment = request.form['comment']
        comment1 = request.form['comment1']
        comment2 = request.form['comment2']
        x[0] = comment
        x[1] = comment1
        x[2] = comment2
        # type(data2)
        with open('b1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x[0], x[1], x[2]])
            print("CSV File is generated")

        response = 'Review Saved Successfully'
    return render_template('resultpred.html',prediction=response)

if __name__ == '__main__':
   app.run(debug = True)
   