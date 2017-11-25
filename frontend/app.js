var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);

var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Destination', function($resource) {
    return $resource('http://localhost:5000/api/v1/destination/:id', {id: '@id'}, {
        get: { method: 'GET' },
    });
})
.factory('Destinations', function($resource) {
    return $resource('http://localhost:5000/api/v1/destination', {}, {
        query: { method: 'GET', isArray: true },
    });
})
.factory('Country', function($resource) {
    return $resource('http://localhost:5000/api/v1/countries/:id', {id: '@id'}, {
        get: { method: 'GET' }
    });
})
.factory('Countries', function($resource) {
    return $resource('http://localhost:5000/api/v1/countries', {}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Search', function($resource) {
    return $resource('http://localhost:5000/api/v1/search', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Recommend', function($resource) {
    return $resource('http://localhost:5000/api/v1/recommend/:id', {id: '@id'}, {
        query: { method: 'GET', isArray: false }
    });
});

myApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'pages/main.html',
        controller: 'mainController'
    })
    // .when('/newBeer', {
    //     templateUrl: 'pages/beer_new.html',
    //     controller: 'newBeerController'
    // })
    .when('/countries', {
        templateUrl: 'pages/countries.html',
        controller: 'countryListController'
    })
    .when('/destination/:id', {
        templateUrl: 'pages/destination.html',
        controller: 'destinationController'
    })
});

// myApp.filter('filterStyles', function() {
//   return function(input) {
//     var output = new Array();
//     for (i=0; i<input.length; i++) {
//         if (input[i].checked == true) {
//             output.push(input[i].name);
//         }
//     }
//     return output;
//   }
// });

myApp.controller(
    'mainController',
    function ($scope, Search) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.results = Search.query({q: q});    
            }
        };
    }
);

// myApp.controller(
//     'newBeerController',
//     function ($scope, Styles, Beers, $location, $timeout, $filter) {
//         $scope.styles = Styles.query();
//         $scope.insertBeer = function () {
//             $scope.beer.styles = $filter('filterStyles')($scope.styles);
//             Beers.create($scope.beer);
//             $timeout(function (){
//                 $location.path('/beers').search({'created': $scope.beer.name});    
//             }, 500);
//         };
//         $scope.cancel = function() {
//             $location.path('/beers');
//         };
//     }
    
// );

myApp.controller(
    'countryListController',
    function ($scope, Countries) {
        // if ($location.search().hasOwnProperty('created')) {
        //     $scope.created = $location.search()['created'];
        // }
        // if ($location.search().hasOwnProperty('deleted')) {
        //     $scope.deleted = $location.search()['deleted'];
        // }
        // $scope.deleteBeer = function(beer_id) {
        //     var deleted = Beer.delete({id: beer_id});
        //     $timeout(function(){
        //         $location.path('/beers').search({'deleted': 1})
        //     }, 500);
        //     //$scope.beers = Beers.query();
        // };
        $scope.countries = Countries.query();
    }
);

myApp.controller(
    'destinationController', ['$scope', 'Destination', 'Recommend', '$routeParams',
    function ($scope, Destination, Recommend, $routeParams) {
        $scope.result = Destination.get({id: $routeParams.id});

        var recommend_result = Recommend.query({id: $routeParams.id})
        $scope.nodes = new vis.DataSet();
        $scope.edges = new vis.DataSet();
        $scope.network_data = {
            nodes: $scope.nodes,
            edges: $scope.edges
        };
        $scope.network_options = {
            height: '800px',
            width: '800px',
            interaction: {
                zoomView: false
            }
        };
        $scope.onNodeSelect = function(properties) {
            // var selected = $scope.task_nodes.get(properties.nodes[0]);
            // console.log(selected);
        };
        recommend_result.$promise.then(function(d) {
            $scope.nodes.add(recommend_result.nodes)
            $scope.edges.add(recommend_result.edges)
        })
    }
]);

myApp.directive('visNetwork', function() {
    return {
        restrict: 'E',
        require: '^ngModel',
        scope: {
            ngModel: '=',
            onSelect: '&',
            options: '='
        },
        link: function($scope, $element, $attrs, ngModel) {
            var network = new vis.Network($element[0], $scope.ngModel, $scope.options || {});

            var onSelect = $scope.onSelect() || function(prop) {};
            network.on('select', function(properties) {
                onSelect(properties);
            });

        }

    }
});

