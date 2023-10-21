# TODO List

#### Description: 
This is app that will help you keep your tasks organized. It gives you the ability to login and add tasks. You will also be able to edit or delete the tasks that you created.

---
#### Background:
Being a procastinator myself, I usually forget the things that I am supposed to do and end up completely forgetting it or coming to know about it when it is already late. So I thought why not make a **TODO List** that will help me organize things a bit better and maybe also help me **remember** things.

And that's how I came with the idea for my final project of CS50. So my app, **TODO List**, is an app that will help you make a list of things that you have to do and help you remember them.

---
#### Features:
As this is a **TODO List** app, the main thing is going to be letting you add your tasks. Beside that, some other features are:
+ **Edting the TODOS:** Made a typo? No problem! You can always edit your task list.
+ **Account Creation:** You can create account in this app and you can access your task list from anywhere in the world. *(This feature is a little bit incomplete because the app is not on the Internet yet)*
+ **Account Deletion:** Don't want your account anymore? It can easily be deleted with just a few clicks.
+ **Easy-to-use:** The interface is also very simple and easy to understand. Anyone can easily use this app without any issues.

---
## How to use?
#### Getting the App ready
1. Since this app is based on Flask, you can run it by executing the following command in your terminal:

    `flask run`

    *(you can also run `python app.py`)*

    After that, you can click on the URL that shows up in your terminal.\
    *(Example: http://127.0.0.1:5000)*

#### Creating a new account
1. Once you open the link in your browser, you should be able to see the login page.
If you already have an account you can login. Else you can click on **Create a new account** to simply create a new account. You can then create a new account. You should now be redirected to the login page where you can login with your newly created account.

#### Adding, Editing and Deleting the tasks
1. After logging in, you should be redirected to the *`index`* page. This is the home page. You can add new tasks here by clicking the **`Add`** button. Clicking that button will redirect you to the *`add`* page. Here you can enter the new task and click the **`Add`** button at the bottom right to continue or **`Cancel`** button to cancel.

1. You can then see your tasks listed there. Each task will have a delete and edit button. *(**Delete** button is the one with the **trash** icon and **Edit** button is the one with **pencil** icon)* Clicking the delete icon will directly delete that task and clicking the edit button will take you to the *`edit`* page.

1. The *`edit`* page will have the task you had previously entered and you can now change that and click on the **`Save`** button at the bottom right side or click **`Cancel`** to cancel. You will not be redirected to the home page.

#### Navabar
1. At the left of the navbar, you can see the name of the app (**TODO List**). Clicking that will take you to the *`index`* or home page.

1. Just next to that, you can see the **About** button. You can go to the *`about`* page by clicking that button. In this page, you can see info about the page and just above that, you can also see a **`Go Back`** button that will take you to the *`index`* page.

1. Next to that, you can see your username with which you logged in.

1. Next to that, there is the **`Logout`** button. Clicking that will log you out immediately.

1. Then there is the last button which is the **settings** button represented with a **gear** icon. Clicking that will take you to the *`settings`* page.

#### Settings
1. In the settings page, you will see a **`Go Back`** button. Clicking that will simply take you one step behind (in this case, the *`index`* or the home page).

1. In the settings page, you will also be able to see a **`Change Password`** button. Clicking that will take you to the *`change`* page. You will also see the same **`Go Back`** button as the previous page and this will also work just as the previous one.

1. In the *`change`* page, you can change the current password for your account to a new one. For that, you will need to enter you current password, a new password and a confirmation password. After that you can click on the **Save** to change the password or you can click the **Cancel** button to just cancel.


