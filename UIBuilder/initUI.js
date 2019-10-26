(() => {
    window.alert = new AlertUI("alert") //config system alert

    const headBar = new HeadBarUI() //set headBar details

    /* -load Html page into tab- */
    const getHtmlPage = function (div_id, path) {
        const fs = require('fs')
        let f = fs.readFileSync(path).toString("utf-8")
        document.getElementById(div_id).innerHTML = f
    }
    getHtmlPage('posts-body', GROUPS_PAGE_PATH)

    /* -modal builders- */
    const postModal = new ModalUI({
        id: 'post-modal',
        title: 'פרסום פוסט',
        bodyClass: 'modal-body-mor text-right',
        bodyFile: POST_MODAL_PATH,
        footerBtnLeft: 'אישור',
        footerBtnLeftId: 'postID',
        footerBtnRight: ' הוסף תמונה/וידאו',
        footerBtnRightId: 'dNd',
        footerBtnRighticon: '<i class="fas fa-photo-video"></i>'
    })
    
    const dragNdropModal = new DragAndDropUI("dragNdropModal", "dNd", DRAG_AND_DROP_MODAL_PATH)

    const joinModal = new ModalUI({
        id: 'join_modal',
        title: 'הצטרפות אוטומטית לקבוצות',
        bodyClass: 'modal-body text-right',
        bodyFile: JOIN_MODAL_PATH,
        footerBtnLeft: 'הפעל',
        footerBtnLeftId: 'play_group_join',
        footerBtnRight: ''
    })

    const tagInput1 = new TagsUI({
        elementID: 'group_by_text_input'
    })

    const instructionsModal = new ModalUI({
        id: 'instructionsModal',
        title: 'הוראות',
        bodyClass: 'modal-body text-right',
        bodyFile: INSTUCTION_MODAL_PATH,
        footerBtnLeft: 'הבנתי',
        footerBtnLeftId: 'instructionsModal-btn',
        footerBtnRight: ''
    })

})()

/*Listeners*/
document.getElementById("refreshTable").addEventListener("click", () => {
    $('#table').bootstrapTable('refresh')
})

/*
document.getElementById("post-button").addEventListener("click", () => {
    $('#post-modal').modal('show')
})*/

document.getElementById("instructionsBtn").addEventListener("click", () => {
    $('#instructionsModal').modal('show')
})

document.getElementById("join_button").addEventListener("click", ()=>{
    $('#join_modal').modal('show')   
})

/*bootstrap tooltip*/
$('[data-toggle="tooltip"]').tooltip()

/*bootstrap pop-over*/
$(document).ready(() => {
    $('[data-toggle="popover"]').popover()
})