import config
from twython import Twython
from flask import Flask, request, session, redirect, render_template

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

CONSUMER_KEY = config.twitter_keys["CONSUMER_KEY"]
CONSUMER_SECRET = config.twitter_keys["CONSUMER_SECRET"]

CALLBACK_URL = "http://0.0.0.0:8080/result"


# 認証用URLを生成する
def create_auth_url():
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)
    auth = twitter.get_authentication_tokens(callback_url=CALLBACK_URL)
    session["oauth_token"] = auth["oauth_token"]
    session["oauth_secret"] = auth["oauth_token_secret"]
    redirect_url = auth["auth_url"]
    return redirect(redirect_url)


def twitter_auth():
    oauth_verifier = request.values.get("oauth_verifier", None)
    twitter = Twython(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        session["oauth_token"],
        session["oauth_secret"]
    )
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    session["access_token"] = final_step["oauth_token"]
    session["access_secret"] = final_step["oauth_token_secret"]


# ユーザー情報を取得する
def get_user_data(api):
    user = api.me()._json
    user_data_dic = {
        "id": user.get("id"),
        "id_str": user.get("id_str"),
        "name": user.get("name"),
        "screen_name": user.get("screen_name"),
        "location": user.get("location"),
        "profile_location": user.get("profile_location"),
        "description": user.get("description"),
        "url": user.get("url"),
        "protected": user.get("protected"),
        "followers_count": user.get("followers_count"),
        "friends_count": user.get("friends_count"),
        "listed_count": user.get("listed_count"),
        "created_at": user.get("created_at"),
        "favourites_count": user.get("favourites_count"),
        "utc_offset": user.get("utc_offset"),
        "time_zone": user.get("time_zone"),
        "geo_enabled": user.get("geo_enabled"),
        "verified": user.get("verified"),
        "statuses_count": user.get("statuses_count"),
        "lang": user.get("lang"),
        "contributors_enabled": user.get("contributors_enabled"),
        "is_translator": user.get("is_translator"),
        "is_translation_enabled": user.get("is_translation_enabled"),
        "profile_background_color": user.get("profile_background_color"),
        "profile_background_image_url": user.get("profile_background_image_url"),
        "profile_background_image_url_https": user.get("profile_background_image_url_https"),
        "profile_background_tile": user.get("profile_background_tile"),
        "profile_image_url": user.get("profile_image_url"),
        "profile_image_url_https": user.get("profile_image_url_https"),
        "profile_banner_url": user.get("profile_banner_url"),
        "profile_link_color": user.get("profile_link_color"),
        "profile_sidebar_border_color": user.get("profile_sidebar_border_color"),
        "profile_sidebar_fill_color": user.get("profile_sidebar_fill_color"),
        "profile_text_color": user.get("profile_text_color"),
        "profile_use_background_image": user.get("profile_use_background_image"),
        "has_extended_profile": user.get("has_extended_profile"),
        "default_profile": user.get("default_profile"),
        "default_profile_image": user.get("default_profile_image"),
        "following": user.get("following"),
        "follow_request_sent": user.get("follow_request_sent"),
        "notifications": user.get("notifications"),
        "translator_type": user.get("translator_type"),
        "suspended": user.get("suspended"),
        "needs_phone_verification": user.get("needs_phone_verification"),
    }
    return user_data_dic


@app.route("/")
def root():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    return create_auth_url()


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/result")
def result():

    if "access_token" not in session and "access_secret" not in session:
        twitter_auth()

    twitter = Twython(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        session["access_token"],
        session["access_secret"]
    )

    user = twitter.verify_credentials()
    return render_template("result.html", user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
