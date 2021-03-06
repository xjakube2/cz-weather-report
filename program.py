#!/usr/bin/env python3

"""
Author: Petr Jakubec
Date: 2017-09-28
Project: weather client
Find combinations in a database of flights with a given restrictions
"""

import requests
import bs4
import collections


# namedtuple for better control over variables in the output
WeatherReport = collections.namedtuple('WeatherReport',
                                       'cond, temp, scale, loc')


def main():
    code = input('What czech city do you want the weather for (Brno)? ')

    html = get_html_from_web(code)
    report = get_weather_from_html(html)

    print('The temp in {} is {} {} and {}'.format(
        report.loc,
        report.temp,
        report.scale,
        report.cond
    ))

# getting the plain html
def get_html_from_web(city):
    url = 'https://www.wunderground.com/weather/cz/{}'.format(city)
    response = requests.get(url)

    return response.text

# parsing and cleaning the html 
def get_weather_from_html(html):

    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()

    loc = cleanup_text(loc)
    loc = find_city_and_state_from_location(loc)
    condition = cleanup_text(condition)
    temp = round((int(cleanup_text(temp))-32)/9*5, 1)
    scale = '°C'

    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report

# munging the location
def find_city_and_state_from_location(loc: str):
    parts = loc.split('\n')
    return parts[0].strip()

# munging the response
def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


if __name__ == '__main__':
    main()
