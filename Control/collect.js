/////////////////////////////////////////////////////////////
////////////////////collecting process///////////////////////

/**
 * Calls to click_show_more method in the python running environment
 * every 3 seconds -> the python method clicking on a "show more"
 * button. When there is no more displaying "show more" button
 * -> go to collect()
 */
const initCollect = () => {
    styleButtonBefore1().then(
        (function clickShowMore(){ //clicking on "show more" button every 3sec
            setTimeout(() => {
                client.invoke("init_collect", (error, res, more) => {
                    if(error){
                        console.log(error)
                    }
                    if(res == false){
                        console.log(res.toString())
                        clickShowMore() //recursive
                    }
                    if(!more && res==true) {
                        console.log(res.toString())
                        clearTimeout()
                        collect()
                    }
                })
            }, 3000)
        })
    ) 
}

/**
 * Collect the groups list from the facebook page,
 * and exporting a json file with the data of each group.
 */
const collect = () =>{
    client.invoke("collect", (error, res, more) => {
        if(error){
            console.log(error)
            client.close()
            styleButtonAfter1(false)
            return false
        }
        else{
            console.log(res)
            if(res != undefined){
                let counter = document.querySelector('#counter')
                counter.textContent = ("נאספו: " + res)
            }
            if(!more) {
                let success = null
                client.invoke("exportJSON", (error) => {
                    if(error){
                        console.log(error)
                        success = false
                        console.log(success)
                        styleButtonAfter1(success)
                    }
                    else if(res==undefined){
                        console.log("exported Json")
                        success = true
                        console.log(success)
                        styleButtonAfter1(success)
                    }
                })
            }
        }
    })
}

/*Style the collect button after click*/
styleButtonBefore1 = async () => {
    document.getElementById("button-before").hidden = true
    document.getElementById("small-spinner").hidden = false
    let counter = document.querySelector('#counter')
    counter.textContent = ("מתכונן... אנא המתן")
    counter.hidden = false
    document.getElementById("button-background").disabled = true
    $('.tooltip').not(this).hide()
}

/*style the collect button after scan complete, and refresh the table content*/
styleButtonAfter1 = (success) => {
    console.log("Done.");
    $('#table').bootstrapTable('refresh')
    if(success)
        counter.textContent = ("הסתיים בהצלחה")
    else
        counter.textContent = ("לא נמצאו קבוצות")
    document.getElementById("small-spinner").hidden = true
    $('#table').bootstrapTable('refresh')
}

document.getElementById("button-background").addEventListener("click", ()=>{
    initCollect()
})