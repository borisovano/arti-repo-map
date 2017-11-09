import json
import operator
import argparse
import requests
from requests.auth import HTTPBasicAuth
import os
import logging

MB = 1024 * 1024
my_path = os.path.dirname(os.path.realpath(__file__))
repo_info_cache_file = '{}/cached_repo.json'.format(my_path)

# Set logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main(parsed_arguments):
    repo_info = parsed_arguments.repo

    if repo_info.startswith('http'):
        logger.warning("Remote url is used")
        repo_info = cache_repo_info_locally(repo_info, parsed_arguments.repo_user, parsed_arguments.repo_password)
    sorted_repo_dict = parse_artifactory_repo(repo_info, parsed_arguments.url_lookup_depth)
    print_sorted_repo_dict(sorted_repo_dict)


def parse_artifactory_repo(repo_info, url_lookup_depth):
    with open(repo_info) as arti_json:
        data = json.load(arti_json)

    reposize = {}
    for entry in data["files"]:
        urllist = entry['uri'][1:].split('/')
        urlslice = str(urllist[0:url_lookup_depth])

        if not urlslice in reposize.keys():
            reposize[urlslice] = 0
        reposize[urlslice] = reposize[urlslice] + entry['size']

    return sorted(reposize.items(), key=operator.itemgetter(1))


def print_sorted_repo_dict(sorted_x):
    total_size = 0
    for url, size in sorted_x:
        total_size = total_size + size
        size = sizeof_fmt(size)
        url = '/'.join(eval(url))
        print("{0:<50} - {1:<15} (Total: {2})".format(url, size, sizeof_fmt(total_size)))


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def cache_repo_info_locally(url, user, password):
    logger.info("Caching to repo information to local file: ./{}".format(repo_info_cache_file))
    response = requests.get(url, auth=HTTPBasicAuth(user, password), stream=True)
    # Throw an error for bad status codes
    response.raise_for_status()
    with open(repo_info_cache_file, 'wb') as handle:
        threshold = 0
        for block in response.iter_content(1024):
            handle.write(block)
            size = os.fstat(handle.fileno()).st_size
            if size / MB > threshold:
                logger.info("wrote {} MB to disk".format(int(size / MB)))
                threshold = size / MB + 1
    return repo_info_cache_file


if __name__ == "__main__":
    # Args parsing
    parser = argparse.ArgumentParser(description='Display Artifactory repos by size(with variable lookup depth)')
    parser.add_argument("-d", "--depth",
                        default=4,
                        type=int,
                        help='artifactory url depth',
                        dest="url_lookup_depth")
    parser.add_argument("-r", "--repo",
                        default="cached_repo.json",
                        type=str,
                        help="remote repo(artifactory repo info api) url or local path")
    parser.add_argument("-u", "--user",
                        type=str,
                        dest="repo_user",
                        help="Artifactory user (used in case remote repo url provided)")
    parser.add_argument("-p", "--password",
                        type=str,
                        dest="repo_password",
                        help="Artifactory password (used in case remote repo url provided)")
    options = parser.parse_args()
    main(options)

