# Leonard, the gatekeeper

Place Leonard in charge of your apartment key pad. When you punch in the code, Leonard will answer and let you in. You just have to text him ahead of time to let him know that you are coming.

This is a better way of dealing with current apartment door systems. The standard model is that a guest dials your code at the front door, you pick up, and then after a short conversation, you punch in 9 to let them in. This automates that process with a Twilio enabled server.

## Instructions:

### Setup:

1. Find Leonard a nice home on EC2, Rackspace, or Heroku. To run it, just run `python app.py` [1]
2. Set up a Twilio number. Point it at the running instance.
3. Configure Leonard with which numbers should be whitelisted.
4. Have your landlord connect your door code to Leonard

### Daily Use:

1. Text Leonard ahead of time and let him know you are on your way
2. Within 5 minutes, dial the door code.
3. Leonard will answer and let you in.

## Extras:

- If you aren't whitelisted, Leonard can still let you in if you text him the secret password.
- Leonard will foward unknown users to your phone, just like before.
- Party Mode: Leonard will let everyone in!
- Access Log so you can see who is coming and going

## Wouldn't it be nice if:

- There was a web admin interface
- There was an EC2 AMI in the community marketplace
- Verify that it is Twilio hitting the SMS endpoint and not just a random web request.

## Security:

So how secure is this? Let's just say the NSA shouldn't use this. Neither should Fort Knox.


[1]: Heroku Instructions
```
> heroku login
> heroku create
> git push heroku master
> heroku ps:scale web=1 #Since Heroku doesn't keep your 1 dyno warm, you might want to use 2.
```

