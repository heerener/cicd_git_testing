#!/usr/bin/env python
import json
import os
from uuid import uuid4

import requests
from git import Actor, Repo


def write_file():
    with open("modification.txt", "w") as fp:
        fp.write(str(uuid4()))


def commit_and_push(branch_name):
    repo = Repo(".")
    print("Adding remote")
    remote = repo.create_remote(
        "github",
        "https://heerener:${GITHUB_ACCESS_TOKEN}@github.com/heerener/cicd_git_testing",
    )
    print("Remote github added")

    existing_branches = [ref.name for ref in remote.refs]
    remote_ref_name = f"{remote.name}/{branch_name}"
    try:
        remote_ref = next(ref for ref in remote.refs if ref.name == remote_ref_name)
        print(f"{branch_name} already exists, checkout only")
        remote_ref.checkout()
    except StopIteration:
        print(f"{branch_name} does not exist yet - creating")
        repo.create_head(branch_name)
        print("Head created")
        new_branch = next(head for head in repo.heads if head.name == branch_name)
        print(f"New branch: {new_branch}")
        new_branch.checkout()
        print(f"{new_branch} checked out")

    print("Adding to index")
    repo.index.add("modification.txt")
    author = Actor("Erik", "erik.heeren@epfl.ch")
    print("Committing")
    repo.index.commit("Committing a change", author=author)
    print(
        f"Remotes: {(remote.name, [url for url in remote.urls]) for remote in repo.remotes}"
    )
    print("Pushing")
    result = remote.push(refspec=f"{branch_name}:{branch_name}")


def pull_request(branch_name):
    url = "https://github.com/repos/heerener/cicd_git_testing"
    session = requests.Session()
    session.headers = {
        "Authorization": f"token {os.environ['GITHUB_ACCESS_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    print("Getting pull requests")
    pulls = session.get(f"{url}/pulls")
    print(pulls)
    if not pulls:
        print("No pull requests - let's make one")
        data = {
            "title": "New releases",
            "body": "Bumper found new releases, here are the spack version bumps",
            "head": branch_name,
            "base": "initial-setup",
        }
        response = session.post(f"{url}/pulls", data=json.dumps(data))

        print("Pull request made")
        print(response)
        print(response.content)
        print(response.json())


def main():
    branch_name = "my_test_branch"
    write_file()
    # commit_and_push(branch_name)
    pull_request(branch_name)


if __name__ == "__main__":
    main()
