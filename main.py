#!/usr/bin/env python
import os
import jinja2
import webapp2
import time
import random
import re



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        cas = time.strftime("%H:%M:%S")
        title = "Gregor Medvesek | O meni"
        params = {"cas": cas,
                  "title": title,
                  }
        return self.render_template("o-meni.html", params=params)

class ProjectHandler(BaseHandler):
    def get(self):
        cas = time.strftime("%H:%M:%S")
        params = {"cas": cas,
                  "title": "Gregor Medvesek | Moji Projekti",
                  "body_id": "portfolio"
                  }
        return self.render_template("projekti.html", params=params)

class BlogHandler(BaseHandler):
    def get(self):
        cas = time.strftime("%H:%M:%S")
        params = {"cas": cas,
                  "title": "Gregor Medvesek | Blog",
                  "body_id": "blog"
                  }
        return self.render_template("blog.html", params=params)

class ContactHandler(BaseHandler):
    def get(self):
        cas = time.strftime("%H:%M:%S")
        params = {"cas": cas,
                  "title": "Gregor Medvesek | Kontakt"
                  }
        return self.render_template("kontakt.html", params=params)

class LotoHandler(BaseHandler):
    def get(self):
        return self.render_template("loto.html")
    def post(self):
        loto_numbers = []
        for i in range (1,9):
            loto_numbers.append(random.randint(1,39))
        params = {"loto": loto_numbers}
        return self.render_template("loto.html", params=params)

class CalculatoHandler(BaseHandler):
    def get(self):
        return self.render_template("kalkulator.html")
    def post(self):
        number1 = self.request.get("number1")
        operand = self.request.get("operand")
        number2 = self.request.get("number2")


        try:

           number1 = int(number1)
           number2 = int(number2)

        except:

            operand = ""


        if operand == "+":
            rezultat = number1 + number2
        elif operand == "-":
            rezultat = number1 - number2
        elif operand == "/":
            if number2 == "0":
                rezultat = "Deljenje z 0 ni dovoljeno."
            else:
                rezultat = float(number1) / float(number2)
        elif operand == "*":
            rezultat = number1 * number2
        else:
            rezultat = "Napaka. Poskusi znova."

        params = {"rezultat": str(rezultat)}
        return self.render_template("kalkulator.html", params=params)


class GuessTheNumberHandler(BaseHandler):
    def get(self):
        return self.render_template("uganistevilo.html")
    def post(self):
        secret_number = 37
        rezultat = ""

        guess = int(self.request.get("ugani-stevilo"))

        if secret_number == guess:
            rezultat = "Cestitam. Uganil si skrito stevilo."
        elif guess > secret_number:
            rezultat = "Tvoje stevilo je previsoko. Poskusi znova."
        elif guess < secret_number:
            rezultat = "Tvoje stevilo je prenizko. Poskusi znova."

        params = {"rezultat": rezultat}

        return self.render_template("uganistevilo.html", params=params)

class ConverterHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")
    def post(self):
        try:
            km = self.request.get("km")
            mi = float(km) * 0.621
            params = {"km": km, "mi": mi}
            return self.render_template("pretvornik.html", params=params)
        except:
            self.write("Napaka")


class MestaHandler(BaseHandler):
    from uganimesto import Mesto

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

    def get(self):

        self.mesto = self.mesta[random.randint(0, len(self.mesta) - 1)]

        params = {
            "city": self.mesto.name,
            "country": self.mesto.country,
            "background": self.mesto.url

        }
        return self.render_template("mesta.html", params=params)




class ForenzikiHandler(BaseHandler):
    def get(self):
        return self.render_template("forenzicniprogram.html")
    def post(self):

        sequences = {
            "Hair": {
                "Crna": "CCAGCAATCGC",
                "Rjava": "GCCAGTGCCG",
                "Korencek": "TTAGCTATCGC"
            },
            "Face": {
                "Kvadraten": "GCCACGG",
                "Okrogel": "ACCACAA",
                "Ovalen": "AGGCCTCA"
            },
            "Eyes": {
                "Modra": "TTGTGGTGGC",
                "Zelena": "GGGAGGTGGC",
                "Rjava": "AAGTAGTGAC"
            },
            "Sex": {
                "Moski": "TGCAGGAACTTC",
                "Zenski": "TGAAGGACCTTC"
            },
            "Race": {
                "Belec": "AAAACCTCA",
                "Crnec": "CGACTACAG",
                "Azijec": "CGCGGGCCG"
            }
        }

        features = {}
        for feature in sequences:
            for value, substring in sequences[feature].iteritems():
                if substring in self.request.get("DNA"):
                    features[feature] = value

        return self.render_template("forenzicniprogram.html", params=features)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/projekti', ProjectHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/kontakt', ContactHandler),
    webapp2.Route('/loto', LotoHandler),
    webapp2.Route('/kalkulator', CalculatoHandler),
    webapp2.Route('/uganistevilo', GuessTheNumberHandler),
    webapp2.Route('/pretvornik', ConverterHandler),
    webapp2.Route('/uganimesto', MestaHandler),
    webapp2.Route('/forenzicniprogram', ForenzikiHandler),

], debug=True)
