## Brewery Finder

This is an application that allows users to input their favorite Breweries.

The same user can add multiple breweries. 

They can also search up breweries and get information about them.

Finally, users can suggest breweries that aren’t currently in the database that they think should be added.


Routes

http://localhost:5000/ -> base.html —- Home Page

http://localhost:5000/addNew -> addNew.html —- Page for users to enter a name and brewery. On Submit, it brings the user to either brew.html or nonexist.html

http://localhost:5000/nonExist -> nonexist.html —- Page that appears when users enter a brewery that is not in the API. This page only appears if an invalid input is presented

http://localhost:5000/giveAdvice -> advice.html —- Page that allows users to enter a suggestion of a new brewery to add to the database/api. This page redirects back to itself upon successful entry. 

http://localhost:5000/showAll -> name.html —- Page outputs all user and brewery combinations as well as all suggestions.

http://localhost:5000/getBrew —> brew.html —- page that gives brewery info to user. Only appears when users submits brewery from addNew. If entered normally it redirects to addNew

error.html —- Shows error page (404) when an invalid url is given