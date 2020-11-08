# Genrex

Genrex generates matching strings to a given regular expressions.

### Usecases
- generate test data
- calculate the cardinality of a regular expression.

# Quickstart

## Requirements

- Pyhton 3.x

## Install

```
pip install genrex
```

## First Steps

```python
import genrex

emails = genrex.parse(r'(John|Jane)\.(Doe|Smith)@(gmail|outlook|protonmail)\.com')

print('random email address: ', emails.random())
print('first email address: ', emails[0])
print('number of email addresses: ', len(emails))

print('')
[print(email) for email in emails] #print all emails

```

Output:
```
random email address:  Jane.Doe@gmail.com
first email address:  John.Doe@gmail.com
number of email addresses:  12

John.Doe@gmail.com
Jane.Doe@gmail.com
John.Smith@gmail.com
Jane.Smith@gmail.com
John.Doe@outlook.com
Jane.Doe@outlook.com
John.Smith@outlook.com
Jane.Smith@outlook.com
John.Doe@protonmail.com
Jane.Doe@protonmail.com
John.Smith@protonmail.com
Jane.Smith@protonmail.com
```

# Features

### Supported Regular Expression Syntax

- [x] ```.```
- [x] ```*```
- [x] ```+```
- [x] ```?```
- [x] ```{m}```
- [x] ```{m,n}```
- [x] ```|``` - Branch
- [x] ```[...]``` - Set
- [x] ```(...)``` - Group
- [ ] ```\d```, ```\s```, ... - Categories

# TODO

- support re flags (e.g. [```re.ASCII```](https://docs.python.org/3/library/re.html#re.ASCII))

# Alternatives
| Package | License|
| ------- |:------:|
| [exrex](https://github.com/asciimoo/exrex) | AGPL-3.0 |
| [rstr](https://github.com/leapfrogonline/rstr) | BSD |