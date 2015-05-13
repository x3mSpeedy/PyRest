var app = app || {};

(function () {
    'use strict';

    // Job Model
    // ----------

    app.Job = Backbone.Model.extend ({


        // load data
        urlRoot: '/api/jobs/',

        // Default attributes
        defaults: {
            id: '',
            name: '',
            status: '',
            settings: {},
            user: {}
        },

        parse: function (response) {

        // detect broken link and return 'broken' model for view to show
            if (_.has (response, "scripts")) {
                this.scripts = new app.ScriptCollection (response.scripts, {parse: true});
                delete response.scripts;
            } else {
                this.scripts = new app.ScriptCollection ([], {parse: true});
            }
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.scripts = this.scripts ? this.scripts.toJSON () : [];
            return json;
        }
    });

    app.Script = Backbone.Model.extend ({
        defaults: {
            duration: '',
            id: '',
            result: '',
            timestamp: ''
        },

        parse: function (response) {
            if (_.has (response, "commands")) {
                this.commands = new app.CommandCollection (response.commands, {
                    parse: true
                });
                delete response.commands;
            }
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.commands = this.commands ? this.commands.toJSON () : [];
            return json;
        }
    });

    app.Command = Backbone.Model.extend ({
        defaults: {
            duration: '',
            output: '',
            error: '',
            source_code: ''
        },

        parse: function (response) {
            return response;
        },
        toJSON: function () {
            var json = _.clone (this.attributes);
            json.isComplex = (json.error ? json.error.length > 0 : false)  || (json.output ? json.output.length > 0 : false);
            return json;
        }
    });

    app.ScriptCollection = Backbone.Collection.extend ({
        model: app.Script
    });
    app.CommandCollection = Backbone.Collection.extend ({
        model: app.Command
    });
}) ();