
# Google Calendar -> Toggl synchronizer

This piece of software is synchronizing events from google calendar to the toggl 


## Building from source
* Add google credentials file to data folder
* Run command below

```
pyinstaller --onefile --add-data='data/*:data' main.py
```
