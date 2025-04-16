import requests
import pandas as pd
import time
import pycountry

from dataclasses import dataclass

from constants import APPS_LIST


@dataclass
class Review:
    date: str
    country: str
    user_rating: int
    title: str
    body: str
    vote_sum: int
    vote_count: int
    app_version: str
    
def get_all_country_codes():
    return [
        country.alpha_2 for country in pycountry.countries]


def get_reviews(country_code, app_id):
    print(f"🌎 Getting reviews for country {country_code}")
    url = f"https://itunes.apple.com/{country_code}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
    reviews = []

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            print(f"⚠️ Failed for {country_code} — Status code: {r.status_code}")
            return []

        data = r.json()
        if "feed" in data and "entry" in data["feed"]:
            entry = data["feed"]["entry"]
            if isinstance(entry, dict):
                entry["country"] = country_code
                reviews.append(entry)
            elif isinstance(entry, list):
                entries_with_country = [
                    {**review, "country": country_code} for review in entry
                ]
                reviews.extend(entries_with_country)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {country_code}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error for {country_code}: {e}")

    return reviews


def parse_reviews(reviews_data):
    print("🎨 Parsing reviews")
    parsed_reviews = []
    try:
        for review_item in reviews_data:
            review = Review(
                date=review_item["updated"]["label"].split("T")[0],
                country=review_item["author"]["uri"]["label"].split("/")[3],
                app_version=review_item["im:version"]["label"],
                user_rating=int(review_item["im:rating"]["label"]),
                title=review_item["title"]["label"],
                body=review_item["content"]["label"],
                vote_sum=int(review_item["im:voteSum"]["label"]),
                vote_count=int(review_item["im:voteCount"]["label"]),
            )
            parsed_reviews.append(review)
        return parsed_reviews
    except Exception as e:
        print(f"An error occurred: {e}")


def create_pandas_dataframe(reviews_list):
    print("🗂️ Creating dataframe")
    df = pd.DataFrame(reviews_list)
    return df


def save_to_excel(df, app_name):
    print("💾 Saving to excel")
    df.to_excel(f"ios_{app_name.lower()}_reviews.xlsx")


def main():
    start_time = time.time()
    all_countries_reviews = []
    country_codes = get_all_country_codes()
    for app in APPS_LIST:
        app_name = app.lower()
        app_id = APPS_LIST[app]
        print(f"⌛️ Processing app {app_name}")
        for country_code in country_codes:
            country_reviews = get_reviews(country_code, app_id)
            all_countries_reviews.extend(country_reviews)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    parsed_reviews = parse_reviews(all_countries_reviews)
    sorted_by_most_recent_df = create_pandas_dataframe(parsed_reviews).sort_values(
        by="date", ascending=False
    )
    save_to_excel(sorted_by_most_recent_df, app_name)


if __name__ == "__main__":
    main()
