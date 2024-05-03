'use strict'

class TemplateEngine {
    constructor(){
        this.re = /<%(.+?)%>/g;
        this.reExp = /(^( )?(var|if|for|else|switch|case|break|continue|default|{|}|;))(.*)?/g;
        this.code = 'var r=[];\n';
        this.cursor = 0;
        this.result;
        this.match;
    }

    reset(){
        this.code = 'var r=[];\n';
        // this.result = "";
        // this.match = "";
    }

    add(line, js){
        if (js) {
            (this.code += line.match(this.reExp) ? line + '\n' : 'r.push(' + line + ');\n');
        } else {
            if (line != ''){
                this.code += 'r.push("' + line.replace(/"/g, '\\"') + '");\n';
            } else {
                this.code += '';
            }
        }
    }

    compile(html){
        let cursor = 0;
        let result;
        let match;

        while(match = this.re.exec(html)) {
            this.add(html.slice(cursor, match.index));
            this.add(match[1], true);
            cursor = match.index + match[0].length;
        }
        this.add(html.substr(cursor, html.length - cursor));
        this.code = (this.code + 'return r.join("");').replace(/[\r\t\n]/g, '');
        try {
            result = new Function('context', this.code);
            
        } catch(err) {
            console.log(this.code);
            console.error("'" + err.message + "'", " in \n\nCode:\n", this.code, "\n");
        }
        
        return result;
    }
}