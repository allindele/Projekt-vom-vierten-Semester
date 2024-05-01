'use strict'

class Projekte {
    constructor(element) {
        this.element = element;
        this.listTemplate = "projectList.tpl.html";
        this.datailTemplate = "projectDetail.tpl.html";
        this.database = "Item_db/"
        this.requester = new Requester_cl();

        this.prevElem = undefined;
    }

    renderList() {
        let path = "/projekt/";
        path += this.database;
        this.requester.GET_px(path).then( result =>{
            let data = JSON.parse(result);
            this.doRenderList(this.listTemplate, data);
        });
    }

    changeDatabase(ptr){
        this.database = ptr + "/"
    }

    renderDetail(id) {
        let path = "/projekt/";
        path+=this.database;
        if(id == undefined){
            path += "0";
        }else{
            path += id;
        }

        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderDetail(this.datailTemplate, data[0]);
        });
    }

    doRenderList (template, data) {
        if (this.doRender(template, data)) {
           this.configRowClickEventHandler();
           this.configSwitchSection();
           this.configDatabaseSection();
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
        let formButtons = document.querySelectorAll('form #buttonSection button');
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
        let publishMsg = "projects." + cmd;

        let form = document.forms["project-form"];
        let jsonStr = that.getFormDataAsJson(form);
        let id = parseInt(JSON.parse(jsonStr)['ID']);
        console.log(jsonStr)
        if(cmd == "save"){
            if (id == 0 || isNaN(id)) {
                that.saveNewProject(jsonStr, that);
            }
            else{
                that.updateProject(id, jsonStr, that);
            }
        }
        if(cmd == "backToList"){
            APP.instance.changeView("app.cmd", ["projects", null]);
        }
    }

    configRowClickEventHandler() {
        let table = document.getElementsByTagName('table')['projectTable'];
        if (table == undefined) {
            return;
        }
        
        for(var i = 1; i < table.rows.length; i++){
            var row = table.rows[i];
            row.addEventListener('click', (e) => {
                this.highlightRow(e, this);
            });;
        }
    }

    configSwitchSection(){
        let footerButtons = document.querySelectorAll('footer button')
        footerButtons.forEach(element => {
            element.addEventListener('click', (e) => {
                this.handleSwitchEvent(e, this);
            });
        }); 
    }

    configDatabaseSection(){
        let databaseButtons = document.querySelectorAll('.dropdown-content button')
        databaseButtons.forEach(element => {
            element.addEventListener('click', (e) => {
                this.handleSwitchEvent(e, e.target.outerText);
            });
        });
    }

    handleSwitchEvent(event, that) {
        let cmd = event.target.dataset.action;
        let publishMsg = "projects." + cmd;
        let dataId = that.prevElem != undefined ? that.prevElem.id : 0;

        switch (cmd) {
            case "new":
                APP.instance.changeView("app.cmd", [publishMsg, null]);
                break;
            case "detail":
                APP.instance.changeView("app.cmd", [publishMsg, dataId]);
                break;
            case "delete":
                that.deleteProject(dataId, that);
                break;
            case "database":
                this.database = that + "/";
                APP.instance.changeView("app.cmd", [publishMsg, null]);
               
                break;
            default:
                break;
        }
    }

    highlightRow(e, that){
        let currentRow = e.target.parentElement;
        
        if(that.prevElem != undefined){
            that.prevElem.classList.remove('selected');
        }
     
        if(currentRow == that.prevElem){
            that.prevElem.classList.remove('selected');
            that.prevElem = undefined;
        }
        else {
            currentRow.classList.add('selected');
            that.prevElem = e.target.parentElement;
        }
    }

    saveNewProject (jsonData, that){
        let path = "/projekt/"+this.database;
        
        that.requester.POST_px(path, JSON.parse(jsonData)).then(result =>{
            APP.instance.changeView("app.cmd", ["projects", null]);
        });
    }

    updateProject (id, jsonData, that){
        let path = "/projekt/"+this.database+id;

        that.requester.PUT_px(path, JSON.parse(jsonData)).then(result => {
            APP.instance.changeView("app.cmd", ["projects", null]);
        });
    }

    deleteProject (id, that){
        let path = "/projekt/"+this.database + id;

        that.requester.DELETE_px(path).then(result => {
            APP.instance.changeView("app.cmd", ["projects", null]);
        });
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