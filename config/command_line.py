import argparse
def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("url", type=str)
    parser.add_argument("--timeout_func", type=float, default=10.0)
    parser.add_argument("--timeout_response", type=float, default=5.0)
    parser.add_argument("--concurrency", type=int, default=1)

    args = parser.parse_args()

    if args.timeout_func <= 0:
        parser.error("--timeout_func must be greater than 0")

    if args.timeout_response <= 0:
        parser.error("--timeout_response must be greater than 0")

    if args.concurrency <= 0:
        parser.error("--concurrency must be greater than 0")

    return args

