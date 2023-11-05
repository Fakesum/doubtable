CONTINUE_SEARCH_POLL = true;
CONTINUE_SUMMARY_POLL = true;

setInterval(() => {
    if (CONTINUE_SEARCH_POLL){
        fetch("/pollsearch?id="+SESSION_ID).then(r => {return r.text()}).then(r => {
            r.split("--"+SESSION_ID+"--").forEach(elm => {
                if ((elm == "false") || (CONTINUE_SEARCH_POLL == false)){
                    CONTINUE_SEARCH_POLL = false;
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
                                try{document.querySelector(".spinner-box").remove()}catch{};
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
    };
    if (CONTINUE_SUMMARY_POLL){
        fetch("/pollsummary?id="+SESSION_ID)
            .then(r => {console.log(r);return r.text()})
            .then(summary => {
                if ((summary == "none") || summary == undefined){
                    return
                } else {
                    document.querySelector('.summary-container').textContent = summary;
                    CONTINUE_SUMMARY_POLL = false
                }
            })
    }
}, 1000)