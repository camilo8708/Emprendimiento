app.controller("concursoController", function ($scope, $http, sessionService, ngTableParams, $log, $filter, $routeParams) {

    //Variable para consultar si el usuario está autenticado o está autorizado con los roles que se pasan como
    //parámetro
    $scope.session = {};
    $scope.session.authenticated = sessionService.isAuthenticated();
    $scope.session.authorized = sessionService.isAuthorized();
    $scope.allConcursos = {};
    $scope.detailConcurso={};
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
        $http({method: "GET", url: "/concurso/" + $routeParams.url, params: {idAdmin: sessionService.getUserId()}})
            .success(function (data, status) {
                var hoy = new Date();
                var inicio = new Date(data.fechaInicio);
                var fin = new Date(data.fechaFin);
                if (inicio <= hoy && fin >= hoy) {
                    $scope.isActive = true;
                }
                $scope.videos = data.videos;
                $scope.detalle = data;
                $scope.detalle.fechaInicio = $scope.detalle.fechaInicio.substring(0, 10)
                $scope.detalle.fechaFin = $scope.detalle.fechaFin.substring(0, 10)
                $scope.isAdmin = data.isAdmin;
                $scope.tableVideos = new ngTableParams(
                    {page: 1, count: 50},
                    {
                        total: $scope.videos.length,
                        getData: function ($defer, params) {
                            $defer.resolve($scope.videos.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                            setTimeout(function () {
                                $scope.cargarJwVideo();
                                if ($scope.isAdmin) {
                                    $scope.cargarJwVideoOrig();
                                }
                            }, 0);

                        }
                    }
                );

            }).error(function (data, status) {
            $log.error(data);
        });
    }


    $scope.cargarJwVideo = function () {
        for (i = 0; i < $scope.videos.length; i++) {
            if ($scope.videos[i].estado == 'Convertido') {
                jwplayer("video" + $scope.videos[i].id).setup({
                    file: $scope.videos[i].videoMP4,
                    width: "250px",
                    height: "200px"
                });
            }
        }
    }

    $scope.cargarJwVideoOrig = function () {
        for (i = 0; i < $scope.videos.length; i++) {
            var videoOriginal = $scope.videos[i].video.replace("%3A",":");
            jwplayer("videoOrig"+$scope.videos[i].id).setup({
                file: videoOriginal,
                width: "250px",
                height: "200px"
            });
        }
    }

    $scope.abrirModalCargarVideo = function () {
        $http({method: "GET", url: "/form/concurso/"})
            .success(function (data, status) {
                $("#form_wrapper").html(data.form);
            }).error(function (data, status) {
            //$scope.service = {};
        });

        $("#modalCargarVideo").modal();
    };

    $scope.guardarVideo = function () {
        var send = true;

        if ($scope.newVideo === undefined) {
            send = false;
            $scope.errorMessage = "Debe ingresar información en todos los campos.";
            $("#modal-error").modal("show");
        }

        else {
            if ($scope.newVideo.nombres === undefined || $scope.newVideo.apellidos === undefined
                || $scope.newVideo.correoElectronico === undefined || $scope.newVideo.desc === undefined  || $scope.file == undefined) {
                send = false;
                $scope.errorMessage = "Debe ingresar información en todos los campos.";
                $("#modal-error").modal("show");
            }

        }

        if (send) {
            var fd = new FormData();

            fd.append("nombres", $scope.newVideo.nombres);
            fd.append("apellidos", $scope.newVideo.apellidos);
            fd.append("correoElectronico", $scope.newVideo.correoElectronico);
            fd.append("desc", $scope.newVideo.desc);
            fd.append("file", $scope.file);
            $("body").css("cursor", "progress");
            $http.post("/concurso/"+$routeParams.url+"/", fd, {
                withCredentials: true,
                headers: {"Content-Type": undefined},
                transformRequest: angular.identity
            }).success(function () {
                $("body").css("cursor", "default");
                $("#modalCargarVideo").modal('hide');
                $("#modal-confir").modal('show');
            }).error(function (e) {
                $("body").css("cursor", "default");
                $("#modal-error").modal("show");
            });
        }
    };

    $scope.queryAllConcursos = function () {
        var idEmpresa =sessionService.getUserId();

        $http({method: "GET", url: "/concursos/" + sessionService.getUserId()})
            .success(function (res, status) {
                $scope.allConcursos= res;

                $scope.tableConcursos = new ngTableParams(
                    {page: 1, count: 3},
                    {
                        total: $scope.allConcursos.length,
                        getData: function ($defer, params) {

                            $defer.resolve($scope.allConcursos.slice((params.page() - 1) * params.count(), params.page() * params.count()));

                        }
                    }
                );

            }).error(function (res, status) {
            $scope.allConcursos = {};
            $log.error(res);
        })
    };




    $scope.addEditConcurso = function () {
        var send = true;

        if ($scope.newConcurso === undefined) {
            send = false;
            $scope.errorMessage = "Debe ingresar información en todos los campos.";
            $("#modal-error").modal("show");
        }

        else {
            if ($scope.newConcurso.nombre === undefined || $scope.newConcurso.url === undefined
                || $scope.newConcurso.fechaInicio === undefined || $scope.newConcurso.fechaFin === undefined
                || $scope.newConcurso.descripcion === undefined) {
                send = false;
                $scope.errorMessage = "Debe ingresar información en todos los campos.";
                $("#modal-error").modal("show");
            }

            if ($scope.mode === "Agregar") {
                if ($scope.file == undefined) {
                    send = false;
                    $scope.errorMessage = "Debe ingresar información en todos los campos."
                    $("#modal-error").modal("show");
                }
            }

            f1 = $scope.newConcurso.fechaInicio.getFullYear() + "-" + ($scope.newConcurso.fechaInicio.getMonth() + 1) + "-" + $scope.newConcurso.fechaInicio.getDate();
            f2 = $scope.newConcurso.fechaFin.getFullYear() + "-" + ($scope.newConcurso.fechaFin.getMonth() + 1) + "-" + $scope.newConcurso.fechaFin.getDate();

            var d1 = new Date(f1);
            var d2 = new Date(f2);

            if (d1>d2) {
                send = false;
                $scope.errorMessage = "La fecha inicio no puede ser superior a la fecha de fin."
                $("#modal-error").modal("show");
            }

        }


        if (send) {
            var fd = new FormData();

            if ($scope.mode === "Agregar") {

                fd.append("nombre", $scope.newConcurso.nombre);
                fd.append("url", $scope.newConcurso.url);



                fd.append("fechaInicio", f1);
                fd.append("fechaFin", f2);
                fd.append("descripcion", $scope.newConcurso.descripcion);
                fd.append("idEmpresa", sessionService.getUserId());

                fd.append("file", $scope.file);
                $("body").css("cursor", "progress");
                $http.post("/concursos/", fd, {
                    withCredentials: true,
                    headers: {"Content-Type": undefined},
                    transformRequest: angular.identity
                }).success(function () {
                    $("body").css("cursor", "default");
                    $scope.queryAllConcursos();
                    $("#modal-add").modal("hide");
                }).error(function (e) {
                    $("body").css("cursor", "default");
                    $scope.errorMessage = e;
                    $("#modal-error").modal("show");
                });
            } else {

                fd.append("id", $scope.currentConcurso);
                fd.append("nombre", $scope.newConcurso.nombre);
                fd.append("url", $scope.newConcurso.url);


                fd.append("fechaInicio", f1);
                fd.append("fechaFin", f2);
                fd.append("descripcion", $scope.newConcurso.descripcion);
                fd.append("idEmpresa", sessionService.getUserId());
                fd.append("file", $scope.file);
                $("body").css("cursor", "progress");
                $http.post( "/concursos/u/", fd, {
                    withCredentials: true,
                    headers: {"Content-Type": undefined},
                    transformRequest: angular.identity
                }).success(function () {
                    $("body").css("cursor", "default");
                    $scope.queryAllConcursos();
                    $("#modal-add").modal("hide");
                }).error(function (e) {
                    $("body").css("cursor", "default");
                    $scope.errorMessage = e;
                    $("#modal-error").modal("show");
                });


            }

        }
    };


    $scope.allowConcursoDelete = function (id) {
        $scope.concursoDeleteID = id;
    };


    $scope.deleteConcursoById = function () {
        if ($scope.concursoDeleteID != null) {
            $http({method: "DELETE", url: "/concursos/util/" + $scope.concursoDeleteID})
                .success(function (data, status) {
                    $("#modal-delete").modal("hide");
                    $scope.queryAllConcursos();
                }).error(function (data, status) {
                $log.error(data);
            })
        }
    };


    $scope.getEditConcurso = function (id) {
        $scope.currentConcurso = id;
        $scope.mode = "Actualizar";

        $http({method: "GET", url: "/concursos/util/" + id})
            .success(function (res, status) {
                $scope.newConcurso = res;
                $scope.newConcurso.nombre=res.nombre;
                $scope.newConcurso.url=res.url;
                $scope.newConcurso.fechaInicio=new Date(res.fechaInicio);
                $scope.newConcurso.fechaFin=new Date(res.fechaFin);
                $scope.CurrentFoto=res.foto;

            }).error(function (res, status) {
            $scope.newConcurso = {};
            $log.error(res);
        })
    };


    $scope.open1 = function () {
        $scope.popup1.opened = true;
    };

    $scope.open2 = function () {
        $scope.popup2.opened = true;
    };


    $scope.popup1 = {
        opened: false
    };

    $scope.popup2 = {
        opened: false
    };

    $scope.setMode = function (modo) {
        $scope.mode = modo;
        return $scope.mode;
    };

    if ($routeParams.url == undefined) {
        $scope.queryAllConcursos();
    }
});



