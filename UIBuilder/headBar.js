let HeadBarUI = function () {
    this.profilePicture = document.getElementById("profilePicture")
    this.notificationPicture = document.getElementById("sysNoitificationPng")
    this.userName = document.getElementById("profileName")
    this.setDetails()
    getProfileDetails(this)
}

HeadBarUI.defaults = {
    pPic : './Content/images/profile_pic.png',
    name : 'user name',
    mailPic : './Content/images/mail.png'
}

HeadBarUI.prototype.setDetails = function(){
    this.profilePicture.setAttribute("src", HeadBarUI.defaults.pPic)
    this.notificationPicture.setAttribute("src", HeadBarUI.defaults.mailPic)
    this.userName.textContent = HeadBarUI.defaults.name
}

getProfileDetails = function(obj) {
    const zerorpc = require("zerorpc")
    let client = new zerorpc.Client()
    client.connect("tcp://127.0.0.1:4244") // communicating with python via tcp://127.0.0.1:4242
    client.invoke("getProfileDetails", (error, res, more) => {
        if(error){
            console.log(error)
        }
        if(!more){
            console.log(res)
            obj.profilePicture.setAttribute("src", res['profilePicture'])
            obj.profilePicture.setAttribute("class", "rounded-circle")
            obj.userName.textContent = res['profileName']
            document.getElementById("profileSerial").innerHTML = "רשיון: " + "<small>" + res['serial'] + "</small>"
            document.getElementById("expired").innerHTML = "בתוקף עד: " + "<small>" + res['expired'] + "</small>"
            client.close()
        }
    })
}

