# Paidagogos Bot

Paidagogos is a Telegram bot for remote learning. It is recommended to use it in conjunction with a [Paidagogos Drawer](https://github.com/Macket/paidagogos_drawer), which provides the review interface for teachers.

There are two types of users: **teachers** and **students**. They can do the following things.

#### Teachers

- create classrooms and add students to them
- assign tasks in any format: text, photo, video, files or audio messages
- review submissions ([Paidagogos Drawer](https://github.com/Macket/paidagogos_drawer)), rate and comment them

#### Students

- get tasks from teachers
- send submissions to teachers
- get teachers reviews ([Paidagogos Drawer](https://github.com/Macket/paidagogos_drawer)) on their submissions as well as rates and comments

## Getting Started

Paidagogos bot requires Python 3.7 and packages specified in ```requirements.txt```.

You can install them with

```
pip install -r requirements.txt
```

Before you start Paidagogos it is necessary to create ```.env``` file:

```
touch .env
```

and fill in this file according to the example below:

```
DEBUG = True

BOT_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ADMIN_ID = XXXXXXXXXXX

DATABASE_URL = postgres://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

DB_NAME = paidagogos_db
DB_USER = user
DB_PASSWORD = XXXXXXXXXXX
DB_HOST = localhost

PROXY = https://XXX.XXX.XXX.XXX:XXXX

```

```DEBUG``` should be **False** in prod

```BOT_TOKEN``` is the token got from [BotFather](https://t.me/BotFather)

```ADMIN_ID``` is the telegram id of the admin

```DATABASE_URL``` is used to access the database in prod

```DB_NAME```, ```DB_USER```, ```DB_PASSWORD``` and  ```DB_HOST```  are used to access the database in dev

```PROXY``` is used if Telegram is blocked in your country (also uncomment appropriate code in ***bot.py***)


Then you can start Paidagogos bot with this command:

```
python app.py
```


## Use case

Let's see how [Karl Weierstrass](https://en.wikipedia.org/wiki/Karl_Weierstrass) could teach [Sofya Kovalevskaya](https://en.wikipedia.org/wiki/Sofya_Kovalevskaya) if they had this bot.

First of all, Karl should start the bot and create the classroom.

![1](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/1.png)

Then he invites Sofya.

![2](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/2.png)

And Sofya joins his classroom.

![3](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/3.png)

So Karl can see her in the students list now.

![4](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/4.png)

To create the new task for Sofya, Karl taps **Tasks** and sends the name of the task.

![5](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/5.png)

Then he sends the task itself.

![6](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/6.png)

And assigns it.

![7](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/7.png)

Let's return to Sofya and see that she got notified about the new task.

![8](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/8.png)

She can view it.

![9](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/9.png)

Send her solution in any format.

![10](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/10.png)

And submit for Karl's review

![11](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/11.png)

Karl can see now that he has submissions for review in the appropriate classroom task list.

![12](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/12.png)

He has 1 submission for review and 0 reviewed submissions.

![13](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/13.png)

So Karl starts to review Sofya's solution.

![14](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/14.png)

If Paidagogos Bot is used in conjunction with a [Paidagogos Drawer](https://github.com/Macket/paidagogos_drawer), Karl can tap **Review** and make notes for Sofya in WEB interface.

![demo](https://raw.githubusercontent.com/Macket/paidagogos_drawer/master/videos/readme/demo.gif)

As review is done Karl has the photo with his notes in the bot

![15](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/15.png)

Then he writes comments for Sofya and rates her.

![16](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/16.png)

After that Sofya get notified that her submission is reviewed and can see the result.

![17](https://raw.githubusercontent.com/Macket/paidagogos_bot/master/img/readme/17.png)
