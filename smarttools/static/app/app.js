/**
 * Created by Jorge Runza
 */
var app = angular.module("smarttools", ["ngRoute", "ngTable", "ui.bootstrap"]).config(function ($routeProvider, $locationProvider, $httpProvider, $interpolateProvider) {


    /* Disable Cache */
    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
    }
    $httpProvider.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
    $httpProvider.defaults.headers.get["If-Modified-Since"] = "0";

    /* Change Tags */
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");

    /* Route Views */
    /* https://docs.angularjs.org/api/ngRoute/service/$route */
    $routeProvider

        .when("/inicio", {
            templateUrl: "/static/app/views/indexView.html",
            controller: "exampleController"
        })

        .when("/login_view", {
            templateUrl: "/static/app/views/logInView.html"
        })

        .when("/registro", {
            templateUrl: "/static/app/views/registerView.html",
            controller: "registerController"
        })

        .when("/lista_concurso", {
            templateUrl: "/static/app/views/queryConcursoView.html",
            controller: "concursoController"
        })

        .when("/cargue_clientes", {
            templateUrl: "/static/app/views/cargueClientes.html",
            controller: "cargueController"
        })

        .when("/concurso/:url/:page", {
            templateUrl: "/static/app/views/concursoView.html",
            controller: "concursoController"
        })

        .when("/concurso/:url", {
            templateUrl: "/static/app/views/concursoView.html",
            controller: "concursoController"
        })

        .when("/encuesta/:url", {
            templateUrl: "/static/app/views/encuestaView.html",
            controller: "encuestaController"
        })



        .otherwise({redirectTo: "/inicio"});
});

// Tomado del blog de Cheyne Wallace "Uploading To S3 With AngularJS", disponible en:
// http://www.cheynewallace.com/uploading-to-s3-with-angularjs/
app.directive("file", function () {
    return {
        restrict: "AE",
        scope: {
            file: "@"
        },
        link: function (scope, el, attrs) {
            el.bind("change", function (event) {
                var files = event.target.files;
                var file = files[0];
                scope.file = file;
                scope.$parent.file = file;
                scope.$apply();
            });
        }
    };
});

function sessionService() {

    this.isAuthenticated = function () {
        if (this.getUserId() == "" || this.getUserRole() == "") {
            return false;
        } else {
            return true;
        }
    }

    this.isAuthorized = function (rolesPermitidos) {
        //Roles validos: CONSUMIDOR, PRODUCTOR, ADMINISTRADOR
        if (this.isAuthenticated()) {
            if (angular.isArray(rolesPermitidos)) {
                if (rolesPermitidos.indexOf(this.getUserRole()) !== -1) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    this.getUserId = function () {
        var resp="";
        var ip ="";

        $.ajax({
            async: false,
            global: true,
            url: "login/g/",
            type: "GET",
            data: {},
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            beforeSend: function(){$.event.trigger('ajaxStart');},
            complete: function(){$.event.trigger('ajaxStop');},
            error:function() { },
            success: function(data){
                if(data !={}){
                    resp=data.id;
                    return resp;
                }
            }
        });

        return resp;
    }

    this.getUserRole = function () {
        var resp="";
        var ip ="";
        $.ajax({
            async: false,
            url: "login/g/",
            type: "GET",
            data: {},
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            error:function() { },
            success: function(data){
                if(data !={}){
                    resp=data.rol;
                    return resp;
                }
            }
        });

        return resp;
    }

    /*
     this.isUndefinedOrNull = function(val) {
     return !angular.isDefined(val) || val === null;
     }*/

    this.isJsonString = function (str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

}

sessionService();

app.service("sessionService", sessionService);