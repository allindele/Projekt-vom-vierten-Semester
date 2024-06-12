'use strict'

class mainsite_cl{

    constructor(element) {
        this.element = element;
        this.requester = new Requester_cl();
    }   
    
    renderView() {
        let path = "/mainsite";
        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderView("main.tpl.html", data);
        });
    }

    doRenderView(template, data) {
        if (this.doRender(template, data)) {
           this.configFormButtonEvents();
        }
    }


    doRender(template, data){
        let markup = APP.tm.renderTemplate(template, data);
        let el = document.querySelector(this.element);
        if (el != null) {
           el.innerHTML = markup;
           return true;
        }
        return false;
    }

    configFormButtonEvents() {
        let formButtons = document.querySelectorAll('button');
        formButtons.forEach(element => {
            element.addEventListener('click', (e) => {
                this.handleFormButtonEvent(e, this);
                e.preventDefault();
            });
        });
    }

    handleFormButtonEvent(event, that){
        event.preventDefault();
        
        let cmd = event.target.dataset.action;

        if(cmd == "Einsatzplan"){
            APP.instance.changeView("app.cmd",["einsatzplan.list",0])

        }
        if(cmd == "Krankmeldungen"){
            APP.instance.changeView("app.cmd",["krankmeldung.list"])
            //this.krankmelder.renderList();
        }
        if(cmd == "Krankmelden"){
            APP.instance.changeView("app.cmd",["krankmeldung.create"])
            //display navigation page
        }
    }
}