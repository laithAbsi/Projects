class Movie:

    def __init__(self, movie_title, movie_year):
        self.__title = movie_title
        self.__year = movie_year
        self.__reviews = []

    def addReview(self, movie_review):
        """
        this function adds reviews to movies.
        :param movie_review:
        :return:
        """
        if not (int(movie_review) == float(movie_review)):
            return

        if 1 <= int(movie_review) <= 5:
            self.__reviews.append(int(movie_review))
        else:
            pass

    def shortReview(self):
        """
        this function makes a short review for the movies.
        :return: returns the short review format.
        """
        average_reviews = self.__calcAverage()
        return '{} ({}): {}/5'.format(self.__title, self.__year, average_reviews)

    def longReview(self):
        """
        this function creates a long review for the movies.
        :return: returns the long review format.
        """
        average_reviews = self.__calcAverage()
        counter = [0, 0, 0, 0, 0]
        for review in self.__reviews:
            counter[review - 1] += 1
        return '{} ({})\nAverage review: {}/5\n*****: {}\n**** : {}\n***  : {}\n**   : {}\n*    : {}'.format(
            self.__title, self.__year, average_reviews, counter[4], counter[3], counter[2], counter[1], counter[0])

    def getTitle(self):
        """
        this function gets the tile of the movie.
        :return: returns the title of the movie.
        """
        return self.__title

    def getYear(self):
        """
        this function gets the year that the movie came out.
        :return: returns the year the movie came out in.
        """
        return self.__year

    def __calcAverage(self):
        """
        this function calculates the average reviews of the movies.
        :return: returns a rounded review average.
        """
        if len(self.__reviews) == 0:
            return 0.0
        else:
            average_reviews = sum(self.__reviews) / len(self.__reviews)
            return round(average_reviews, 1)