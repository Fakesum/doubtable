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

                BREAK = false;

                const parser = new DOMParser();
                elm = parser.parseFromString(elm, "text/html").querySelector("#__rbox")

                document.querySelectorAll("#__rbox").forEach(
                    res => {
                        if (!BREAK){
                            if (parseInt(res.getAttribute("priority")) > parseInt(elm.getAttribute("priority"))){
                                res.parentElement.insertBefore(elm, res)
                                BREAK = true;
                            }
                        }
                    }
                );

                // This should only occur for the last element.
                if (!BREAK){
                    document.querySelector(".results-container").appendChild(elm)
                }
            })
        });
    }
}, 1000)