#!/usr/bin/env python

import requests
import sys
import os
import json
from pathlib import Path
import subprocess


# Set the organization and team names
org_name = 'course-1'
team_name = 'students'

# Set the Gitea server URL and API access token
server_url = 'https://helx-test-git.apps.renci.org'
access_token = '<add-token-here>'

# Set the headers with the API access token
headers = {
    'Authorization': f'Basic {access_token}',
    'Accept': 'application/json'
}

data_dir = "data"
course_dir = "course-1"
assignment_dir = "assignment1"
course_path = f'/{data_dir}/{course_dir}'
assignment_path = f'/{data_dir}/{course_dir}/{assignment_dir}'


def create_ottergrader_gitea_dirs():

    # Create directory for repos to clone into:
    clone_path = Path(course_path)
    clone_path.mkdir(parents=True, exist_ok=True)


def get_student_team_id_from_org(org_name):

    teams_api_url =  f'{server_url}/api/v1/orgs/{org_name}/teams'
    response = requests.get(teams_api_url, headers=headers)

    # Check if the response status code is successful (2xx)
    if response.status_code // 100 != 2:
        # Print the error message if the response status code is not successful
        print('Error: {} Exiting.'.format(response.text))
        sys.exit(1)

    teams_json = json.loads(response.text)
    for team in teams_json:
        if team["name"] == team_name:
            team_id = team["id"]
            break

    return team_id


def get_students_from_team_id(team_id):

    team_members_api_url = f'{server_url}/api/v1/teams/{team_id}/members'
    response = requests.get(team_members_api_url, headers=headers)

    # Check if the response status code is successful (2xx)
    if response.status_code // 100 != 2:
        # Print the error message if the response status code is not successful
        print('Error getting students from team id: {} Exiting.'.format(response.text))
        sys.exit(1)

    members_json = json.loads(response.text)
    uid_list = [member['login'] for member in members_json]

    return uid_list



def clone_student_repo(git_url, student, student_repo_dir, cloned_repo_list):

    print(f'Cloning repo for student', student)
    try:
        # Clone into directory named by student onyen
        stdout = subprocess.run(['git', 'clone', git_url, student_repo_dir], check=True, capture_output=True, text=True).stdout
        cloned_repo_list.append(student)
        print(stdout)
        print(f'Successfully cloned {student} repo.')
    except subprocess.CalledProcessError as e:
        if e.output.startswith('error: {'):
            error = json.loads(e.output[7:]) # (skip "error: )"
            print(error['code'])
            print(error['message'])
    except OSError as e:
        if e.output.startswith('error: {'):
            error = json.loads(e.output[7:])
            print(error['code'])
            print(error['message'])
    except Exception as e:
        print(e)



def fetch_student_repo(git_url, student, student_repo_dir, fetched_repo_list):

    # NOTE: Can't specify a directory to put repo in as with git clone. So have to chdir to the repo to run git fetch
    #       or git pull. Even using a refspec with the directory you want as <dst> requires chdir to the repo first.
    #       So save and change back to currrent working directory post-pull

    print(f'Fetching repo for student', student)

    # Save current directory
    wd = os.getcwd()
    print(f'Current working directory: {wd}')

    try:
        os.chdir(student_repo_dir)
        print(f'Git fetch working dir for student {student}: {os.getcwd()}')
    except FileNotFoundError:
        print(f'Directory {student_repo_dir} does not exist')
    except NotADirectoryError:
        print(f'{student_repo_dir} is not a directory')
    except PermissionError:
        print(f'You do not have permissions to change to {student_repo_dir}')

    try:
        stdout = subprocess.run(['git', 'fetch', git_url], check=True, capture_output=True, text=True).stdout
        fetched_repo_list.append(student)
        print(stdout)
        print(f'Successfully cloned {student} repo.')
    except CalledProcessError as e:
        if e.output.startswith('error: {'):
            error = json.loads(e.output[7:]) # (skip "error: )"
            print(error['code'])
            print(error['message'])
    except OSError as e:
        if e.output.startswith('error: {'):
            error = json.loads(e.output[7:])
            print(error['code'])
            print(error['message'])
    except Exception as e:
        print(e)

    finally:
        # Change back to orignal working dir
        os.chdir(wd)
        print(f'Exiting fetch_student_repo with cwd set back to: {os.cwd()}')



def update_student_repos(student_list):

    # git clone or fetch each student's git repo
    cloned_repo_list = []
    fetched_repo_list = []
    for student in student_list:

        git_url = f'{server_url}/{student}/{course_dir}.git'
        student_repo_dir = f'/{student}'

        if not os.path.isdir(student_repo_dir):
            clone_student_repo(git_url, student, student_repo_dir, cloned_repo_list)
        else:
            fetch_student_repo(git_url, student, student_repo_dir, fetched_repo_list)

    # Check for and list any failures
    #if len(student_list) != len(cloned_repo_list) + len(fetched_repo_list):
    print(f'Student repos: {student_list}')
    print(f'Repos cloned : {cloned_repo_list}')
    print(f'Repos fetched: {fetched_repo_list}')
    updated_repo_list = cloned_repo_list + fetched_repo_list
    print(f'Repos updated: {updated_repo_list}')
    not_updated_set = set(student_list).difference(updated_repo_list)
    if len(not_updated_set) > 0:
        print(f'ERROR: The following repos failed to update: {not_updated_set}')
        return False

    return True

def main():

    current_dir = create_ottergrader_gitea_dirs()
    team_id = get_student_team_id_from_org(org_name)
    student_list = get_students_from_team_id(team_id)
    rc = update_student_repos(student_list)

if __name__ == '__main__':
    main()
