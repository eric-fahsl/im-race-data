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

    var raceData = {
      'stgeorge' : {
        'racename': 'stgeorge70.3',
        'raceid': '2147483658',
        'bibs': [
          { 'bib': '1856', 'starttime': '07:42:00' }
        ]
      },
      'texas' : {
        'racename': 'texas',
        'raceid': '2147483675',
        'bibs': [
          { 'bib': '885', 'starttime': '07:00:00' },
          { 'bib': '2640', 'starttime': '07:00:00' },
          { 'bib': '2686', 'starttime': '07:00:00' },
          { 'bib': '1922', 'starttime': '07:00:00' },
          { 'bib': '457', 'starttime': '07:00:00' }
        ]
      },
      'victoria' : {
        'racename': 'victoria70.3',
        'raceid': '',
        'bibs': [
          { 'bib': '1043', 'starttime': '06:03:00' },
          { 'bib': '95', 'starttime': '06:15:00' },
          { 'bib': '296', 'starttime': '06:12:00' },
          { 'bib': '324', 'starttime': '06:12:00' },
          { 'bib': '366', 'starttime': '06:12:00' },
          { 'bib': '522', 'starttime': '06:15:00' },
          { 'bib': '585', 'starttime': '06:15:00' },
          { 'bib': '637', 'starttime': '06:15:00' },
          { 'bib': '973', 'starttime': '06:00:00' },
          { 'bib': '1209', 'starttime': '06:06:00' },
          { 'bib': '1369', 'starttime': '06:21:00' }
          
        ]
      }
    };
    
    var setScopeVariables = function(race, $rootScope, $scope) {
      $rootScope.menu = race;
      $scope.raceData = raceData[race];
    };

    $routeProvider.when('/texas', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        // $rootScope.menu = 'texas';
        // $scope.raceData = raceData.texas;
        setScopeVariables('texas', $rootScope, $scope);
      }
    })
    .when('/stgeorge', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        setScopeVariables('stgeorge', $rootScope, $scope);
      }
    })
    .when('/victoria', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        setScopeVariables('victoria', $rootScope, $scope);
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
