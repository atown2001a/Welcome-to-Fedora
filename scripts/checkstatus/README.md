Check FAS user status.

## Configuration:
rename `myconfig.cfg.example` to `myconfig.cfg` and edit it accordingly (it contains your FAS credentials).

## Syntax:
`python3 check.py username days`

Where `username` is the FAS user to check and `days` is the number of days to check on datagrepper in order to
get a list of activities logged from the fedmsg bus.

## Results
The script output is as follow:
* Username
* Human name
* Last seen (date of last FAS login)
* Groups
** list of FAS group membership, status and approval date
** total number of groups the user is member of
* Activities in the last X days:
** a list of activity topics grabbed from datagrepper
** total number of activities
