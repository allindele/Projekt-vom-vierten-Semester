'use strict'

class LogInView {
    constructor(element) {
        this.element = element;
        this.template = "login.tpl.html";

        this.requester = new Requester_cl();
    }
    renderView(data) {
        if (this.isUserLoggedIn()) {
            APP.instance.changeView("login.done");
            return;
        }

        let markup = APP.tm.renderTemplate(this.template, data);
        let el = document.querySelector(this.element);
        if (el != null) {
            el.innerHTML = markup;
        }

        this.configHandleEvent();
    }

    configHandleEvent() {
        let el = document.getElementById("doLogin");
        if (el != null) {
            el.addEventListener("click", (e) => {
                this.handleEvent(e, this);
            });
        }
    }

    handleEvent(event, that) {
        event.preventDefault();
        let path_s = "/login";
        let formData = document.forms["login-form"];
        let formJson = that.getFormDataAsJson(formData);

        that.requester.POST_px(path_s, JSON.parse(formJson)).then(result => {
            console.log('Success:', JSON.stringify(result));
            APP.instance.changeView("login.done", [null, null]);
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

    getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    userAuthenticated() {
        var cookie = this.getCookie("user");
        if (cookie == "" || cookie == undefined) {
            return false;
        }
        return true;
    }

    isUserLoggedIn(){
        return this.userAuthenticated();
    }
}