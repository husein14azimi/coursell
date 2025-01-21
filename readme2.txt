the university project:
	the account challenges:
		profile picture
	the course challenges:
		verifier for video files - tags
	the discount challenges:



the comment viewset smartly is decoupled from other apps and models. the comment viewset only applies the isauthenticated permission, which is a security bug/threat as unenrolled users can put comments on courses they are not enrolled in (which may be very small). plus, they can update the comments they didn't create.