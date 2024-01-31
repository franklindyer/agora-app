To the public user view:
```
{
    "uid":          user's ID number (int),
    "username":     user's username (string),
    "pfp":          access ID of the user's profile picture (string),
    "status":       user's status (string),
    "suspended":    whether or not user is suspended (0 or 1),
    "posts":        list of user's posts, as pairs of post IDs and titles ([(int, string)]),
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
