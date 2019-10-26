PATH = SAVED_GROUP_LISTS_PATH
FORMAT = ".json"

document.getElementById("save").setAttribute("data-content", "<div style='padding-top:5px'><input id='nameToSave'; style='border: 1px solid grey;'; type='text'; required/><a href='#' style='font-weight: bold' onclick='save()'> שמור</a><br><small>*נא לבחור שם באנגלית</small><hr><a class='text-left' href='#' style='padding-right: 35%; color: red; font-weight: bold' onclick=document.getElementById('save').click();>X סגור</a></div>")

let save = () => {
    let fileName = document.getElementById("nameToSave").value
    checked = getChecked("save")
    if(checked.length == 0 || fileName=="")
        return false
    else{
        checked = JSON.stringify($('#table').bootstrapTable('getSelections'))
        fs.writeFileSync(PATH + fileName + FORMAT, checked, 'utf8')
        $('#table').bootstrapTable('getSelections')
        document.getElementById("save").click()
        setTimeout(() => {
            refreshTable()
        },3000)
    }
}

let open = () =>{
    let nameList = "<div style='padding-top:5px'><li><a href='#' style='font-weight: bold' onclick=load('./groupList.json')> הצג הכל</a></li><hr></div>"
    let listOfFileNames = []
    fs.readdirSync(PATH).forEach(file => {
        fname = file.match(/([^.]+)/)[0] //match all characters before ".".
        listOfFileNames.push(fname)
    })
    for(let i=0; i<listOfFileNames.length; i++)
        nameList += "<li id='li"+i+"'>"+ "<span class='row'><span class='col'>"+(i+1)+". " +"<a href='#' style='font-weight: bold' onclick=load('" + listOfFileNames[i] + "')> " + listOfFileNames[i] + "</a></span><span class='col text-left'><a href='#' onclick=del('" + listOfFileNames[i] + "') style='color:red'>מחק</a></span></span></li><hr>"
    nameList+= "<a class='text-left' href='#' style='padding-right: 35%; color: red; font-weight: bold' onclick=document.getElementById('open').click();>X סגור</a>"
    document.getElementById("open").setAttribute("data-content", nameList)
}
document.getElementById("open").addEventListener("click", open)// Do not to relocate!

let load = (lname) => {
    if(lname == "./groupList.json")
        path = MAIN_LIST_PATH
    else
        path = PATH +lname+ FORMAT
    document.getElementById("open").click()
    $('#table').bootstrapTable('refresh', {url: path})
}

let del = (lname) => {
    path = PATH +lname+ FORMAT
    fs.unlink(path, (err) => {
        if (err) {
          console.error(err)
          return
        }
        else
            document.getElementById("open").click()
    })
}

