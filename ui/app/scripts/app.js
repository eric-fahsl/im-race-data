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
    'smart-table'
  ])
  .config(function ($routeProvider) {

    //raceData available on the global level
    
    var setScopeVariables = function(race, $rootScope, $scope) {
      $rootScope.menu = race;
      $scope.raceData = raceData[race]; // jshint ignore:line
    };

    $routeProvider.when('/:race', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope, $routeParams) {
        $rootScope.summaryData = '';
        setScopeVariables($routeParams.race, $rootScope, $scope);

        $scope.displayedCollection = [];
        $scope.rowCollection = [];

        $rootScope.removeItemFromTable = function(bib) {
          for (var i=0; i < $scope.rowCollection.length; i++ ) {
            if ($scope.rowCollection[i].bib === bib) {
              $scope.rowCollection.splice(i,1);
              // console.log('item ' + i + ' removed');
            }
          }
        };

        $rootScope.updateTableParams = function(latestUpdate) {
          // console.log('about to push to list: ', latestUpdate);
          $scope.rowCollection.push(latestUpdate);
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
