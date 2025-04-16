import requests
import pandas as pd
import time
import pycountry
from tqdm import tqdm


from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    return [country.alpha_2 for country in pycountry.countries]


def get_reviews(country_code, app_id):
    url = f"https://itunes.apple.com/{country_code}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
    reviews = []

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return "failed", []

        data = r.json()

        # If there are reviews for the country, they will be inside 'feed' > 'entry'. Otherwise, the key 'entry' will not exist
        # If 'entry' exists, it could hold 2 different types of values depending on whether it only contains 1 review ('dict') or more ('list' of dicts)
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
            return "success", reviews
        else:
            return "no_reviews", []

    except requests.exceptions.RequestException:
        return "failed", []
    except Exception:
        return "failed", []


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


def fetch_reviews_threaded(app_id, country_codes, max_workers=15):
    print(f"🚀 Starting threaded review fetch with {max_workers} workers")

    def task(country_code):
        status, reviews = get_reviews(country_code, app_id)
        return country_code, status, reviews

    all_reviews = []
    successful, no_reviews, failed = [], [], []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task, code): code for code in country_codes}
        for future in as_completed(futures):
            country_code, status, reviews = future.result()
            if status == "success":
                all_reviews.extend(reviews)
                successful.append(country_code)
            elif status == "no_reviews":
                no_reviews.append(country_code)
            elif status == "failed":
                failed.append(country_code)

    return all_reviews, successful, no_reviews, failed


def create_pandas_dataframe(reviews_list):
    print("🗂️ Creating dataframe")
    df = pd.DataFrame(reviews_list)
    return df


def save_to_excel(df, app_name):
    print("💾 Saving to excel")
    df.to_excel(f"ios_{app_name.lower()}_reviews.xlsx")


def write_summary_log(successful, no_reviews, failed, apps_processed, elapsed_time):
    with open("review_fetch_summary.log", "w") as log_file:
        log_file.write("📱 Apps Processed:\n")
        for app in apps_processed:
            log_file.write(f" - {app}\n")
        log_file.write("\n")

        log_file.write(f"⏱️ Total Execution Time: {elapsed_time:.2f} seconds\n\n")
        log_file.write(
            f"✅ Reviews successfully fetched from: {', '.join(successful)}\n"
        )
        log_file.write(f"🕳️ No reviews available for: {', '.join(no_reviews)}\n")
        log_file.write(f"❌ Failed requests for: {', '.join(failed)}\n")


def main():
    start_time = time.time()
    country_codes = get_all_country_codes()

    all_successful = set()
    all_no_reviews = set()
    all_failed = set()
    apps_processed = []

    try:
        for app in APPS_LIST:
            app_name = app.lower()
            app_id = APPS_LIST[app]
            apps_processed.append(app_name)
            print(f"⌛️ Processing app {app_name}")

            (
                all_countries_reviews,
                successful_countries,
                no_reviews_countries,
                failed_countries,
            ) = fetch_reviews_threaded(app_id, country_codes, max_workers=15)

            all_successful.update(successful_countries)
            all_no_reviews.update(no_reviews_countries)
            all_failed.update(failed_countries)

            parsed_reviews = parse_reviews(all_countries_reviews)
            sorted_by_most_recent_df = create_pandas_dataframe(
                parsed_reviews
            ).sort_values(by="date", ascending=False)
            save_to_excel(sorted_by_most_recent_df, app_name)

    except Exception as e:
        print(f"❌ Script terminated due to error: {e}")

    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 🔐 Make sure this always runs, even if there's an error
        write_summary_log(
            sorted(all_successful),
            sorted(all_no_reviews),
            sorted(all_failed),
            apps_processed,
            elapsed_time,
        )

        print(f"📝 Summary log written.")
        print(f"⏱️ Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
