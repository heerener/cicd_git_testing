#!/usr/bin/env python

from uuid import uuid4

from git import Actor, Repo


def write_file():
    with open("modification.txt", "w") as fp:
        fp.write(str(uuid4))


def commit_and_push():
    repo = Repo(".")
    remote = repo.create_remote("github", "ssh://git@github.com/heerener/cicd_git_testing")
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
        new_branch = next(head for head in repo.heads if head.name == branch_name)
        new_branch.checkout()

    repo.index.add("modification.txt")
    author = Actor("Erik", "erik.heeren@epfl.ch")
    repo.index.commit("Committing a change", author=author)
    result = remote.push(refspec=f"branch_name:branch_name")
    print(result.summary)


def main():
    write_file()
    commit_and_push()


if __name__ == "__main__":
    main()
