import instaloader

# Create an instance of instaloader
insta = instaloader.Instaloader()

# Get the post by its shortcode
post = instaloader.Post.from_shortcode(insta.context, 'CqPYQHpODb7')

# Print the comments
for comment in post.get_comments():
    print(comment.text)