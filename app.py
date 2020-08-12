from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import SearchForm
from WeatherService import WeatherService
from pyowm.commons.exceptions import NotFoundError
import os

API_KEY = "ff722f94ac00e2e5fdf2c0f52de09754"
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route("/", methods=["GET", "POST"])
def getWeather():
    form = SearchForm()
    if form.validate_on_submit():
        service = WeatherService(API_KEY)
        try:
            weather = service.getCurrentWeatherByCity(form.city.data)
            location = service.getLocationByCity(form.city.data)
            message = service.analyzeWeather(weather)
        except NotFoundError:
            flash("Город не найден")
            return redirect(url_for('getWeather'))
        return render_template('result.html', weather=weather, location=location, message=message)
    return render_template('search.html', form=form)


if __name__ == '__main__':
    app.run()
