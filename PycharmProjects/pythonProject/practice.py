

year_of_interest = int(input("Please enter the year that you want to calculate the personal interest rate for: "))
numb_of_cat = int(input("Please enter the number of expenditure categories: "))

total_for_lyear = 0
total_for_yearOfinterest = 0

counter = 0

while True:
    if numb_of_cat > counter:

        expenses_for_lyear = float(input("Please enter expenses for previous year: "))
        expenses_for_yearOfinterest = float(input("Please enter expenses for year of interest: "))

        total_for_lyear += expenses_for_lyear
        total_for_yearOfinterest += expenses_for_yearOfinterest

        counter += 1

    elif numb_of_cat == counter:
        break



interest_rate = ((total_for_yearOfinterest - total_for_lyear) / (total_for_yearOfinterest)) * 100

if (interest_rate < 3):
    type_of_inflation = "low"

elif (3 >= interest_rate < 5):
    type_of_inflation = "moderate"

elif (5 > interest_rate < 10):
    type_of_inflation = "high"

else:
    type_of_inflation = "hyper"


print("personal inflation rate for", year_of_interest, "is", interest_rate,"%")


print("Inflation type is: ", type_of_inflation)