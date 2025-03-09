import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

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
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("Which city would you like to analyze? (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input, please enter a valid city name.")
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? (January to June, or 'all' for no filter): ").strip().lower()
        if month in months:
            break
        print("Invalid input, please enter a valid month or 'all'.")
    
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? (Monday to Sunday, or 'all' for no filter): ").strip().lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day or 'all'.")
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')

    # filter the data by month and day
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def display_raw_data(df):
    """Displays raw data upon request."""
    row_index = 0
    while True:
        view_data = input('Would you like to see 5 rows of raw data? Enter yes or no: ').lower()
        if view_data == 'yes':
            print(df.iloc[row_index:row_index+5])
            row_index += 5
        elif view_data == 'no':
            print("Exiting raw data display.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(f"Most Common Month: {df['month'].mode()[0]}")
    print(f"Most Common Day: {df['day_of_week'].mode()[0].title()}")
    print(f"Most Common Start Hour: {df['Start Time'].dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f"Most Common Start Station: {df['Start Station'].mode()[0]}")
    print(f"Most Common End Station: {df['End Station'].mode()[0]}")
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    print(f"Most Common Trip: {df['Trip'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print(f"Total Travel Time: {df['Trip Duration'].sum()} seconds")
    print(f"Mean Travel Time: {df['Trip Duration'].mean()} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:")
    print(df['User Type'].value_counts())

    if 'Gender' in df:
        print("\nGender:")
        print(df['Gender'].value_counts())
    
    if 'Birth Year' in df:
        print("\nBirth Year Stats:")
        print(f"Earliest: {int(df['Birth Year'].min())}")
        print(f"Most Recent: {int(df['Birth Year'].max())}")
        print(f"Most Common: {int(df['Birth Year'].mode()[0])}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# some visualtizon i learned from the data analysis nano degree , to enhance user experince
def plot_trip_duration(df):
    """Plots a histogram of trip durations."""
    plt.figure(figsize=(10,6))
    plt.hist(df['Trip Duration'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Trip Duration Distribution')
    plt.xlabel('Trip Duration (seconds)')
    plt.ylabel('Frequency')
    plt.savefig('trip_duration_distribution.png')  # Save the plot as an image file
    plt.close()

def plot_popular_stations(df):
    """Plots bar charts for most popular stations."""
    start_station_counts = df['Start Station'].value_counts().head(10)
    end_station_counts = df['End Station'].value_counts().head(10)

    # Plotting most popular start stations
    plt.figure(figsize=(10,6))
    start_station_counts.plot(kind='bar', color='salmon')
    plt.title('Top 10 Most Popular Start Stations')
    plt.xlabel('Start Station')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('most_popular_start_stations.png')  # Save the plot as an image file
    plt.close()

    # Plotting most popular end stations
    plt.figure(figsize=(10,6))
    end_station_counts.plot(kind='bar', color='lightgreen')
    plt.title('Top 10 Most Popular End Stations')
    plt.xlabel('End Station')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('most_popular_end_stations.png')  # Save the plot as an image file
    plt.close()

def plot_user_types(df):
    """Plots a pie chart for user types."""
    user_types = df['User Type'].value_counts()
    plt.figure(figsize=(8,8))
    user_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
    plt.title('Distribution of User Types')
    plt.ylabel('')  
    plt.tight_layout()
    plt.savefig('user_types_distribution.png')
    plt.close()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
