
app.controller("registerController", function ($scope, $route, $routeParams, $location, $http, sessionService, $log) {

    $scope.addEmpresa = function () {
        var send = true;

        if ($scope.newEmpresa === undefined) {
            send = false;
            $scope.errorMessage = "Debe ingresar información en los campos requeridos.";
            $("#modal-error").modal("show");
        }

        else  if ($scope.newEmpresa.nombreEmpresa === undefined || $scope.newEmpresa.nombresEmpleado === undefined ||
            $scope.newEmpresa.apellidosEmpleado === undefined || $scope.newEmpresa.correoElectronico === undefined ||
            $scope.newEmpresa.telefonoEmpleado === undefined || $scope.newEmpresa.contrasenia === undefined ||
            $scope.newEmpresa.contraseniaCon === undefined || $scope.file == undefined) {
            send = false;
            $scope.errorMessage = "Debe ingresar información en todos los campos.";
            $("#modal-error").modal("show");
        }
        else if ($scope.validarEmail($scope.newEmpresa.correoElectronico) == 1) {
            $scope.errorMessage = "Ingrese un correo electrónico válido.";
            $("#modal-error").modal("show");
        }  else if ($scope.newEmpresa.contrasenia != $scope.newEmpresa.contraseniaCon ) {
            $scope.errorMessage = "Las constraseña no son iguales";
            $("#modal-error").modal("show");
        }
        else {
            var fd = new FormData();
            fd.append("nombreEmpresa", $scope.newEmpresa.nombreEmpresa);
            fd.append("nombres", $scope.newEmpresa.nombresEmpleado);
            fd.append("apellidos", $scope.newEmpresa.apellidosEmpleado);
            fd.append("correoElectronico", $scope.newEmpresa.correoElectronico);
            fd.append("telefono", $scope.newEmpresa.telefonoEmpleado);
            fd.append("contrasenia", $scope.newEmpresa.contrasenia);

            if ($scope.file != undefined) {
                fd.append("file", $scope.file);
            }

            $http.post("/empresas/", fd, {
                withCredentials: true,
                headers: {"Content-Type": undefined},
                transformRequest: angular.identity
            }).success(function () {
                window.location.href = "/login_view/";
            }).error(function (e) {
                $scope.errorMessage = e;
                $("#modal-error").modal("show");
            });
        }
    };


    $scope.validarEmail = function (email)  {
        expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if ( !expr.test(email) )
            return 1;
        return 0;
    }
});