app.controller("encuestaController", function ($scope, $http, sessionService, ngTableParams, $log, $filter, $routeParams) {

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
    $scope.rate = 7;
    $scope.max = 10;
    $scope.isReadonly = false;
    $scope.dynamic = 2.5;

    if($routeParams.page == undefined || $routeParams.page < 1){
        $routeParams.page = 1
    }

    $scope.url = $routeParams.url;

    if ($routeParams.url != undefined) {
        $http({method: "GET", url: "/encuesta/" +  $scope.url , params: {idAdmin: sessionService.getUserId()}})
            .success(function (data, status) {
                $scope.detalle = data[0];
            }).error(function (data, status) {
            $log.error(data);
        });
    }



    $scope.hoveringOver = function(value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };

    $scope.ratingStates = [
        {stateOn: 'glyphicon-ok-sign', stateOff: 'glyphicon-ok-circle'},
        {stateOn: 'glyphicon-star', stateOff: 'glyphicon-star-empty'},
        {stateOn: 'glyphicon-heart', stateOff: 'glyphicon-ban-circle'},
        {stateOn: 'glyphicon-heart'},
        {stateOff: 'glyphicon-off'}
    ];


    $scope.nextStep = function() {
        if($scope.dynamic<10)
            $scope.dynamic = $scope.dynamic + 2.5;
        else if ($scope.dynamic==10) {
            // Se guarda las respuestas
            var fd = new FormData();
            fd.append("idEncuesta", $scope.url);
            fd.append("preguntaRecomendacion", $scope.overStar);
            fd.append("preguntaExperiencia", "3");
            fd.append("primerComentario", "pregunta1");
            fd.append("SegundoComentario", "pregunta2");

            $http.post("/encuesta/", fd, {
                withCredentials: true,
                headers: {"Content-Type": undefined},
                transformRequest: angular.identity
            }).success(function () {
                $scope.detalle.estadoEncuesta = 'Finalizada';
            }).error(function (e) {
                $scope.errorMessage = e;
                $("#modal-error").modal("show");
            });
        }
        else{

        }

    };
});



