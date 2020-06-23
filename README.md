# pymble: Bumble API for Python
Unofficial API for interacting with the dating app Bumble using Python
## How to use
```
import pymble

## start pymble session
s = pymble.Session("<phone number>", "<password>") # e.g. "4916299999999"
## return nearby users
users = s.get_users() 
## like all users
s.vote_all(user_ids=users.keys(), like=True)
## update location
s.update_location(lat=52.52, lon=13.4)
## update location by address (requires pygeo)
s.update_address('Berlin')
```
## Supported features
```
s.get_users() # returns dict of nearby users
s.vote(user_id, like) # like/reject user
s.vote_all(user_ids, like) # like/rejects list of users
s.update_location(lat,log) # set location
s.update_address(address) # update location using address (requires pygeo)
```

### Next steps
- Messaging
- Change profile details
- Multithreading