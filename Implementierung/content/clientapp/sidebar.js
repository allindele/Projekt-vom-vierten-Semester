'use strict'

class SideBar {
    constructor(element) {
        this.element = element;
        this.template = "sidebar.tpl.html";
        this.configHandleEvent();
    }
    render(data) {
        let markup = APP.tm.renderTemplate(this.template, data);
        let el = document.querySelector(this.element);
        if (el != null) {
            el.innerHTML = markup;
        }
    }

    configHandleEvent() {
        let el = document.querySelector(this.element);
        if (el != null) {
            el.addEventListener("click", this.handleEvent);
        }
    }


    handleEvent(event) {
        let cmd = event.target.dataset.action;
        APP.instance.changeView("app.cmd", [cmd, null]);
        
    }
}