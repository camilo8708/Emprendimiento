app.controller("concursoController", function ($scope, $http, sessionService, ngTableParams, $log, $filter, $routeParams) {

    //Variable para consultar si el usuario está autenticado o está autorizado con los roles que se pasan como
    //parámetro
    $scope.session = {};
    $scope.session.authenticated = sessionService.isAuthenticated();
    $scope.session.authorized = sessionService.isAuthorized();
    $scope.allEncuesta = {};
    $scope.detailEncuesta ={};
    $scope.currentConcurso=0;
    $scope.mode = "Agregar";
    $scope.detalle = {};
    $scope.isActive = false;
    $scope.isAdmin = false;

    if($routeParams.page == undefined || $routeParams.page < 1){
        $routeParams.page = 1
    }

    $scope.url = $routeParams.url;

    if ($routeParams.url != undefined) {
        $http({method: "GET", url: "/encuesta/" + $routeParams.id, params: {idAdmin: sessionService.getUserId()}})
            .success(function (data, status) {
                $scope.detalle = data;

            }).error(function (data, status) {
            $log.error(data);
        });
    }



});



