'use strict'

class einsatzplan_cl{

    constructor(element) {
        this.element = element;
        this.veranstaltundDetail = "veranstaltungDetail.tpl.html";
        this.krankmeldungList = "einsatzplan.tpl.html";
        this.requester = new Requester_cl();
        this.prevElem = undefined
    }   
    
    renderDetail(id) {
        let path = "/plan/detail/";
        if (parseInt(id)>0){
            path += id
        }
        else{
            path += 0
        }
        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderDetail(this.veranstaltundDetail, data);
        });
    }
    renderList() {
        let path = "/plan/list";
        this.requester.GET_px(path).then(result => {
            let data = JSON.parse(result);
            this.doRenderList(this.krankmeldungList, data);
            this.createTable(data)
        });
    }

    doRenderDetail (template, data) {
        if (this.doRender(template, data)) {
           this.configFormButtonEvents();
           this.onchangeTrigger();
        }
    }
    doRenderList (template, data) {
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

    onchangeTrigger(){
        document.getElementsByName("Ort")[0].addEventListener("change",this.dozentChange)
        document.getElementsByName("Von")[0].addEventListener("change",this.dozentChange)
        document.getElementsByName("Bis")[0].addEventListener("change",this.dozentChange)
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
            let form = document.forms["einsatplan-form"];
            let jsonStr = that.getFormDataAsJson(form);
            this.requester.PUT_px("plan/create/"+event.target.id,jsonStr);
            //this.krankmelder.renderList();
        }
        if(cmd == "back"){
            //display navigation page
        }
        if(cmd == "edit" && this.prevElem != undefined){
             APP.instance.changeView("app.cmd",["einsatzplan.detail",this.prevElem.id])
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
    createTable(data){
        let table = document.getElementById("einsatz")
        //

        this.rowData("Mo",data,table)
        this.rowData("Di",data,table)
        this.rowData("Mi",data,table)
        this.rowData("Do",data,table)
        this.rowData("Fr",data,table)
        //Dienstag
    }
    rowData(tag,data,table){
        let row = document.createElement("tr")
        let t = document.createElement("td")
        let time = 8
        t.innerHTML = tag
        row.append(t)
        for (var entry in data[tag]){
            time = 8
            for(var inhalt in data[tag][entry]){
                if(parseInt(inhalt) > time){
                    for(let i = time; i<inhalt;i++){
                        row.append(document.createElement("td"))
                    }
                }
                    t = document.createElement("td")
                    let dat = data[tag][entry][inhalt]
                    t.colSpan = data[tag][entry][inhalt]["Bis"] - inhalt
                    time = data[tag][entry][inhalt]["Bis"]
                    t.innerHTML = data[tag][entry][inhalt]["Type"]
                    t.id = dat["Vnr"]
                    t.addEventListener("click",(e)=>{
                        this.highlightRow(e,this)
                    })
                    row.append(t)
            }    
        for(let i = time;i<20;i++){
            row.append(document.createElement("td"))
        }
        
        table.append(row)
        row = document.createElement("tr")
        row.append(document.createElement("td"))
            
        }
        return row
    }

    dozentChange(){
        var start = document.getElementById("start");        
        let path = "plan/getPersonal/"
        path += document.getElementsByName("Von")[0].value+"/"
        path +=document.getElementsByName("Bis")[0].value+"/"
        path+=document.getElementsByName("Ort")[0].value
        APP.instance.requester.GET_px(path).then(result =>{
            let data = JSON.parse(result)
            let end = document.getElementById("userID")


            var length = end.options.length;
            for (let i = length-1; i >= 0; i--) {
            end.options[i] = null;
            }

            for (var key in data){
                var option = document.createElement("option");
                option.text = data[key]["Nachname"];
                end.add(option);
            } 

        })
    }

    highlightRow(e, that){
        let currentRow = e.target;
        
        if(that.prevElem != undefined){
            that.prevElem.classList.remove('selected');
        }
     
        if(currentRow == that.prevElem){
            that.prevElem.classList.remove('selected');
            that.prevElem = undefined;
        }
        else {
            currentRow.classList.add('selected');
            that.prevElem = e.target;
        }
    }
}