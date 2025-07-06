from flask import Flask, request, render_template
from datetime import datetime, timedelta, date
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/converter')
def converter():
    return render_template('form.html', timezones=pytz.all_timezones)

@app.route('/convert', methods=['POST'])
def convert():
    dt_input = request.form['datetime']
    from_zone = request.form['from_zone']
    to_zone = request.form['to_zone']
    dt = datetime.strptime(dt_input, "%Y-%m-%dT%H:%M")
    from_tz = pytz.timezone(from_zone)
    to_tz = pytz.timezone(to_zone)
    localized_dt = from_tz.localize(dt)
    converted_dt = localized_dt.astimezone(to_tz)
    # Using render_template for consistency with new styling
    return render_template('result.html',
                           title="Converted Time",
                           messages=[
                               f"From ({from_zone}): {localized_dt.strftime('%Y-%m-%d %H:%M')}",
                               f"To ({to_zone}): {converted_dt.strftime('%Y-%m-%d %H:%M')}"
                           ],
                           back_link='/converter')

@app.route('/countdown')
def countdown_form():
    # Pass seconds as None initially.
    # The |tojson filter in the template will correctly render this as 'null' in JS.
    return render_template('countdown.html', timezones=pytz.all_timezones, seconds=None)

@app.route('/countdown/start', methods=['POST'])
def start_countdown():
    dt_input = request.form['datetime']
    zone = request.form['timezone']
    event_time = pytz.timezone(zone).localize(datetime.strptime(dt_input, "%Y-%m-%dT%H:%M"))
    now_utc = datetime.now(pytz.utc)
    remaining = event_time.astimezone(pytz.utc) - now_utc
    total_seconds = int(remaining.total_seconds())
    
    # Pass total_seconds. The |tojson filter in the template will correctly render this as a number in JS.
    return render_template('countdown.html', seconds=total_seconds, timezones=pytz.all_timezones)

@app.route('/calculator')
def time_calc_form():
    return render_template('calculator.html', timezones=pytz.all_timezones)

@app.route('/calculator/result', methods=['POST'])
def calc_result():
    dt_input = request.form['datetime']
    hours = int(request.form['hours'])
    operation = request.form['operation']
    zone = request.form['timezone']
    dt = pytz.timezone(zone).localize(datetime.strptime(dt_input, "%Y-%m-%dT%H:%M"))
    delta = timedelta(hours=hours)
    result = dt + delta if operation == 'add' else dt - delta
    # Using render_template for consistency with new styling
    return render_template('result.html',
                           title="New Time",
                           messages=[f"New Time ({zone}): {result.strftime('%Y-%m-%d %H:%M')}"],
                           back_link='/calculator')

@app.route('/zones')
def zones_by_country():
    from pytz import country_names, country_timezones
    data = {country_names[c]: country_timezones.get(c, []) for c in country_names}
    return render_template('zones_by_country.html', data=data)

@app.route('/stopwatch')
def stopwatch():
    return render_template('stopwatch.html')

@app.route('/age')
def age_form():
    return render_template('age.html')

@app.route('/age/result', methods=['POST'])
def age_result():
    dob = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    # Using render_template for consistency with new styling
    return render_template('result.html',
                           title="Your Age",
                           messages=[f"You're {years} years old."],
                           back_link='/age')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)