

let AlertUI = function (id) {
    this.alert = document.getElementById(id)
    this.msg = document.createElement("span")
    this.msgList = ["x"]
    build(this)
    this.hideAlert()
    closeAlertListener(this)
}

/*build elements*/
build = (obj) => {
    obj.alert.classList = "alert alert-dark"
    obj.alert.setAttribute("role", "alert")
    obj.msg.id = "message-alert"
    obj.alert.appendChild(obj.msg)
}

AlertUI.prototype.showAlert = function (msg) {
    this.push_msg(msg)
    this.alert.hidden = false
}

AlertUI.prototype.hideAlert = function () {
    this.alert.hidden = true
}

/*add one more message to alert box*/
AlertUI.prototype.push_msg = function (msg) {
    this.msgList.push(msg)
    this.msg.innerText = this.msgList.join(' | ')
}

/*pop last message*/
AlertUI.prototype.pop_msg = function (msg) {
    if (this.msgList.length > 1) {
        this.msgList = this.msgList.filter(e => e !== msg)
        this.msg.innerText = this.msgList.join(' | ')
    }
}

closeAlertListener = function(obj){
    obj.alert.addEventListener("click",()=>{obj.hideAlert()})
}