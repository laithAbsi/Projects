from movie import Movie

class MovieDataBase:

    def __init__(self):
        self.__movies = []

    def search_movie(self, title, year):
        """
        this function makes sure the movie is in the database.
        :param title: title of the movie.
        :param year: year of release of the movie.
        :return: returns False if the movie is not in the database and returns True if the movie is in the database.
        """
        for movie in self.__movies:
            if movie.getTitle() == title and movie.getYear() == year:
                return True
        return False

    def addMovie(self, movie_title, movie_year):
        """
        this function adds the movie to the movie to the database if it's not in there.
        :param movie_title: title of the movie.
        :param movie_year: year of release of the movie.
        :return: does not return anything.
        """
        if self.search_movie(movie_title, movie_year) == False:
            self.__movies.append(Movie(movie_title, movie_year))
        else:
            raise KeyError('movie already exists')

    def findMovie(self, title, year):
        """
        this function gets a movies from the database.
        :param title: title of the movie.
        :param year: year of release of the movie.
        :return: returns None.
        """
        for movie in self.__movies:
            if movie.getTitle() == title and movie.getYear() == year:
                return movie
        return None

    def showAll(self):
        """
        this function sorts all movies in the database by year and title. Then  print all short reviews for all movies in the database.
        :return: returns nothing.
        """
        self.__movies.sort(key=lambda x: x.getYear())
        self.__movies.sort(key=lambda x: x.getTitle())

        for movie in self.__movies:
            print(movie.shortReview())


