class headerClass {

    constructor(element) {
        this.element = element;
        this.template = "header.tpl.html";
        this.requester = new Requester_cl();
        this.currCity  = ""
    }

    renderView(data){
        let markup = APP.tm.renderTemplate(this.template, data);
        let el = document.querySelector(this.element);
        if (el != null) {
            el.innerHTML = markup;
        }
        this.configSwitchSection();
    }
    renderData(extendedpath = ""){

    }

    configSwitchSection(){
        let footerButtons = document.querySelectorAll('button')
        footerButtons.forEach(element => {
            element.addEventListener('click', (e) => {
                this.handleSwitchEvent(e, this);
            });
        });
    }



    handleSwitchEvent(event,that) {
        let cmd = event.target.dataset.action;
        console.log(event.target)
        switch (cmd) {
            case "refresh":
                this.renderData()
                break;
            default:
                break;
        }
    }
}