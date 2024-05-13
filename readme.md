## 1. About the project:
- This project is a big exercise for a Python course at my school.
- It is a web application that is built on the Flask framework. The app is a platform for students to create section classes and in each section class, students can create vocabularies for themselves and can practice through using flashcards or playing games.

## 2. Prerequisite:
- Python 3.10 or higher
- Flask
- With firebase: This project uses firestore to store data. You need to create a project on firebase and get the credentials to connect to the database. I have a image that shows how to get the credentials. You can see it in the folder `static/images/setup_project/how_to_get_private_key.png` 

## 3. Folder structure:
```
- app
    | - blueprints: contains all blueprints of the app
    |    | - auth: login, register,...
    |    | - home: home page
    |    | - section_class: CRUD of section_class
    |    | ....
    |    | - utils: contains all utilities of the app relevant to firebase, helpers
    | - layouts: contains all layouts which are used by templates
    |    | _layout.html
    |    | ...
    | - static
    |    | - css: contains all css files of every page
    |    | - js: contains all javascript files of every page
    |    | - images
    |    | - favicon
    |    | - libraries: jquery, bootstrap, etc.
```

## 4. How to run the app
1. Clone the project
2. Install all dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## 5. Temp
PVTB