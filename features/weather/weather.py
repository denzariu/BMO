import requests

def weather_in_city(lat, long, key):
    #url = 'https://wttr.in/{}'.format(city)

    #lat = float("{:.2f}".format(lat))
    #long = float("{:.2f}".format(long))
    url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(long) + "&appid=" + str(key)
    print(url)
    response = requests.request("GET", url, params='').json()
    print(response)
    if response["cod"] != "404" and response["cod"] != "401":
        print(response)
        print(response["main"])
        y = response["main"]
        
        current_temperature = y["temp"]
    
        current_pressure = y["pressure"]

        current_humidity = y["humidity"]
    
        z = response["weather"]

        weather_description = z[0]["description"]
    
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidity) +
            "\n description = " +
                        str(weather_description))

        return [int(current_temperature - 273.15), int(y["feels_like"] - 273.15), weather_description]
    else:
        print(" City Not Found ")
    
