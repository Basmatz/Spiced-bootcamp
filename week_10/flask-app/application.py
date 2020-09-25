from flask import Flask, render_template, request
#import recommender as rec #import all objects from recommender.py
import functions as fun
#pip install Flask

app = Flask(__name__) #tell Flask to make THIS script the center of the application


@app.route('/index') #whenever user visits HOSTNAME:PORT/index, this function is triggered
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations') #python decorater modifies the function that is defined on the next line.
def recommender():
    user_input_dict = dict(request.args)

    user_films = {k:v for (k,v) in user_input_dict.items() if 'movie' in k}
    user_ratings = {k:v for (k,v) in user_input_dict.items() if 'rating' in k}

    films =  user_films.values()
    ratings =  user_ratings.values()

    films_cleaned = fun.fuzzy_select(films)

    print('*** films ***')
    print(films)
    print('*** films_cleaned ***')
    print(films_cleaned)
    print('*** ratings ***')
    print(ratings)

    user_films_dict = dict(zip(films_cleaned, ratings))

    print('*** user_films_dict ***')
    print(user_films_dict)

    result = fun.NMF_recommender(user_films_dict)
    return render_template('recommendations.html', movies=result)





if __name__ == '__main__':
    #whatever occurs after this line is executed when we run "python application.py"
    #however, whatever occurs after this line is NOT executed when we IMPORT application.py

    app.run(debug=True) #this will start an infinite process, i.e. serving our web page.
    #debug mode displays backend errors to the browser
    #(good for development but bad idea for production).
    #Also automatically restarts server upon changes to code.
