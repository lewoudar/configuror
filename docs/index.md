# Configuror documentation

Everything you need to know about configuror.

## Why configuror?

While using [Flask](http://flask.pocoo.org/docs/1.0/), I realized that their Config class could be useful for any type
of project. And the utility became more and more obvious to me when I looked at a project like
[Ansible](https://docs.ansible.com/ansible/latest/index.html). If you look the 
[section](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)
where they define variables precedence, you will notice that there may be several locations for the configuration files,
and these configuration files can be written in different formats (json, yaml..).

What if there was a simple tool that would aggregate information from different sources in the order you wanted? This
is **why** the configuror project exists!

## Features
- The ability to add files of different types in the order you want.
- The ability to ignore non-existing files in the list you passed.
- The ability to load dotenv files to help you comply with the [12factor app](https://12factor.net/).
- The ability to handle the main configuration file formats: json, ini, yaml and toml.

## Contents
- [Installation](installation.md)
- [Usage](usage.md)
- [API](api.md)
- [Changelog](changelog.md)
