/*
* Login script
* connecting to server and facebook
*/

const zerorpc = require("zerorpc")
const remote = require('electron').remote
const ipcRenderer = require('electron').ipcRenderer

let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4244") // communicating with python via tcp://127.0.0.1:4242

/*prevent submit refresh problem of submit*/
$("#lf").submit((e) => {
    e.preventDefault()
})

let loginForm = document.forms["loginF"]
let err1 = document.querySelector('#error1')
let err2 = document.querySelector('#error2')
let e1 = "התרחשה שגיאה - נסה שוב"
let e2 = "בדוק את חיבור האינטרנט שלך"

/*event listener for submit action*/
loginForm.addEventListener('submit', () => {
    
    if(loginForm["pass"].value && loginForm["serial"].value){
        
        $('#loadingModal').modal('show') // start loading animation  

        let details = JSON.stringify({"serial": loginForm["serial"].value, "password": loginForm["pass"].value}) // login form values                        

        client.invoke("serverLoginRequest", details, (error, res, more) => {
            if(error)
                errorModal(error, e1, e2)

            else if(res['status']==false)
                errorModal(error, res.err1, res.err2) // login to server failed

            else if(!more && res['status']==true){
                client.invoke("facebookLoginRequest", (error, res, more) => { 
                    [...document.getElementsByTagName("input")].forEach((x) => {x.value = ""})
                    if(error)
                        errorModal(error, e1, e2)

                    else if(!more && res['status']==true) // login success
                        nextP() //redirect to the main page of existing user
                    
                    else if(!more && res['status']==false)
                        errorModal(error, res.err1, res.err2) // login to facebook failed
                })
            }
        })
    }
})

errorModal = (error, e1, e2) => {
    $('#loadingModal').modal('hide') // end loading animation
    console.log(error)
    err1.textContent = e1
    err2.textContent = e2
    $('#InformationproModalftblack').modal('show')
}

closeApp = () =>{
    remote.getCurrentWindow().close()
}

/*redirect to the main page*/
nextP = () => {
    remote.getCurrentWindow().hide() // hide parent window
    ipcRenderer.sendSync('nextPage')
}
