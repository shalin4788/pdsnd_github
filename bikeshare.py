import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Hello! Let\'s explore some US bikeshare data!")
    while True:
        city = input("Would you like to see data for Chicago, New York City or Washington?\n").split(": ")[0].lower()
        try:
            if city not in CITY_DATA:
                print("Sorry, {} is not a valid city. Please type again by entering either 'Chicago', 'New York City' OR 'Washington' again".format(city))
                continue
            else:
                break
        except ValueError as e:
            print("Exception occurred: {}".format(e))

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April or June?..Enter 'all' if no month filter\n").lower()
        try:
            months = ['january', 'february', 'march', 'april', 'may', 'june','all']
            if month not in months:
                print("Sorry, {} is not a valid month. Please type again by entering again".format(month))
                continue
            else:
                break
        except ValueError as e:
                print("Exception occurred: {}".format(e))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = input("Which day? Enter the response in integer. Ex: 1 = Sunday..Enter 'all' if no day filter\n")
        try:
            if day_of_week.isnumeric():
                day_of_week = int(day_of_week)
                day_of_week_dir = {1:"Sunday",2:"Monday",3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday",7:"Saturday"}
                for key, value in day_of_week_dir.items():
                    if day_of_week != key:
                        print("Sorry, {} is not a valid day. Please type again by entering either the day of week in integer ex: 1 = Sunday".format(day_of_week))
                        continue
                    else:
                        day = value
                        break
            else:
                if day_of_week == "all":
                    day = "all"
                    break
                else:
                    continue
        except ValueError as e:
                print("Exception occurred: {}".format(e))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] =df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def user_input(city, month, day):
    """
    Fetches user's Boolean input of Yes/No to determine if they want to view dataframe's raw data at any point
    Input -
    Boolean value - yes allows user to view top 5 rows of raw data from the dataframe. User can enter 'yes' to see 5 more rows incrementally till 'no' is entered
    Returns -
    Returns random 5 row entries from dataframe each time this function is called on user input
    """
    df = pd.read_csv(CITY_DATA[city])
    while True:
        try:
            inp = input("\nDo you want to view the dataframe? (Type: Yes/No)\n").lower()
            #cont = 'yes'
            if inp == 'yes':
                #if inp == 'yes':
                print(df.sample(5))
                try:
                    cont = input("\nDo you want to view the dataframe?(Type Yes/No)\n").lower()
                    if cont == 'yes':
                        print(df.sample(5))
                    elif cont == 'no':
                        print("\nOk, let's move on..\n")
                        break
                    else:
                        print("\nThis is not a valid user input..Let's move on\n")
                        break
                except ValueError as e:
                    print("Exception occurred: {}".format(e))
                    break
            elif inp == 'no':
                print("\nOk, let's move on..\n")
                break
            else:
                print("\nThis is not a valid user input..Let's move on\n")
                break
        except ValueError as e:
            print("Exception occurred: {}".format(e))
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =df['Start Time'].dt.weekday_name

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("\nWhat is the most common month for traveling?...\n")
    month_num = df['month'].mode()[0]
    month_map = {1:'January',2:'February',3:'March',4:'April',6:'June'}
    for key, value in month_map.items():
        if month_num == key:
            month_name = value.split(":")[0]
    print(month_name)

    # TO DO: display the most common day of week
    print("\nWhat is the most common day of the week?...\n")
    common_day = df['day_of_week'].mode()[0]
    print(common_day)

    # TO DO: display the most common start hour
    print("\nWhat is the most common start hour (in 24 hour format)?...\n")
    df['Start Hour'] =  df['Start Time'].dt.hour
    common_hour = df['Start Hour'].mode()[0]
    print(common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nMost commonly used start station is: {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nMost commonly used end station is: {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    #most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    #print("\nThe most commonly used start station and end station : {}, {}".format(most_common_start_end_station[0],most_common_start_end_station[1]))
    popular_station_combination = df[['Start Station', 'End Station']].groupby(['Start Station','End Station']).count().sort_values(by=['Start Station','End Station'], axis = 0).reset_index().iloc[0]
    print("\nMost frequent combination of start and end station trip is {}".format(popular_station_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #Alternative logic : total_travel_time = df.sum(axis = 0, skipna = True)['Trip Duration']
    print("\nTotal travel time: {}".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of user types:\n{}\n".format(user_types))


    # TO DO: Display counts of gender
    try:
        df.dropna(axis = 0, inplace = True)
        gender_count = df['Gender'].value_counts()
        print("\nCounts of gender:\n{}\n".format(gender_count))
    except KeyError:
        print("\nCounts of gender is: Sorry, Gender information not available for this city")


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        df.dropna(axis = 0, inplace = True)
        earliest_bday = df['Birth Year'].min(axis = 0)
        #earliest_bday = df.sort_values(by = 'Birth Year').mode()[0]
        print("\nEaliest year of birth is: {}".format(earliest_bday))
    except KeyError:
        print("\nEarliest year of birth is : Sorry, Birth year information not available for this city")

    try:
        df.dropna(axis = 0, inplace = True)
        recent_bday = df['Birth Year'].max(axis = 0)
        #recent_bday = df.sort_values(by = 'Birth Year', ascending = False).mode()[0]
        print("\nMost recent year of birth is: {}".format(recent_bday))
    except KeyError:
        print("\nMost recent year of birth is : Sorry, Birth year information not available for this city")

    try:
        df.dropna(axis = 0, inplace = True)
        common_birthday = df['Birth Year'].mode()[0]
        print("\nMost common year of birth is: {}".format(common_birthday))
    except KeyError:
        print("\nMost common birth year is : Sorry, Birth year information not available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df = user_input(city, month, day)
        time_stats(df)
        df = user_input(city, month, day)
        station_stats(df)
        df = user_input(city, month, day)
        trip_duration_stats(df)
        df = user_input(city, month, day)
        user_stats(df)
        df = user_input(city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
