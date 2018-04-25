# The LetsEncrypt Role
This document serves as a lightweight note about the role and its maintenance.

## How to Use this Role with Open edX
This role is primarily used for Open edX deployments,
but is generic enough to be used for other Debian based 
systems that use Nginx.

This role is included in our deployment playbooks like
[`ficus_basic.yml`](https://github.com/appsembler/configuration/blob/appsembler/ficus/master/playbooks/appsemblerPlaybooks/ficus_basic.yml)
and 
[`ginkgo_enterprise.yml`](https://github.com/appsembler/configuration/blob/appsembler/ginkgo/master/playbooks/appsemblerPlaybooks/ginkgo_enterprise.yml).

So usually it will be run without intervention. However, in some cases we need to run this role only.
Below are few examples on how to use it.

**Note:** Run via `$ ax` instead of `$ ansible-playbook` for Appsembler deployments.

### Run the LetsEncrypt Role
To run all the tasks (except for renew tasks):

```
$ ansible-playbook --tags=letsencrypt ficus_basic.yml
```

### Manually Renew the Certs
When necessary, a manual renew can be done by adding the `letsencrypt:renew` tag.

```
$ ansible-playbook --tags=letsencrypt,letsencrypt:renew ficus_basic.yml
```

For a quicker run, the `letsencrypt:renew` tags can be used separately:

```
$ ansible-playbook --tags=letsencrypt:renew ficus_basic.yml
```

## Version Pinning for Certbot
Unlike `$ pip`, `$ apt-get` does not support versioning pretty well, so version pins will usually break
as the maintainers can (and usually do) remove the old packages from their debian package repositories.

That being said, having a missing dependency will make Ansible complain and that will make it clear for
the engineer who is deploying the server.

Once a version gone missing the LetsEncrypt playbook should be amended. 

Otherwise we're risking feature deprecation and having new functionality sneak in without
notice which probably what caused the multiple SSL renewals failures in late 2017 to early 2018.
