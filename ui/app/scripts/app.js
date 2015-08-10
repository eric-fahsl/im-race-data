'use strict';

/**
 * @ngdoc overview
 * @name ngTempApp
 * @description
 * # ngTempApp
 *
 * Main module of the application.
 */
angular
  .module('uiApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ngTable'
  ])
  .config(function ($routeProvider) {

    //raceData available on the global level
    
    var setScopeVariables = function(race, $rootScope, $scope) {
      $rootScope.menu = race;
      $scope.raceData = raceData[race]; // jshint ignore:line
    };

    $routeProvider.when('/:race', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope, $routeParams, ngTableParams, $filter) {
        $rootScope.summaryData = '';
        setScopeVariables($routeParams.race, $rootScope, $scope);

        // var data = [{name: 'Moroni', age: 50},
        //     {name: 'Tiancum', age: 43},
        //     {name: 'Jacob', age: 27},
        //     {name: 'Nephi', age: 29},
        //     {name: 'Enos', age: 34},
        //     {name: 'Tiancum', age: 43},
        //     {name: 'Jacob', age: 27},
        //     {name: 'Nephi', age: 29},
        //     {name: 'Enos', age: 34},
        //     {name: 'Tiancum', age: 43},
        //     {name: 'Jacob', age: 27},
        //     {name: 'Nephi', age: 29},
        //     {name: 'Enos', age: 34},
        //     {name: 'Tiancum', age: 43},
        //     {name: 'Jacob', age: 27},
        //     {name: 'Nephi', age: 29},
        //     {name: 'Enos', age: 34}];

        $rootScope.tableData = [
          // {name: 'Name', lastCheckPointLoc: 'lastCheckPoint', lastCheckPointRaceTime: 'lastCheckPointTime', 
          //   nextCheckPointLoc: 'nextCheckPointLoc', nextCheckPointRaceTime: 'nextCheckPointRaceTime'},
          //   {name: 'Name2', lastCheckPointLoc: 'lastCheckPoint2', lastCheckPointRaceTime: 'lastCheckPointTime', 
          //   nextCheckPointLoc: 'nextCheckPointLoc', nextCheckPointRaceTime: 'nextCheckPointRaceTime'}
          ];

        $rootScope.updateTableParams = function(latestUpdate) {
          
          //check if the entry is already included
          var found = false;
          // for (var i=0; i<$rootScope.tableData.length; i++) {
          //   if ($rootScope.tableData[i].bib === latestUpdate.bib)
          //     found = true;
          //     $rootScope.tableData[i] = latestUpdate;
          // }
          // for (var i in $rootScope.tableData) {
            
          // }
          if (!found) {
            $rootScope.tableData.push(latestUpdate);
          }

          //render the table
          $scope.tableParams = new ngTableParams({ // jshint ignore:line
              page: 1,            // show first page 
              count: 100,           
              sorting: {
                  lastCheckPointLoc: 'desc',
                  name: 'asc'     // initial sorting
              }
              }, {
                  total: $rootScope.tableData.length, // length of data
                  getData: function($defer, params) {
                      // use build-in angular filter
                      var orderedData = params.sorting() ?
                              $filter('orderBy')($rootScope.tableData, params.orderBy()) :
                              $rootScope.tableData;

                      $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
              });
          };
      }
    });
        
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html'
      })
      .otherwise({
        redirectTo: '/'
      });
    
  });
