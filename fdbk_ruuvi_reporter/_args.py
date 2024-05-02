#!/usr/bin/env python3

from fdbk.utils import get_reporter_argparser


def parse_args():
    parser = get_reporter_argparser()
    parser.add_argument(
        "--save-topic",
        nargs=2,
        type=str,
        metavar=(
            "MAC",
            "TOPIC_ID",
        ),
        help="Save topic id for mac")
    parser.add_argument(
        "--create-topic",
        nargs=2,
        type=str,
        metavar=(
            "NAME",
            "MAC",
        ),
        help="Create topic for name and mac")
    parser.add_argument(
        "--pull-topics",
        action="store_true",
        help="Pull topics data from DB")
    parser.add_argument(
        "--update-topics",
        action="store_true",
        help="Update topics in the DB to the latest version")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print package version")

    return parser.parse_args()
