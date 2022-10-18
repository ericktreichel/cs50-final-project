# HOW TO CODE

### Video Demo: URL-here

#### Description:

I made this web application named 'How to Code' where users can create an account, post about anything they want to talk (about technology and software development I hope), and see posts made by other users. The web app was made using Python, Flask and SQLAlchemy in the backend and HTML, CSS and JS in the frontend.

I used many features of Flask to make the site smarter and more reliable, such as Flask Login and UserMixin for user control, WTForms for efficient and custom forms, bcyrpt for password encryption, flash for displaying custom messages when necessary, url_for to make the links more robust and Pillow to resize (and compact) pictures uploaded by users, etc.

I tried to follow a standard for organizing files, so I created a '/static' directory to store static files such as stylesheets, .js files and pictures, the latter being divided into folders according to the type (whether they are general site images or profile pictures). All 13 HTML files are in the 'templates' folder, one of which is the default layout for all pages, which is imported into all other pages. The same goes for the navbar, which is also in its own file and is imported into the layout.

A SQLAlchemy database called howtocode.db was created to store the tables, schemas and site data.
I decided to create a class for Users and another for Posts, so these classes will be instantiated each time a new user registers or a new post is made. Such classes are defined in a file called 'models.py'.
All forms in the app were also created as classes in a file called 'forms.py'. On pages where a form is necessary, an instance of that specific form will be created also inheriting from FlaskWTF's 'FlaskForm' class. Using WTForms allowed me to include some important validations for specific fields.

Much of the program's magic is in the 'routes.py' file. This is where the content to be rendered on each page is defined according to the type of access (GET or POST), where you check if the user is logged in or not, etc. It is in 'routes.py' that the intelligence of the code itself is. The file has 12 different routes, each one with its specific codes, such as the route to 'register()' that checks if the user filled in everything correctly when registering and also if that user or email was not used before; and also the route to 'login()' that checks if the data entered by the user matches the data in the database, among others. I have restricted access to several pages to only logged in users using Flask_Login's 'login_required' feature, to give users more privacy.

Just as a joke I decided to implement an API on the site, on the page 'fluffy.html', where at each access a public API is consulted and returns the image of a corgi. Also for fun I put on some pages images of some animals using laptops (acting as developers) that I created recently using the AI plataform DALL-E2. These images match the theme of the website/blog about technology and programming.

I thought about implementing the possibility for users to leave comments on posts, but I ended up not developing this because it would be a very similar logic to implementing the posts themselves, where I would just add a new class in the 'models.py' file that would relate an id of the user who comments with the id of the specific post, another class in 'forms.py' and then render the form in the HTML file. I also thought of implementing some more useful APIs in the app, such as checking whether the registered email is valid, for example, but APIs are usually paid or have some very large limitations in use; so let's leave the dog images anyway.

The flask app and its settings are all in the '**init**.py' file, which also includes the instances created for bcrypt, SQLAlchemy and login_manager.
The only file to be executed to run the program is called 'app.py', and this is the only purpose of this file: to import the 'app.py' from the '**init**.py' and run the program. With the exception of the 'app.py' file, all the other files are inside the 'trchl' directory, which works as a kind of Python Package because it has the '**init**.py' file inside it.
There is also the requirements.txt file which purpose is list all the dependencies from the project
That' it. This was How to Code. This was CS50.
