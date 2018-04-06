# The LetsEncrypt Role
This document serves as a lightweight note about the role and its maintainance.


## Version Pinning for Certbot
Unlike `$ pip`, `$ apt-get` doesn't support versioning pretty well, so version pins will usually break
as the maintainers can (and usually do) remove the old packages from their debian package repositories.

That being said, having a missing dependency will make Ansible complain and that will make it clear for us.
We'll amend our playbook. Otherwise we're risking feature deprecation and having new funcitonality sneak in without
notice which probably what caused the multiple SSL renewals failures in late 2017 to early 2018.
