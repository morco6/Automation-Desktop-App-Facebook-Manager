(function(){
    let f = JSON.parse(fs.readFileSync(GROUP_CATEGORY_LIST_PATH, "UTF-8"))
    f.forEach(function(obj) {
        let opt = document.createElement("option");
        opt.text = obj.name
        opt.value = obj.url
        document.getElementById("options").appendChild(opt)
      })
}())

/*join to groups*/
const join_to_groups = () => {
    if(document.getElementById("by_category").checked){
        console.log("first")
        let opt = document.getElementById("options")
        let opt_name = opt.options[opt.selectedIndex].text
        let opt_val = opt.options[opt.selectedIndex].value
        console.log(opt_name, opt_val)
        start_join_to_groups(opt_val)
    }
    else if(document.getElementById("group_by_text").checked){
        console.log("second")
    }
}

let start_join_to_groups = (url) => {    
    client.invoke("init_groups_to_join", url, (error, res, more)=>{
        if(!more){
            (async function(){
                let result = await join()
                console.log("join: ", result)
            }())
        }
    })   
}

let join = async () =>{
    return new Promise(resolve => {
        
        let randTime = getRandomInt(MIN_TIME_GROUP,MAX_TIME_GROUP)
        
        setTimeout( () => {
            client.invoke("join_group", (error, res, more)=>{
                
                if(!more && res==false){//no more groups in page
                    clearTimeout()
                    resolve("no more groups")
                }
                
                else if(!more && res==true){
                    client.invoke("isForm", (error, res1, more1)=>{
                        
                        if(!more1 && res1==false){//no form to fill
                            (async function(){
                                await join(counter)
                            }())
                        }
                        
                        else if(!more1 && res1==true){
                            (async function(){
                                let result = await fillForm()
                                await join(counter)
                            }())
                        }
                    })
                }
            })
        },randTime)
    })
}

let fillForm=()=>{
    return new Promise(resolve => {
        client.invoke("fillForm", (error, res, more)=>{
            
            if(!more){//finish form
                resolve(res)//group details
            }
            
            else if(res==false){
                resolve("not finish fill")
            }
        })
    })
}

document.getElementById("play_group_join").addEventListener("click", ()=>{
    join_to_groups() 
})