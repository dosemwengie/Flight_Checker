# Flight_Checker
Web application to check flight deals via skiplagged API


Workflow:

User logs into account and chooses flight criteria(origin,destination,target price,dates,etc.)
Criteria is inserted into the database
Periodically, a scheduled job is launched, to check skiplagged for any matching flights specified by the user.
If a match, insert into user's results and notify user via email. When user returns to the site, the matching flight(s) will be displayed in their homepage.


Miscellaneous scripts:

clean_up: remove flight criteria and results of past dates.
run_54: sends reminder to user when flights are 54 days out(optimal prices in many cases, but not always true)

![Login](https://github.com/dosemwengie/Flight_Checker/blob/master/img/login.png)
![Homepage](https://github.com/dosemwengie/Flight_Checker/blob/master/img/homepage.png)
