'use strict'

class Application {
    constructor() {
        this.sideBar = new SideBar("nav");
        this.loginView = new LogInView("main");
        this.projekteView = new Projekte("main");
        this.header = new headerClass("header")
        this.requester = new Requester_cl();
        this.krankmelder = new krankmelder_cl("main")
        this.einsatzplan = new einsatzplan_cl("main")
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
                this.header.renderData()

                this.requester.GET_px("/navbar").then(result => {
                    let data = JSON.parse(result);
                    this.sideBar.render(data);
                });

                let markup = APP.tm.renderTemplate("home.tpl.html", null);
                let el = document.querySelector("main");
                if (el != null) {
                    el.innerHTML = markup;
                }
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
                    case "projects":
                        this.projekteView.renderList();
                        break;

                    case "projects.new":
                        this.projekteView.renderDetail();
                        break;

                    case "projects.detail":
                        this.projekteView.renderDetail(data[1]);
                        break;
                    case "projects.database":
                        this.projekteView.renderList();
                        break;
                    
                    case "users":
                        this.userView.renderList();
                        break;
                    case "users.new":
                        this.userView.renderDetail();
                        break;
                    case "users.detail":
                        this.userView.renderDetail(data[1]['id'], data[1]['role']);
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
                        this.einsatzplan.renderDetail();
                        break;
                    default:
                        console.log("message \"" + data[0] + "\" unknown")
                }
                break;
        }
    }
}