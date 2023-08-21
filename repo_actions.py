#!/usr/bin/env python
import os
from uuid import uuid4

from git import Actor, Repo


def write_file():
    with open("modification.txt", "w") as fp:
        fp.write(str(uuid4))


def commit_and_push():
    print(f"Git SSH: {os.environ['GIT_SSH']}")
    print(str(os.path.exists(".ssh/deploy")))
    repo = Repo(".")
    print("Adding remote")
    remote = repo.create_remote(
        "github", "ssh://git@github.com/heerener/cicd_git_testing"
    )
    print("Remote github added")
    branch_name = "my_test_branch"

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
    print(f"Result: {result.summary}")


def main():
    write_file()
    commit_and_push()


if __name__ == "__main__":
    main()
