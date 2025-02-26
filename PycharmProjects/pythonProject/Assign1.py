

           # Laith Al Absi. This program determines the windchill or humidex depending on what the temperature is.

repeat = True

while repeat:

    UserInp = float(input('Enter a temperature between -50 and 50: '))

    while UserInp > 50 or UserInp < -50:       # This section takes care if the user input does not meet the requirements.

        print('That temperature is invalid.')
        UserInp = float(input('Enter a temperature between -50 and 50: '))

    if UserInp <= 0:               # This section calculates the windchill if the user temperature input is below 0.

        print('Calculating windchill.')
        windInp = float(input('Enter a wind speed between 1 and 99 km/h: '))

        while windInp < 1 or windInp > 99:

            print('That wind speed is invalid.')
            windInp = float(input('Enter a wind speed between 1 and 99 km/h: '))

        else:

            windchill = 13.12 + 0.6125 * UserInp - 11.37 * windInp ** 0.16 + 0.3965 * UserInp * windInp ** 0.16
            roundedNumber = round(windchill)


        if 0 >= windchill >= -9:      # This part informs the user of the risk of being outside at their given temperature and windspeed.
            print('The windchill is {}. Low risk.'.format(roundedNumber))

        elif -10 >= windchill >= -27:
            print('The windchill is {}. Moderate risk.'.format(roundedNumber))

        elif -28 >= windchill >= -39:
            print('The windchill is {}. High Risk. Skin can freeze in 10-30 minutes.'.format(roundedNumber))

        elif windchill <= -40:
            print('The windchill is {}. Very High Risk. Skin can freeze in under 10 minutes.'.format(roundedNumber))

        question = input('Check another weather condition (Y/N)? ')   # Asks if the user wants to check another weather condition.

        while not(question == 'Y' or question == 'y' or question == 'N' or question == 'n'):

            print('That input is invalid.')
            question = input('Check another weather condition (Y/N)? ')

        if question == 'N' or question == 'n':

            repeat = False

    else:

        if UserInp >= 20 and UserInp <= 50:         # This section calculates the humidex given the dewpoint and the temperature.

            print('Calculating humidex.')
            dewpoint = float(input('Enter the dewpoint between -50 and 50: '))

            while dewpoint < -50.0 or dewpoint > UserInp:

                print('That dew point is invalid.')
                dewpoint = float(input('Enter the dewpoint between -50 and 50: '))

            else:

                HumidexFormula = 6.11 * 2.71828 ** (5417.7530 * (1 / 273.16 - 1 / (273.16 + dewpoint)))
                GFormula = 5 / 9 * (HumidexFormula - 10)
                humidex = UserInp + GFormula
                roundedHumidex = round(humidex)


                if 20 <= humidex <= 29:
                    print('The humidex is {}. Little or no discomfort.'.format(roundedHumidex))

                if 30 <= humidex <= 39:
                    print('The humidex is {}. Some discomfort.'.format(roundedHumidex))

                if 40 <= humidex <= 44:
                    print('The humidex is {}. Great discomfort. Avoid exertion.'.format(roundedHumidex))

                if humidex >= 45:
                    print('The humidex is {}. Dangerous. Heat stroke possible.'.format(roundedHumidex))


        elif UserInp < 20 and UserInp > 0:

            print('Windchill and humidex are not a factor at this temperature.')

        question = input('Check another weather condition (Y/N)? ')     # This section asks the user if they want to check another weather condition.

        while not (question == 'Y' or question == 'y' or question == 'N' or question == 'n'):

            print('That input is invalid.')
            question = input('Check another weather condition (Y/N)? ')

        if question == 'N' or question == 'n':
            repeat = False




















