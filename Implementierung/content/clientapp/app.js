'use strict'

class Application {
    constructor() {
        this.loginView = new LogInView("main");
        this.requester = new Requester_cl();
        this.krankmelder = new krankmelder_cl("main")
        this.einsatzplan = new einsatzplan_cl("main")
        this.mainsite = new mainsite_cl("main")
    }

    run(){
        APP.tm.initialize(()=>{
            if (APP.tm.initialized) {
                this.changeView("login");
            }
        }, ()=>{
            this.changeView("templates.failed")
        });
    }

    changeView(newView, data) {
        switch (newView) {
            case "templates.failed":
                alert("Vorlagen konnten nicht geladen werden.");
                break;

            case "login":
                this.loginView.renderView();
                break;

            case "login.done":
                this.changeView("app.cmd",["mainsite"])
                break;

            case "app.cmd":
                if (!this.loginView.isUserLoggedIn()) {
                    APP.instance.changeView("login", [null, null]);
                    return;
                }
               


                // hier müsste man überprüfen, ob der Inhalt gewechselt werden darf
                switch (data[0]) {
                    case "home":
                        let markup = APP.tm.renderTemplate("home.tpl.html", null);
                        let el = document.querySelector("main");
                        if (el != null) {
                            el.innerHTML = markup;
                        }
                        break;
                    case "krankmeldung.create":
                        this.krankmelder.renderDetail();
                        break;
                    case "krankmeldung.list":
                            this.krankmelder.renderList();
                            break;
                    case "einsatzplan.list":
                        this.einsatzplan.renderList();
                        break;
                    case "einsatzplan.detail":
                        this.einsatzplan.renderDetail(data[1]);
                        break;
                    case "mainsite":
                        this.mainsite.renderView()
                        break;
                    default:
                        console.log("message \"" + data[0] + "\" unknown")
                }
                break;
        }
    }
}