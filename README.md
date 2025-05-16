# CANVAS2DOIST 

This is a work in progress.

##### CURRENT TODO: 
- Upgrade automation scripts
- Handle class selection startup more elegantly
- Better interface than going to the localhost:5000 address

Here's a fun little script that's just for you if you use Todoist to keep track of your assignments from Canvas! It uses Canvas API and Todoist API to sync your assignments from canvas into todoist.

#### How to Run
1. Once you pull in the repository, change the environment variables within the `.env` file. 
1.1 While you're at it, `cd class-selection` and run an `npm install` to install the packages required for the frontend.
##### Canvas API
To obtain Canvas API, navigate to your account settings and scroll over to 'Approved Integrations'. Click on 'New Access Token' to generate your canvas API key, and insert it into the `.env` file under `CANVAS_API_TOKEN`.
##### Todoist API
Open your todoist app, and click on your profile on the top left and navigate to settings. Within settings, click on 'Integrations'. Click on the tab titled 'Developer' and copy the API token. Insert this key into the `.env` file under `TODOIST_API_TOKEN`.
##### Canvas Base URL
Navigate to your university's canvas landing page, it will usually be of the structure `university.instructure.com`. For example, at the University of Cincinnati, it is `uc.instructure.com`. Find this base URL and insert it into the `.env` under `CANVAS_BASE_URL`.

2. Once you have all the keys inserted into the `.env` file, run the python script.
2.1 For the first time, I'd also recommend selecting courses first. Do this by running the react app by running `npm start` in `class-selection`.
2.2 Now, press the refresh list button and let it load up the classes.
2.3 Select which classes matter to you, and hit done.
3. Now, in your browser, navigate to `localhost:5000/sync-assignments` (or run the sweet automation scripts)
4. Voila! Watch your tasks flow into todoist.

##### Powershell Automation
Now if you want to go crazy and set up the powershell script to automate the script with an alias,

1. Open powershell
2. Enter `notepad $profile`
3. Paste the code from `powershell_profile.ps1` into your `$profile`
4. Boom! Now source your profile by running `. $profile` and you're all set! 

#### How to update class selection
Good news! I finally got around to actually making it more friendly, but still working on making it more elegant. However, here's how you can do it now:

1. If you're done with a semester, or want to change up the classes selected, you can use the same interface you used to select classes when setting up.
2. To do so, first `cd class-selection` and run `npm start`
3. Now, go to `localhost:3000`, select courses
4. Click done
5. Now, when you run `localhost:5000/sync-assignments` (or sweet automation script ;) ), you're chilling!

This is a jank solution to a problem I've been facing lately to solve my eternal laziness to fill in my todoist myself. This can and will be improved to have a better user experience, but I wanted to put this out there for anyone else facing the same issue. 

I am currently making it more user friendly, apologies for the shell-play.

If you are interested to contribute to this, feel free to contact me!