'use strict'

class krankmelder_cl{

    constructor(element) {
        this.element = element;
        this.krankmelder = "krankmeldung.tpl.html";
        this.krankmeldungList = "krankmeldungList.tpl.html";
        this.requester = new Requester_cl();
    }   
    
    renderDetail() {
        let path = "/krankmeldung/detail";
        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderDetail(this.krankmelder, data);
        });
    }
    renderList() {
        let path = "/krankmeldung/list";
        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderList(this.krankmeldungList, data);
        });
    }

    doRenderList (template, data) {
        if (this.doRender(template, data)) {
           this.configFormButtonEvents();
        }
    }

    doRenderDetail (template, data) {
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
        let id =0
        try{
            let id = parseInt(JSON.parse(jsonStr)['ID']);
        }
        catch{   
        }

        if(cmd == "reject"){
            this.requester.DELETE_px("krankmeldung/reject/"+event.target.id)
            this.renderList();

        }
        if(cmd == "send"){
            let form = document.forms["krankmeldung-form"];
            let jsonStr = that.getFormDataAsJson(form);
            this.requester.PUT_px("krankmeldung/create",jsonStr);
            //this.krankmelder.renderList();
        }
        if(cmd == "back"){
            //display navigation page
        }
    }

    getFormDataAsJson(form) {
        var obj = {};
        var elements = form.querySelectorAll("input, select, textarea");
        for (var i = 0; i < elements.length; ++i) {
            var element = elements[i];
            var name = element.name;
            var value = element.value;

            if (name) {
                obj[name] = value;
            }
        }
        return JSON.stringify(obj);
    }

}