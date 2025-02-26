# Laith Al Absi. This program manages a database for movie reviews.
# It adds movies to the system, and reviews are added for that movie.
# Then summaries of all reviews for that movie can be displayed.

from moviedb import MovieDataBase

COMMAND = 0
TITLE = 1
YEAR = 2
REVIEW = 3

NEW_COMMAND = 'NEW'
REVIEW_COMMAND = 'REV'
SHOW_COMMAND = 'SHO'
PRINT_COMMAND = 'PRI'


def readFile(input):

    our_data_base = MovieDataBase()

    with open(input, 'r') as fh:
        for line in fh:
            data = line.strip().split('-')

            command = data[COMMAND]

            if command == NEW_COMMAND:
                title = data[TITLE]
                year = data[YEAR]

                # CODE FOR PROCESSING NEW COMMANDS
                try:
                    our_data_base.addMovie(movie_title=title, movie_year=year)
                except KeyError:
                    pass

            elif command == REVIEW_COMMAND:
                title = data[TITLE]
                year = data[YEAR]
                review = data[REVIEW]

                # CODE FOR PROCESSING REV COMMANDS
                the_movie = our_data_base.findMovie(title=title, year=year)
                if the_movie is not None:
                    the_movie.addReview(movie_review=review)

            elif command == SHOW_COMMAND:
                # CODE FOR PROCESSING SHO COMMANDS
                our_data_base.showAll()
            elif command == PRINT_COMMAND:
                title = data[TITLE]
                year = data[YEAR]
                # CODE FOR PROCESSING PRI COMMANDS
                the_movie = our_data_base.findMovie(title=title, year=year)
                if the_movie is not None:
                    print(the_movie.longReview())

def Main():

    user_input = input('Enter the name of the file: ')
    readFile(user_input)

Main()
