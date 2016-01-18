Venmo
=====

Pay or charge people on the command line!

```sh
venmo pay 19495551234 23.19 "Thanks for the beer <3"
venmo charge 19495551234 23.19 "That beer wasn't free!"
```

Installation
------------
`venmo` can be installed via `pip`.

```sh
pip install venmo
```

Authentication
--------------
`venmo` requires an access token to make requests on your behalf. The access
token is written to the file "/usr/local/var/venmo/ACCESS_TOKEN"
