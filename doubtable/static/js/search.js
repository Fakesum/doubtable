CONTINUE = true;
setInterval(() => {
    if (CONTINUE){
        fetch("/pollsearch?id="+SESSION_ID).then(r => {return r.text()}).then(r => {
            r.split("--"+SESSION_ID+"--").forEach(elm => {
                if ((elm == "false") || (CONTINUE == false)){
                    CONTINUE = false;
                    return;
                }else if (elm == "true"){
                    return;
                };
                
                document.querySelector(".results-container").innerHTML += elm;
            })
        });
    }
}, 1000)