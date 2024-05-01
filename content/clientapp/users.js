'use strict'

class UserView {
    constructor(element) {
        this.element = element;
        this.listTemplate = "userList.tpl.html";
        this.datailTemplate = "userDetail.tpl.html";

        // REST paths
        this.qsUsersPath = "/qsmitarbeiter/";
        this.devUsersPath = "/swentwickler/";

        this.requester = new Requester_cl();

        this.filterData = {filterField: 'role', filterValue: 'all'};
        this.prevElem = undefined;
    }
    getPathByRole(role){
        switch(role){
            case "qsuser":
                return this.qsUsersPath;
                break;
            case "developer":
                return this.devUsersPath;
                break;
            default:
                return this.devUsersPath;
                break;
        }
    }
    filterUsers(userData, filterData){
        let returnData = {};

        for (let key in userData) {
            if (userData.hasOwnProperty(key)) {
                let element = userData[key];
                if(filterData.filterField in element && element[filterData.filterField] == filterData.filterValue){
                    returnData[key] = element;
                }
            }
        }
        return returnData;
    }
    renderList(newFilterData) {
        if(newFilterData !== undefined){
            this.filterData = newFilterData;
        }
        let allUsers = null;

        this.requester.GET_px(this.qsUsersPath).then(result => {
            let qsUsers = JSON.parse(result);
            this.requester.GET_px(this.devUsersPath).then(result => {
                let devUsers = JSON.parse(result);
                
                allUsers = Object.assign({}, qsUsers, devUsers);

                if(this.filterData.filterValue == 'all'){
                    this.doRenderList(this.listTemplate, allUsers);
                }else{
                    let filteredData = this.filterUsers(allUsers, this.filterData);
                    this.doRenderList(this.listTemplate, filteredData);
                }
            })
        });
    }
    renderDetail(id, role) {
        // Daten anfordern
        let path = this.getPathByRole(role);

        if(id == undefined){
            path += "0";
        }else{
            path += id;
        }

        this.requester.GET_px(path).then(result => {
            let user = JSON.parse(result);
            this.doRenderDetail(this.datailTemplate, user);
        });
    }
    doRenderList (template, data) {
        if (this.doRender(template, data)) {
            this.initListView()
            this.configFilterEventHandler();

           this.configRowClickEventHandler();
           this.configSwitchSection();
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
    initListView(){
        let filterObject = document.getElementById("userRoleFilter");
        let selectedIndex = 0;
        for (let i = 0; i < filterObject.options.length; i++) {
            const element = filterObject.options[i];
            if(element.value == this.filterData.filterValue){
                selectedIndex = element.index;
            }
        }
        filterObject.selectedIndex = selectedIndex;
    }
    configFilterEventHandler(){
        let filterObject = document.getElementById("userRoleFilter");
        filterObject.addEventListener('change', (e) => {
            e.preventDefault();

            let select = e.target;
            let selectedIndex = select.options.selectedIndex;
            let filterValue = select.options[selectedIndex].value;

            this.filterData.filterValue = filterValue;

            APP.instance.changeView("app.cmd", ["users", this.filterData]);
        });
    }
    configFormButtonEvents() {
        let formButtons = document.querySelectorAll('form #buttonSection button');
        formButtons.forEach(element => {
            element.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleFormButtonEvent(e, this);
            });
        });
    }
    handleFormButtonEvent(event, that){
        event.preventDefault();
        let cmd = event.target.dataset.action;
        let publishMsg = "users." + cmd;

        if(cmd == "backToList"){
            APP.instance.changeView("app.cmd", ["users", null]);
        }

        let form = document.forms["user-form"];
        let jsonStr = that.getFormDataAsJson(form);
        let id = parseInt(JSON.parse(jsonStr)['id']);
        if(cmd == "save"){
            if (id == 0) {
                that.saveNewUser(jsonStr, that);
            }
            else{
                that.updateUser(id, jsonStr, that);
            }
        }
    }
    configRowClickEventHandler() {
        let table = document.getElementsByTagName('table')['userTable'];
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
    handleSwitchEvent(event, that) {
        let cmd = event.target.dataset.action;
        let publishMsg = "users." + cmd;
        let dataId = that.prevElem != undefined ? that.prevElem.id : 0;
        let role = that.prevElem != undefined ? that.prevElem.dataset.role : undefined;
        
        let data = {'id': dataId, 'role': role}
        
        switch (cmd) {
            case "new":
                APP.instance.changeView("app.cmd", [publishMsg, null]);
                break;
            case "detail":
                APP.instance.changeView("app.cmd", [publishMsg, data]);
                break;
            case "delete":
                that.deleteUser(data, that);
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
    saveNewUser (jsonData, that){
        let role = JSON.parse(jsonData)['role'];
        let path = this.getPathByRole(role);
        
        that.requester.POST_px(path, JSON.parse(jsonData)).then(result => {
            APP.instance.changeView("app.cmd", ["users", null]);
        });
    }
    updateUser (id, jsonData, that){
        let role = JSON.parse(jsonData)['role'];
        let path = this.getPathByRole(role);
        path += id;

        that.requester.PUT_px(path, JSON.parse(jsonData)).then(result => {
            APP.instance.changeView("app.cmd", ["users", null]);
        });
    }
    deleteUser (data, that){
        let path = that.getPathByRole(data.role) + data.id;

        that.requester.DELETE_px(path).then(result => {
            APP.instance.changeView("app.cmd", ["users", null]);
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