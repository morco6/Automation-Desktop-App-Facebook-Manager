
let ModalUI = function (options) {
    this.options = Object.assign(ModalUI.defaults, options)//user define
    this.check()
    this.modal = document.getElementById(this.options.id)
    this.build()
}

/*default configurations*/
ModalUI.defaults = {
    id: null,
    title: 'title',
    bodyClass: 'modal-body text-right',
    bodyFile: '<div></div>',
    footerBtnLeft: 'title', footerBtnLeftId: '#', footerBtnLefticon: '',
    footerBtnRight: '', footerBtnRightId: '#', footerBtnRighticon: ''
}

ModalUI.prototype.check = function(){
    if (this.options.id == null)
        throw " Div ID not found!"
}

ModalUI.prototype.build = function(){
    /*create*/
    let a = document.createElement("div")
    let b = document.createElement("div")
    let close = document.createElement("div")
    let title = document.createElement("div")
    let body = document.createElement("div")
    let footer = document.createElement("div")
    /*config*/
    a.classList = "modal-dialog"
    b.classList = "modal-content"
    close.classList = "modal-close-area modal-close-df"
    close.innerHTML = '<a class="close" data-dismiss="modal" href="#" style="background-color: #fff; color:#0062cc"><i class="fa fa-close"></i>x</a>'
    title.classList = "header-color-modal bg-color-1"
    title.innerHTML = '<h4>' + this.options.title + '</h4>'
    body.style = 'color: #fff'
    body.classList = this.options.bodyClass
    body.id = this.options.id + 'Body'
    this.getBodyModal(body, this.options.bodyFile)
    footer.classList = "row modal-footer"

    let f = ''
    if (this.options.footerBtnRight != '') {
        f += '<div class="col"><button class="btn btn-primary"><div class="row"><span id="' + this.options.footerBtnRightId + '" href="#">' + this.options.footerBtnRighticon + this.options.footerBtnRight + '</span></div></button></div>'
    }
    f += '<div class="col text-left"><button data-dismiss="modal" class="btn btn-secondary"><div class="row"><span id="' + this.options.footerBtnLeftId + '" style="padding-left: 5px; padding-right: 5px;" onclick="">' + this.options.footerBtnLefticon + this.options.footerBtnLeft + '</span></div></button></div>'
    footer.innerHTML = f

    /*append*/
    b.appendChild(close)
    b.appendChild(title)
    b.appendChild(body)
    b.appendChild(footer)
    a.appendChild(b)

    this.modal.appendChild(a)
}

ModalUI.prototype.getBodyModal = function (body, fileName) {
    const fs = require('fs')
    let f = fs.readFileSync(fileName).toString("utf-8")
    body.innerHTML = f
}






