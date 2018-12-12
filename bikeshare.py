import time
import pandas as pd
import numpy as np
import calendar

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
    print('\nHello! Let\'s explore some US bikeshare data!')


    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month - January, February, March, April, May, June, or All? ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All? ').lower()

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':

       df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The Most Common Month Is: {}'.format(calendar.month_name[common_month]))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The Most Common Day Is: {}'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The Most Common Hour Is: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Common Commonly Used Start Station Is: {}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Common Commonly Used End Station Is: {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Popular Route'] = df['Start Station'] + ' To ' + df['End Station']
    popular_route = df['Popular Route'].mode()[0]
    print('The Most Frequent Combination of Start Station And End Station Trip Is: {}'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (df['Trip Duration'].sum()/60)
    print('Total Travel Time: {} minutes'.format(total_travel_time))


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('Average Travel Time: {} minutes'.format(mean_travel_time))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    user_count = df.groupby(['User Type'])['User Type'].count()
    print('# Of Users By User Types:\n{}'.format(user_count))

    try:
        # TO DO: Display counts of gender
        adf = df.fillna('Not Available')
        gender_count = adf.groupby(['Gender'])['Gender'].count()
        print('\n# Of Users By Gender:\n{}'.format(gender_count))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        print('\nEarliest Year Of Birth: {}'.format(int(earliest_year_of_birth)))

        recent_year_of_birth = df['Birth Year'].max()
        print('Most Recent Year Of Birth: {}'.format(int(recent_year_of_birth)))

        common_year_of_birth = df['Birth Year'].mode()
        print('Most Common Year Of Birth: {}'.format(int(common_year_of_birth)))

    except KeyError:
        print('\nWashington Has No Data On User Gender Or User Birth Year')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def expand(df):
    start = 0
    end = 10
    data = input('Would you like to see the raw data? ').lower()

    while data == 'yes':
        print(df.iloc[start:end])
        data = input('Would you like to see 10 more rows of raw data? ').lower()
        start = end
        end += 10

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

        except (KeyError, ValueError, IndexError):
            print('\nYour input for either city or month is incorrect.')
            try_again = input('Would you like to try again? Enter yes or no.\n')
            if try_again.lower() != 'yes':
                break
            else:
                main()

        try:
            time_stats(df)
        except (KeyError, ValueError, IndexError):
            print('Your input for day is incorrect.')
            try_again = input('Would you like to try again? Enter yes or no.\n')
            if try_again.lower() != 'yes':
                break
            else:
                main()

        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        expand(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('-'*40)

            break


if __name__ == "__main__":
	main()
