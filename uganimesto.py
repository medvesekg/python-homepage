import random

class Mesto(object):
    def __init__(self, name, country, url):
        self.name = name
        self.country = country
        self.url = url

mesta = [
    Mesto("Ljubljana", "Slovenije", "ljubljana.jpg"),
    Mesto("Peking", "Kitajske", "beijing.jpg"),
    Mesto("Cape Town", "Juzne Afrike", "capetown.jpg"),
    Mesto("London", "Velike Britanije", "london.jpg"),
    Mesto("Moskva", "Rusije", "moscow.jpg"),
    Mesto("Rim", "Italije", "rome.jpg"),
    Mesto("Tokio", "Japonske", "tokyo.jpg"),
    Mesto("Dunaj", "Avstrije", "vienna.jpg"),
    Mesto("Washington", "ZDA", "washington.jpg"),
]

mesto = mesta[random.randint(0, len(mesta) - 1)]
