
/*communicate with python*/
let shell = require('electron').shell;
const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4244") // communicating with python via tcp://127.0.0.1:4242

/*requires*/
const fs = require('fs')

/*open links externally by default*/
$(document).on('click', 'a[href^="https"]', function (event) {
    event.preventDefault()
    shell.openExternal(this.href)
})

/*json files*/
MAIN_LIST_PATH = 'Content/groupList.json'
GROUP_CATEGORY_LIST_PATH = 'Content/groupsCategory.json'
SAVED_GROUP_LISTS_PATH = 'Content/saved/'

/*html files*/
//modals
POST_MODAL_PATH = 'UIBuilder/modals/postModal.html'
DRAG_AND_DROP_MODAL_PATH = 'UIBuilder/dragAndDrop/dragAndDropModal.html'
JOIN_MODAL_PATH = 'UIBuilder/modals/joinModal.html'
INSTUCTION_MODAL_PATH = 'UIBuilder/modals/instructionsModal.html'
//pages
GROUPS_PAGE_PATH = 'UIBuilder/pages/groups.html'

/*settings for group join*/
MIN_TIME_GROUP = 30 //minimum seconds between two posts (default  = 90)
MAX_TIME_GROUP = 60 //maximum seconds between two posts (default  = 180)

/*settings for posting on groups*/
MIN_TIME_POST = 90 //minimum seconds between two posts (default  = 90)
MAX_TIME_POST = 180 //maximum seconds between two posts (default  = 180)
EPOCHS = 5 // default = 6
ONE_MINUTE = 60000 //60000ms = 60sec
HOW_MANY_MINUTES = 10 //default = 15
PAUSE_TIME = ONE_MINUTE*HOW_MANY_MINUTES

var fileList = [] //list of files in drag&drop