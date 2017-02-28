/**
 * Created by Jorge on 08/03/2016.
 */
app.controller("exampleController", function ($scope, $route, $routeParams, $location, $http) {

    $scope.message = "hola";
    $scope.servicios = false;

    var hi = function () {
        alert("hi");
    };

    $scope.setServicios = function (modo) {
        $scope.servicios = modo;
        return $scope.servicios;
    };

    $scope.getServicios = function () {
        return $scope.servicios;
    };

});