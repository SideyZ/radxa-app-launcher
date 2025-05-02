This is a Projekt about an App-Launcher for the radxa zero with DietPi. 
It is an Python3 App that runs on a xserver


To make your own apps for the launcher, you need to create a folder with the name of the app, inside that folder there has to be a start.sh script. In that script you can write everything else hat needs to happen for your app to start. 
Optionally you can add a icon.png file which will be used as your app icon.
If you want the app to run in the background, be minimized and be able to get the current instance back in the foreground, you need to add a window_class.txt file which the title of the app in your app folder
