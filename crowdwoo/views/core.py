import datetime as dt
from flask import Module, render_template, redirect, url_for, session, request
from crowdwoo.views.auth import requires_auth
from crowdwoo import queries

# define this module
core = Module(__name__)

@core.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('core.stats'))
    user_count = queries.users_count()
    return render_template('core/index.html', user_count=user_count)


@core.route('/stats')
@requires_auth
def stats():
    
    # generate the stats
    user_count = queries.users_count()
    last_day = last_day_of_month()
    days_until = last_day - dt.date.today()
    usage_stats = dict(user_count=user_count, last_day=last_day, days_until=days_until)
    
    return render_template('core/stats.html', stats=usage_stats)


def last_day_of_month():
    today = dt.date.today() 
    nm = dt.date(today.year, today.month, 15) + dt.timedelta(days=31)
    return dt.date(nm.year, nm.month, 1) - dt.timedelta(days=1)