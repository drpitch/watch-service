# watch-service
A Python3 tool to trigger custom notifications when input data matches user defined rules

## Overview

Input data is read line by line from standard input or a file if specifed. When a line matches any of the user defined rules, all notifiers are triggered.

Watch service is configured via settings.json file. The configuration file has two sections: **matchers** (where the rules are defined) and **notifiers** (actions to execute when any rule are met).

There are two types of matchers (**Sentence** and **RegExp**) and two types of notifiers (**Console** and **Mail**) available. Feel free to add new types you may need :-)

## Configuration

### Matchers

#### Sentence matcher
Matches when the specified text is found at input line as complete words.
```
{
  "type": "Sentence"
  "text": "The sentence you want to match"
}
```
####  RegExp matcher
Matches when the regular expression matches the input line.
```
{
  "type": "RegExp",
  "pattern": "The regexp pattern"
}
```

### Notifiers

#### Console notifier
Prints line content to standard output.
```
{
  "type": "Console"
}
```
#### Mail notifier
Sends line contents by email.
```
{
  "type": "Mail",
	"options": {
	  "host": "localhost",
	  "port": "25",
	  "provider": "SMTP" or "Dumper",
	  "from": "me@mail.com",
	  "to": "you@mail.com",
	  "subject": "New message from Watcher :-)"
}
```
Host and port are optional. Default values are "localhost" and "25", respectively.
Provider can be "SMTP" (to use a SMTP server) or "Dumper" (to dump the email to standard output, mainly used for debugging).

### Sample configuration file
```
{
	"matchers": [
		{
			"type": "Sentence",
			"text": "I see trees of green"
		},
		{
			"type": "RegExp",
			"pattern": "(hello|go(o)+dbye)"
		}
	],

	"notifiers": [
		{
			"type": "Console"
		},
		{
			"type": "Mail",
			"options": {
				"provider": "SMTP",
				"from": "me@mail.com",
				"to": "you@mail.com",
				"subject": "New message from Watcher :-)"
			}
		}
	]
}
```

## Running the program

```
Usage: python watcher.py [filename]

Example: tail -f /var/log/nginx/error.log | python watcher.py
```
