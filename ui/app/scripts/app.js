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
        'raceid': '2147483756',
        'bibs': [
          { 'bib':'973', 'starttime':'06:00:00'},
          { 'bib':'1043', 'starttime':'06:03:00'},
          { 'bib':'1021', 'starttime':'06:03:00'},
          { 'bib':'1209', 'starttime':'06:06:00'},
          { 'bib':'366', 'starttime':'06:09:00'},
          { 'bib':'419', 'starttime':'06:09:00'},
          { 'bib':'296', 'starttime':'06:12:00'},
          { 'bib':'324', 'starttime':'06:12:00'},
          { 'bib':'95', 'starttime':'06:15:00'},
          { 'bib':'585', 'starttime':'06:15:00'},
          { 'bib':'1270', 'starttime':'06:18:00'},
          { 'bib':'1315', 'starttime':'06:18:00'},
          { 'bib':'1369', 'starttime':'06:21:00'},
          { 'bib':'657', 'starttime':'06:24:00'}          
        ]
      },
      'cda' : {
        'racename': 'cda',
        'raceid': '2147483690',
        'bibs': [
          { 'bib':'1690', 'starttime':'05:45:00'},
          { 'bib':'773', 'starttime':'05:45:00'},
          { 'bib':'1780', 'starttime':'05:45:00'},
          { 'bib':'1786', 'starttime':'05:45:00'},
          { 'bib':'2012', 'starttime':'05:45:00'},
          { 'bib':'1358', 'starttime':'05:45:00'},
          { 'bib':'1995', 'starttime':'05:45:00'},
          { 'bib':'2021', 'starttime':'05:45:00'}
        ]
      }
    };
    
    var setScopeVariables = function(race, $rootScope, $scope) {
      $rootScope.menu = race;
      $scope.raceData = raceData[race];
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
