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
    $scope.recomendacion = 5;
    $scope.text1 = "";
    $scope.text2 = "";

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

    $scope.selecion = function(value) {
        $scope.recomendacion = value;
    }

    $scope.ratingStates = [
        {stateOn: 'glyphicon-ok-sign', stateOff: 'glyphicon-ok-circle'},
        {stateOn: 'glyphicon-star', stateOff: 'glyphicon-star-empty'},
        {stateOn: 'glyphicon-heart', stateOff: 'glyphicon-ban-circle'},
        {stateOn: 'glyphicon-heart'},
        {stateOff: 'glyphicon-off'}
    ];

    $scope.nextStep = function() {
        if ($scope.dynamic < 10){
            $scope.dynamic = $scope.dynamic + 2.5;
            if ($("#Text1").val() != undefined) {
                $scope.text1 = $("#Text1").val();
            }
        }else if ($scope.dynamic==10) {
            if ($("#Text2").val() != undefined) {
                $scope.text2 = $("#Text2").val();
            }
            // Se guarda las respuestas
            var fd = new FormData();
            fd.append("idEncuesta", $scope.detalle.id);
            fd.append("preguntaRecomendacion", $scope.overStar);
            fd.append("preguntaExperiencia", $scope.recomendacion);
            fd.append("primerComentario", $scope.text1);
            fd.append("SegundoComentario", $scope.text2);

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
