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
    'ngTouch'
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
        setScopeVariables($routeParams.race, $rootScope, $scope);
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
