If a GET request is successful, the `data` object passed to the template shall have `"success": 1`. Otherwise it will have `"success": 0`, and the error name will be present at the `"error"` key.

The following keys will also be present in the `data` object passed to other specific pages.

To the public user view:
```
{
    "uid":          user's ID number (int),
    "username":     user's username (string),
    "pfp":          access ID of the user's profile picture (string),
    "status":       user's status (string),
    "suspended":    whether or not user is suspended (0 or 1),
    "posts":        list of user's posts, as a dictionary with post IDs and titles ({'pid': int, 'title': string}),
    "friends":      list of friends, as pairs of user IDs and usernames ([(int, string)]),
}
```

To the post view:
```
{
    "pid":          ID of the post (int),
    "title":        title of the post (string),
    "timestamp":    timestamp of the post (string),
    "content":      content of the post (HTML string)
    "votes":        net up/downvotes of the post (int),
    "owner":        ID of the post author,
    "comments":     list of comments, which are dictionaries with the following structure:
    {
        "uid":          ID of the posting user (int),
        "username":     username of the posting user (string),
        "content":      content of the comment (string),
        "timestamp":    timestamp of the comment (string)
    }
}
```


```
uid
username
email
status
suspended
admin
posts
title
friends
images

```
