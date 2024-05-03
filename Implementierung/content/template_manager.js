'use strict'

if (APP == undefined) {
    var APP = {};
}

class TemplateManager {
    constructor(){
        this.initialized = false;

        this.templates = {};
        this.compiled  = {};

        this.template_compiler = new TemplateEngine();
        this.requester = new Requester_cl();
    }

    initialize (successCallback, errorCallback) {
        // Templates als Ressource anfordern und speichern
        let requestPath = "/templates/";
        this.requester.GET_px(requestPath).then(result => {
            let data = JSON.parse(result);
            this.templates = data['templates'];

            this.initialized = true;
            console.log("templates.loaded");
            successCallback();
        });
    }

    renderTemplate(templateName, data) {
    var compiled = null;
    if (templateName in this.compiled) {
        compiled = this.compiled[templateName];
    } else {
        // Übersetzen und ausführen
        if (templateName in this.templates) {
            this.template_compiler.reset();
            compiled = this.template_compiler.compile(this.templates[templateName]);
            this.compiled[templateName] = compiled;
        }
    }
    if (compiled != null) {
        return compiled(data);
    } else {
        return null;
    }
    }
}

APP.instantiateTemplateManager = function(){
    APP.tm = new TemplateManager();
}