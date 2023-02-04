import requests


def cases_of_covid(country):
    try:
        cases = get_covid_cases(country)
        return cases
    except Exception as e:
        print("Error: ", e)
        return None

def get_covid_cases(country):
    try:
        response = requests.get('https://api.covid19api.com/live/country/' + country + '/status/confirmed').json()
        totalActiveCases = response[len(response) - 1].get('Active') - response[len(response) - 2].get('Active')
        return totalActiveCases
    except Exception as e:
        print("Error at data fetch (COVID Active Cases Today): ", e)
   
   
def cases_of_covid_alltime(country):
    try:
        cases = get_covid_cases_alltime(country)
        return cases
    except Exception as e:
        print("Error: ", e)
        return None 
def get_covid_cases_alltime(country):
    try:
        response = requests.get('https://api.covid19api.com/live/country/' + country + '/status/confirmed').json()
        totalActiveCases = response[len(response) - 1].get('Confirmed')
        return totalActiveCases
    except Exception as e:
        print("Error at data fetch (COVID Active Cases Today): ", e)