[![Build Status](https://travis-ci.org/appsembler/roles.svg?branch=develop)](https://travis-ci.org/appsembler/roles)

# Ansible Roles

The purpose of this repository is to collect general-purpose Ansible roles with a focus on sane defaults,
extensibility, and reusability.


## Getting started

Clone this repo:

    $ cd /path/to/extra/roles
    $ git clone git@github.com:appsembler/roles.git appsembler-roles

Add it to your `ansible.cfg`:

    [defaults]
    roles_path = /path/to/extra/roles/appsembler-roles


## Philosophy

Roles that live in this repo should be general enough to be reused across multiple applications. Please read the
[documentation on best practices][best-practices].


[best-practices]: https://github.com/appsembler/roles/tree/develop/docs/best-practices.md


## Testing

At the very least, you should run a syntax check locally:

    $ make syntax-check

The repo is configured to run some basic tests on TravisCI. It runs
them on Ubuntu 14.04 and 16.04 systems with different ansible
versions, just checking that the roles can be applied without errors
and that they are idempotent.

(TODO: document how to run these tests locally)
