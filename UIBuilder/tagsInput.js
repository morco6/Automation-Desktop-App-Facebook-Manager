

let TagsUI = function (options) {
    this.options = Object.assign(TagsUI.defaults, options)//user define
    this.original_input = document.getElementById(options.elementID)//user div element id
    this.tagList = []//list of all current tags
    this.div = document.createElement('div')//the parent div of tags
    this.input = document.createElement('input')//new input
    this.input.placeholder = "לדוגמא: דירות למכירה"
    buildUI(this)
    addEvents(this)
}
/*default configurations*/
TagsUI.defaults = {
    elementID: '',
    divClass: 'tags-input',
    tagClass: 'tag',
    max: null,
    duplicate: false
}

TagsUI.prototype.addTag = function (tagVal) {

    if (this.anyErrors(tagVal))
        return

    this.tagList.push(tagVal)
    let tagInput = this

    let tag = document.createElement('span')
    tag.className = this.options.tagClass

    let closeIcon = document.createElement('a')
    closeIcon.innerHTML = '&times; ' + tagVal
    closeIcon.addEventListener('click', function (e) {
        e.preventDefault()
        let tag = this.parentNode

        for (let i = 0; i < tagInput.div.childNodes.length; i++) {
            if (tagInput.div.childNodes[i] == tag)
                tagInput.deleteTag(tag, i)
        }
    })

    tag.appendChild(closeIcon)
    this.div.insertBefore(tag, this.input)
    this.original_input.value = this.tagList.join(',')

    return this
}

TagsUI.prototype.deleteTag = function (tag, i) {
    tag.remove()
    this.tagList.splice(i, 1)
    this.original_input.value = this.tagList.join(',')
    return this
}


TagsUI.prototype.anyErrors = function (string) {
    if (this.options.max != null && this.tagList.length >= this.options.max) {
        console.log('max tags limit reached')
        return true
    }

    if (!this.options.duplicate && this.tagList.indexOf(string) != -1) {
        console.log('duplicate found " ' + string + ' " ')
        return true
    }

    return false
}


TagsUI.prototype.pushText = function (tagList) {
    tagList.forEach(x => {
        this.addTag(x)
    })
    return this
}

TagsUI.prototype.getInputString = function () {
    return this.tagList.join(',')
}

// Private function to initialize the UI Elements
buildUI = (tags) => {
    tags.div.append(tags.input)
    tags.div.classList.add(tags.options.divClass)
    tags.original_input.setAttribute('hidden', 'true')
    tags.original_input.parentNode.insertBefore(tags.div, tags.original_input)
}

addEvents = (tags) => {
    tags.div.addEventListener('click', () => {
        tags.input.focus()
    })
    tags.input.addEventListener('keydown', (event) => {
        let str = tags.input.value.trim()
        if (event.keyCode === 13) {
            tags.input.placeholder = ""
            tags.input.value = ""
            if (str != "")
                tags.addTag(str)
        }
    })
}




//tagInput1.pushText(["דירות להשכרה","דירות בדרום"])
//console.log(tagInput1.getInputString())