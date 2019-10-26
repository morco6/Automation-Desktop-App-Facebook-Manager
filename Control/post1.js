/*
* Posting on facebook groups!
* EPOCHS --> pause after |EPOCHS| posts (default is 3)
* PAUSE_TIME --> the rest time of the robot, after |EPOCHS| (default is 15 minutes)
* 15 minutes = 60000milliseconds*15
*/


let selections = [] //checked groups
let post_content = "" // content of post
let countPostsPerEpoch = 0 // a flag counter to count index of cycle.
let running_process_flag = false // tell if process is running or not. 
const $table = $('#table') //bootstrap table


/**
 * Event listener to click on main post button to open post modal. 
 */
document.getElementById("post-button").addEventListener("click", () => {
    
    $table.bootstrapTable('getSelections').forEach(element => {
        selections.push(element)
    })// loop that get the selected groups from the table group list.

    
    
    $('#post-modal').modal('show')// display post modal
})


/**
 * Event listener to click on post modal button to confirm the message content to post.
 */
document.getElementById("postID").addEventListener('click', () => {
    
    post_content = post_content = document.getElementById("post-box").value

})

const status_by_name = (name, status)=>{

    $table.children("tbody").find("tr").each(function() {
        
        let tst = $(this).get()
        if(tst[0].cells[2].innerText == name){
            tst[0].cells[3].innerHTML = change_status(status)
        }
      })

}

/**
 * Event listener to click on start posting button.
 */
document.getElementById("runPostBTN").addEventListener("click", () => {
    
    stop_btn_style() // change the style of run posting button to spinner animation.
    
    run().then(() => {
        finish_btn_style() // reset button style on finish.
    })

})

const change_status = (status, link = null)=>{
    switch (status) {
        
        case "wait":
            return '<small>ממתין...</small>'

        case "on":
            return '<small style="color: purple;">פועל</small>'
                
        case "success":
            return '<small style="color: green;">הסתיים <a href="' + link + '">(הצג)</a></small>'
            
        case "fail":
            return '<small style="color: red;">נכשל</small>'
    
    }
}


/*
 * Execute the posting process. 
 * Between each post process, there is 1-2 minutes of rest time.
 * Between each 5 posts, there is 15 minutes (PAUSE_TIME=15m) of rest time.
 */
const run = () => {

    $table.bootstrapTable('getSelections').forEach(element => {
        status_by_name(element.name, "wait")
    })

    running_process_flag = true
    let counter = 0 // count the amount of current completed groups
    
    return new Promise((resolve) => {
        
        (function postAgain() { //recursive function that loop each url from the array.
            
            if (running_process_flag == false) {//stop by user click (see event listener at EOF).
                clearTimeout()
                return false
            }

            if (countPostsPerEpoch == EPOCHS) {// pause the time by settings - per epoch.
                countPostsPerEpoch = 0
                console.log("pause for " + HOW_MANY_MINUTES + " minutes")
                setTimeout(postAgain(), PAUSE_TIME)
            }

            else if (counter < selections.length) {
                
                //random time between two posts
                let randTime = getRandomInt(MIN_TIME_POST, MAX_TIME_POST)
                
                status_by_name(selections[counter].name, "on")//display "in progress" status
                
                setTimeout(() => {
                    
                    //transfer url and fileList if exist files to upload
                    client.invoke("post", selections[counter].url, fileList, post_content, (error, res, more) => {
                        
                        if (error) {
                            status_by_name(selections[counter].name, "fail")//display "failed" status
                            console.log(error)
                            counter++
                            postAgain()
                        }

                        if (!more) {

                            console.log(res)
                            
                            linkToPost().then(async(result) => {// catch link to post.
                                
                                if (result != false) {
                                    await status_by_name(selections[counter].name, "success", result)
                                    countPostsPerEpoch++
                                    counter++
                                    postAgain()
                                }

                                else //link failed
                                    postAgain()
                                
                            })
                        }
                    })
                }, 5000)
            }

            else {
                clearTimeout()
                resolve(true)
            }

        }())
    })


}


/**
 * Get a url to the current post.
 * if done ("!more"), display the result.
 */
linkToPost = () => {
    
    return new Promise((resolve, reject) => {

        client.invoke("linkToPost", (error, res, more) => {

            console.log("link: " + res)

            if (error) {
                console.log(error)
                reject(false)
            }

            else if (!more)
                resolve(res)

        })
    }, 3000)//wait 3 seconds before catching the link

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


stop_btn_style = () => {

    document.getElementById("runPostBTN").hidden = true
    document.getElementById("stop_button").hidden = false
    document.getElementById("button-before2").hidden = true
    document.getElementById("small-spinner2").hidden = false
    $('.tooltip').not(this).hide()

}

finish_btn_style = () => {
    
    document.getElementById("button-before2").hidden = false
    document.getElementById("runPostBTN").hidden = false
    document.getElementById("stop_button").hidden = true
    document.getElementById("button-before2").textContent = "הפעל"
    document.getElementById("runPostBTN").disabled = false
    document.getElementById("small-spinner2").hidden = true

}

/**
 * Event listener for stop process button.
 */
document.getElementById("stop_button").addEventListener("click", () => {
    
    running_process_flag = false
    finish_btn_style()

})

/*open links externally by default*/
$(document).on('click', 'a[href^="https"]', function (event) {
    event.preventDefault()
    shell.openExternal(this.href)
})