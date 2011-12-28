from flask import Module, render_template, request, redirect, url_for, session, flash, g
from flaskext.oauth import OAuth
from functools import wraps
from crowdwoo import queries

# define the remote oauth application
twitter = OAuth().remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='foo',
    consumer_secret='bar'
)

# define this module
auth = Module(__name__)


@auth.route('/signin')
def signin():
    return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))


@auth.route('/signout')
def signout():
    if 'user' in session:
        del(session['user'])
    return redirect(url_for('core.index'))


@auth.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    
    # if they denied the request, then send them to the splash
    if resp is None:
        return redirect(url_for('core.index'))
    
    user = queries.find_twitter_id(resp['user_id'])
    
    # create this user if they are new
    if user is None:
        user = queries.create_user(resp)
        user = queries.find_user(user)
    
    # just in case something blows up
    if user is None:
        return redirect(url_for('core.index'))
    
    # update the users oauth settings if they have changed
    if user.get('oauth_token') != resp['oauth_token'] or user.get('oauth_token_secret') != resp['oauth_token_secret']:
        queries.set_tokens(user, resp)
    
    # store this user's database id in their session
    session['user'] = dict(_id=user['_id'], twitter_handle=user['twitter_handle'], oauth_token=resp['oauth_token'], oauth_token_secret=resp['oauth_token_secret'])
    
    return redirect(url_for('core.stats'))


@twitter.tokengetter
def get_twitter_token():
    
    # provide the oauth tokens if theyre already in the session
    if 'user' in session and 'oauth_token' in session['user'] and 'oauth_token_secret' in session['user']:
        return session['user']['oauth_token'], session['user']['oauth_token_secret']


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated