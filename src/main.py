import json
import os
from pathlib import Path

import vk_api
from dotenv import load_dotenv

from utils import convert_unixtime_to_datetime, is_after, is_sunday

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MAX_COUNT = 100  # API limit per one request

with Path.open("../config.json") as config_file:
    config = json.load(config_file)


GRP_ID = config["owner_id"]  # VK group ID with minus sign
nposts_to_parse = config["number_of_posts_to_parse"]  # 0 to parse all


api = vk_api.VkApi(token=ACCESS_TOKEN, api_version="5.199")


def get_total_num_of_posts() -> int:
    return api.method(
        method="wall.get",
        values={"owner_id": GRP_ID, "count": 1},
    )["count"]


def parse_posts(offset: int, num_to_parse: int = MAX_COUNT) -> list[dict[str,]]:
    """Function uses API method wall.get to parse posts.

    Args:
        offset: the number of posts to skip from the last (by date) post.
            so, if we enumerate posts from nposts to 1 (going backwards in time),
            this func parses [offset; offset + num_to_parse]
        num_to_parse: the number of posts to parse. By default MAX_COUNT=100 (api limit)

    Returns:
        list of posts, each post is the dict with keys:
            text - full text of post
            date - unixtime of post publication
            link_to_post - link to post on VK
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


def parse_only_sunday_posts() -> None:
    """Function for my specific task.

    I needed to parse only posts that
        1) were published on sundays
        2) were published after some date (which unixtime is 1474146000)
    So after parsing all posts we need to filter only ones
      that is appropriate and than write them to file.
    Also, enumerates all posts.
    """
    date_stop = 1474146000  # 18 сентября 2016 0:00
    global nposts_to_parse  # noqa:PLW0603

    nposts_total = get_total_num_of_posts()

    if not nposts_to_parse or nposts_total < nposts_to_parse:
        nposts_to_parse = nposts_total

    print(f"{nposts_total = }")
    print(f"{nposts_to_parse = }")

    counter = 1
    post_offset = nposts_to_parse

    with Path.open("../results/sunday.md", "w", encoding="utf-8") as output_file:
        while post_offset > 0:
            # number of posts to parse on this iteration
            count = min(MAX_COUNT, post_offset)

            print(f"Parsing posts from {post_offset - count} to {post_offset}")

            posts = parse_posts(post_offset - count, count)
            post_offset -= count

            for post_data in posts[::-1]:
                if is_sunday(post_data["date"]) and is_after(
                    post_data["date"],
                    date_stop,
                ):
                    output_file.write(
                        "# "
                        + str(counter)
                        + "\n"
                        + convert_unixtime_to_datetime(post_data["date"])
                        + " | "
                        + post_data["link_to_post"]
                        + "\n\n"
                        + post_data["text"]
                        + "\n\n---\n\n",
                    )
                    counter += 1


def parse_all_posts() -> None:
    nposts_total = get_total_num_of_posts()
    global nposts_to_parse  # noqa:PLW0603
    if not nposts_to_parse or nposts_total < nposts_to_parse:
        nposts_to_parse = nposts_total

    print(f"{nposts_total = }")
    print(f"{nposts_to_parse = }")

    counter = nposts_to_parse  # for enumerating posts. most recent = max value
    post_offset = 0

    with Path.open("../results/all.md", "w", encoding="utf-8") as output_file:
        while post_offset < nposts_to_parse:
            # number of posts to parse on this iteration
            count = min(nposts_to_parse - post_offset, MAX_COUNT)

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
                    + "\n\n---\n\n",
                )
                counter -= 1


if __name__ == "__main__":
    parse_all_posts()
    parse_only_sunday_posts()
