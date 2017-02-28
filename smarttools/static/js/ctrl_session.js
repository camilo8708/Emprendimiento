app.controller("ctrl_session", function ($scope, $http, $rootScope, sessionService) {

    //Variable para consultar si el usuario está autenticado o está autorizado con los roles que se pasan como
    //parámetro
    $scope.session = {};
    $scope.session.authenticated = sessionService.isAuthenticated();
    $scope.session.authorized = sessionService.isAuthorized();

    $scope.session.actualizar = function () {
        $scope.session.authenticated = sessionService.isAuthenticated();
    };



    $scope.session.isAuthorized = function (roles) {
        $scope.session.authorized = sessionService.isAuthorized(roles);
    };

    //Para sacar de sesión al usuario
    $scope.logout = {};

    $scope.logout = function () {
        $http({method: "GET", url: "login/c/" +  $rootScope.ip , params: {idAdmin: sessionService.getUserId()}})
            .success(function (res, status) {
                $scope.session.actualizar();
                window.location.href = "/login_view/";
            }).error(function (res, status) {
            $log.error(res);
        });

    };

    //Para inicio de sesión
    //$scope.login = {};

    $scope.login = function () {
        $scope.post_login();
    };

    $scope.post_login = function () {
        $http({
            method: "POST",
            url: "/post_login/",
            data: $scope.serialize($scope.login),
            headers: {'Content-Type': "application/x-www-form-urlencoded"}
        })
            .success(function (data, status) {
                $scope.session.actualizar();
                window.location.href = "/";
            }).error(function (data, status) {
            $scope.login = {};
            $("#modal-error").modal("show");
        });
    };

    $scope.serialize = function (obj) {
        var str = [];
        for (var p in obj) {
            if (obj.hasOwnProperty(p)) {
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            }
        }
        return str.join("&");
    };



});



