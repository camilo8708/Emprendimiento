/**
 * Created by Jorge on 08/03/2016.
 */
app.controller("exampleController", function ($scope, $route, $routeParams, $location, $http) {

    $scope.message = "hola";
    $scope.servicios = false;
    $scope.B1 = true;
    $scope.B2 = true;
    $scope.B3 = true;
    $scope.B4 = true;
    $scope.B5 = true;
    $scope.B0= true;

    var hi = function () {
        alert("hi");
    };

    $scope.setServicios = function (B) {
        if (B == 1){
            $scope.B1 = !$scope.B1;

        }else if (B == 2){
            $scope.B2 = !$scope.B2;
        }else if (B == 3){
            $scope.B3 = !$scope.B3;
        }else if (B == 4){
            $scope.B4 = !$scope.B4;
        }else if (B == 5){
            $scope.B5 = !$scope.B5;
        }else{}
        if(!$scope.B1 || !$scope.B2 || !$scope.B3 || !$scope.B4 || !$scope.B5)
            $scope.B0= false;
        else
            $scope.B0= true;
        return  true;
    };

    $scope.getServicios = function () {
        return $scope.servicios;
    };

});