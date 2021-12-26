#!/usr/bin/env python3

# Import the standard python library
import subprocess
import argparse
from datetime import datetime,timedelta
import arrow
import boto3

# Set the registry & retrieve release info
image_registry = "public.ecr.aws/"
release_bucket_name = 'automate-tern'
release_file = "ficticious_release_11.3.txt"
s3 = boto3.resource('s3')
s3.meta.client.download_file(release_file, release_bucket_name, release_file)
print (s3)

# Create the parser
parser = argparse.ArgumentParser(
    description="tern_fetch_.py: Compute the Tern file for a repository"
)

# Add arguments for project, repo, tag, and push time
parser.add_argument(
    "--project", "-p", dest="project_name", help="Name of the project.  Required."
)
parser.add_argument(
    "--repo",
    "-r",
    dest="repo_name",
    required=True,
    help="Name of the repository.  Required.",
)
parser.add_argument(
    "--tag", "-t", dest="tag_name", required=True, help="Name of the tag"
)
parser.add_argument(
    "--push-time", "-d", dest="push_time", help="Perform scan on artifacts pushed to Harbor in last __ days", type=int
)
parser.add_argument(
    "--output-dir", "-o", dest="output_dir", help="Output directory for the Tern file"
)
parser.add_argument(
    "--verbose", "-v", action="store_true", dest="verbose", help="Verbose debugging"
)

# Parse the arguments
args = parser.parse_args()

# Use args to define repo:tag then format output
image = image_registry + args.project_name + "/" + args.repo_name + ":" + args.tag_name
#print(image)
newformat = image.replace(":", "-").replace("/", "-")

# print('Hello,', args)
#Check the push_time fo the artifact
#cmnd = 'curl -X GET https://system.registry.aws-us-east-2.devstar.cloud/api/v2.0/projects/' + args.project_name + '/repositories/' + args.repo_name + '/artifacts?page=%d&page_size=40'
#print(cmnd)
#os.system(cmnd)

if args.push_time is not None:
    arw = arrow.utcnow()
    print(args.push_time, "days ago the date was",  arw.shift(days=-args.push_time), "Checking for pushes occuring since then.")
    #print(push_time)
    cmnd = 'curl -X GET ' + image_registry + args.project_name + '/repositories/' + args.repo_name + '/artifacts?page=%d&page_size=40'
    cmnd_response = subprocess.call(cmnd, shell=True) # returns the exit code
    print (cmnd_response)

""" cmnd = (
    'sudo /mnt/c/projects/tern/docker_run.sh ternd "report -i %s -y 1" > /tmp/%s.txt'
    % (image, newformat)
) """
