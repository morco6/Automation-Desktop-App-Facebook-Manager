/*
* Posting on facebook groups!
* EPOCHS --> pause after |EPOCHS| posts (default is 3)
* PAUSE_TIME --> the rest time of the robot, after |EPOCHS| (default is 15 minutes)
* 15 minutes = 60000milliseconds*15
*/

let countPostsPerEpoch = 0
let postOption = null
let on = false //while true - keep running posting process.

/**
 * A general function that takes the selected rows (checkbox)
 * and manipulate the content of each row to display the status/results.
 * Parameters:
 *      'selected': Current group name (by row). 
 *      In addition, if selected parameter is "save" - display appropriate message
 *      'spinner': If selected group start to process - display spinner (timer with percent).
 *      'mSeconds': Comes together with the spinner - the approximate time for the process.
 *      'link': If exist - process is complete and display a link to the post.
 *      If there is no parameters - the function will return an array with the selected rows. 
*/
let getChecked = (selected = null, spinner = false, mSeconds = null, link) => {
    let checked = document.getElementsByClassName("selected")
    to_send = []
    for (let i = 0, cell; cell = checked[i]; i++) {
        to_send[i] = checked[i].cells[2].innerHTML
        statusContent = checked[i].cells[3]
        if ((selected != null) && (to_send[i] == selected)) {
            if ((spinner == false) && (mSeconds == false) && (link == false)) {//process failed
                statusContent.innerHTML = '<small style="color: red;">נכשל</small>'
            }
            else if ((spinner != false) && (mSeconds != null)) {//process is in progress
                return timer(mSeconds + 8000, statusContent)
            }
            else {
                if (link != undefined) {//process complete and there is a link to post
                    statusContent.innerHTML = '<small style="color: green;">הסתיים <a href="' + link + '">(הצג)</a></small>'
                    return true
                }
                else {//process complete and link to post not found
                    statusContent.innerHTML = '<small style="color: red;">הסתיים</small>'
                    return false
                }
            }
        }
        else if (selected == "save") {//saved row
            return false
        }
        else if (statusContent.textContent == " ") {//process in queue
            statusContent.innerHTML = "<small>ממתין...</small>"
        }
    }
    return to_send
}

/*
 * Find the selected groups in the JSON file ('groupList.json')
 * and push them into JSON format to send to python running environment.
*/
parseToJson = () => {
    return new Promise((resolve, reject) => {
        checked = getChecked()
        let rdata = fs.readFileSync('Content/groupList.json')
        let jsn = JSON.parse(rdata)
        //console.log(jsn)
        arr = []
        for (let j = 0, c; c = checked[j]; j++) {
            for (let i = 0, obj; obj = jsn[i]; i++) {
                if (obj.name == checked[j]) {
                    arr.push(obj)
                }
            }
        }
        //arr = JSON.stringify(arr)
        resolve(arr)
    })
}


/*
 * Execute the posting process. 
 * Between each post process, there is 1-2 minutes of rest time.
 * Between each 5 posts, there is 15 minutes (PAUSE_TIME=15m) of rest time.
 * if postOption == 1 then will execute option1 else if 2 then option 2.
*/
run = () => {
    let x = 0
    on = true
    styleButtonBefore2()
    parseToJson().then((response) => {
        (function postAgain() { //recursive
            if (on == false) {
                console.log("stop:" + on)
                clearTimeout()
                return false
            }
            if (countPostsPerEpoch == EPOCHS) {
                countPostsPerEpoch = 0
                console.log("pause for " + HOW_MANY_MINUTES + " minutes")
                setTimeout(() => {
                    postAgain()
                }, PAUSE_TIME)
            }
            else if (x < response.length) {
                let randTime = getRandomInt(MIN_TIME_POST, MAX_TIME_POST)
                getChecked(toFind = response[x].name, spinner = true, randTime)
                setTimeout(() => {
                    console.log("Working on: " + response[x].name)
                    let url = response[x].url
                    client.invoke("post", url, fileList, (error, res, more) => {
                        if (error) {
                            console.log(error)
                            getChecked(response[x].name, false, false, false)//display failed
                            x++
                            postAgain()
                        }
                        if (!more) {
                            console.log(res)
                            linkToPost(response[x].name).then((res1) => {
                                if (res1 == true) {
                                    console.log("The group: " + response[x].name + " Done!")
                                    countPostsPerEpoch++
                                    x++
                                    postAgain()
                                }
                                else {
                                    console.log("The group: " + response[x].name + " link failed")
                                    postAgain()
                                }
                            })
                        }
                    })
                }, randTime)
            }
            else {
                clearTimeout()
                styleButtonAfter2()
            }
        }())
    },
        (error) => {
            console.log(error)
        })
}

/*
 * returns a random number between min(number) to max(number)
 * the returned number represent time in milliseconds. 
 */
getRandomInt = (min, max) => {
    min = Math.ceil(min)
    max = Math.floor(max)
    res = Math.floor(Math.random() * (max - min + 1)) + min
    return res * 1000
}

/**
 * percent progress that represent the random time
 * it will take to make a new post. 
 */
timer = (ms, statusContent) => {
    let unit = ms / 100
    let progress = 0
    frame = () => {
        if (progress >= 100)
            clearInterval(id)
        else {
            progress++
            statusContent.innerHTML = '<small style="color: blue;">' + progress * 1 + '%</small>'
        }
    }
    let id = setInterval(frame, unit)
}

/**
 * Get a url to the current post.
 * if done ("!more"), display the result.
 */
linkToPost = (name) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            client.invoke("linkToPost", (error, res, more) => {
                if (error) {
                    console.log(error)
                }
                console.log("link: " + res)
                if (!more) {
                    resolve(getChecked(name, false, null, res))
                }
            })
        }, 3000)//wait 3 seconds before catching the link
    })
}

//////////////////////////////////////////////////////////////////
////////////////////DOM Scripts for styling///////////////////////

/*Style the run button before click*/
styleButtonBefore2 = () => {
    document.getElementById("button-background2").hidden = true
    document.getElementById("button-background3").hidden = false
    document.getElementById("button-before2").hidden = true
    document.getElementById("small-spinner2").hidden = false
    $('.tooltip').not(this).hide()
}

/*style the run button after posting process has finished*/
styleButtonAfter2 = () => {
    on = false
    document.getElementById("button-before2").hidden = false
    document.getElementById("button-background2").hidden = false
    document.getElementById("button-background3").hidden = true
    document.getElementById("button-before2").textContent = "הפעל"
    document.getElementById("button-background2").disabled = false
    document.getElementById("small-spinner2").hidden = true
}

document.getElementById("button-background3").addEventListener("click", () => {
    styleButtonAfter2()
})