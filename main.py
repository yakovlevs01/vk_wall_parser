import vk_api
import os
import json
from dotenv import load_dotenv
from test import sundays_to_2016, is_appropriate_post, convert_unixtime_to_datetime


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MAX_COUNT = 100  # API limit

with open("config.json") as config_file:
    config = json.load(config_file)


GRP_ID = config["owner_id"]  # VK group ID with minus sign
nposts_to_parse = config["number_of_posts_to_parse"]  # 0 to parse all


api = vk_api.VkApi(token=ACCESS_TOKEN, api_version="5.137")


def get_total_num_of_posts() -> int:
    total_num_of_posts = api.method(
        method="wall.get",
        values={"owner_id": GRP_ID, "count": 1},
    )["count"]

    return total_num_of_posts


def parse_posts(offset: int, num_to_parse: int = MAX_COUNT) -> list[dict[str,]]:
    """Offset is number of posts to skip from the last (by date) post.

    so, if we enumerate posts from nposts to 1 (going backwards in time),
    this func parses    [offset; offset + num_to_parse]
    """
    data = api.method(
        method="wall.get",
        values={
            "owner_id": GRP_ID,
            "offset": offset,
            "count": num_to_parse,
        },
    )["items"]

    return [
        {
            "text": post["text"],
            "date": post["date"],
            "link_to_post": "https://vk.com/wall" + str(GRP_ID) + "_" + str(post["id"]),
        }
        for post in data
    ]


def parse_only_sunday_posts():
    global nposts_to_parse

    nposts_total = get_total_num_of_posts()

    if not nposts_to_parse or nposts_total < nposts_to_parse:
        nposts_to_parse = nposts_total

    print(f"{nposts_total = }")
    print(f"{nposts_to_parse = }")

    counter = nposts_to_parse
    post_offset = 0

    with open("result_sunday.md", "w", encoding="utf-8") as output_file:
        while post_offset < nposts_to_parse:
            count = (  # number of posts to parse on this iteration
                MAX_COUNT
                if nposts_to_parse - post_offset > MAX_COUNT
                else nposts_to_parse - post_offset
            )

            print(f"Parsing posts from {post_offset} to {post_offset + count}")

            posts = parse_posts(post_offset, count)
            post_offset += count

            for post_data in posts:
                if is_appropriate_post(post_data["date"], sundays_to_2016):
                    output_file.write(
                        "# "
                        + str(counter)
                        + "\n"
                        + convert_unixtime_to_datetime(post_data["date"])
                        + " | "
                        + post_data["link_to_post"]
                        + "\n\n"
                        + post_data["text"]
                        + "\n\n---\n\n"
                    )
                    counter -= 1


def parse_all_posts():
    global nposts_to_parse

    nposts_total = get_total_num_of_posts()

    if not nposts_to_parse or nposts_total < nposts_to_parse:
        nposts_to_parse = nposts_total

    print(f"{nposts_total = }")
    print(f"{nposts_to_parse = }")

    counter = nposts_to_parse
    post_offset = 0

    with open("result.md", "w", encoding="utf-8") as output_file:
        while post_offset < nposts_to_parse:
            count = (  # number of posts to parse on this iteration
                MAX_COUNT
                if nposts_to_parse - post_offset > MAX_COUNT
                else nposts_to_parse - post_offset
            )

            print(f"Parsing posts from {post_offset} to {post_offset + count}")

            posts = parse_posts(post_offset, count)
            post_offset += count

            for post_data in posts:
                output_file.write(
                    "# "
                    + str(counter)
                    + "\n"
                    + convert_unixtime_to_datetime(post_data["date"])
                    + " | "
                    + post_data["link_to_post"]
                    + "\n\n"
                    + post_data["text"]
                    + "\n\n---\n\n"
                )
                counter -= 1


if __name__ == "__main__":
    parse_all_posts()
