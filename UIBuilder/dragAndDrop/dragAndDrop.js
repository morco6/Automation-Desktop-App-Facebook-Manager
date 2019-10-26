
let DragAndDropUI = function (div_id, btn_id, fileName) {
    this.modal = document.getElementById(div_id) //div id of dnd modal
    getBodyModal(this.modal,fileName)
    this.modalBtn = document.getElementById(btn_id)
    this.msg = ""
    
    this.modalBtn.addEventListener("click", () => {
        $('#dragNdropModal').modal('show')
        let holder = document.getElementById('drag-file')
        let showIMG = "<div class='row'>"

        holder.ondragover = () => { return false }
        holder.ondragleave = () => { return false }
        holder.ondragend = () => { return false }
        holder.ondrop = (e) => {
            alert.pop_msg(this.msg)
            e.preventDefault()

            for (let f of e.dataTransfer.files) {
                fileList.push(f.path)
                showIMG += "<div class='col'><img src=" + f.path + " style='max-width:100%; max-height:100%; height: auto;'></div>"
                console.log(f)
            }
            showIMG += "</div>"
            document.getElementById(btn_id + "-body").innerHTML = showIMG
            this.msg = "נבחרו " + fileList.length + " קבצים"
            alert.showAlert(this.msg)
            return false
        }
    })

    document.getElementById("clean").addEventListener("click", () => {
        fileList = []
        alert.pop_msg(this.msg)
        alert.hideAlert()
        document.getElementById(btn_id + "-body").innerHTML = '<h2 id="h2-dnd">גרור את הקובץ לתיבה זו</h2><br><h1 id="h1-dnd" style="color: #fff"><i class="fas fa-camera-retro"></i></h1>'
    })
}

getBodyModal = (modal, fileName) => {
    const fs = require('fs')
    let f = fs.readFileSync(fileName).toString("utf-8")
    modal.innerHTML = f
}

