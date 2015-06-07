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
    // var raceData = [
    //   {
    //     name: 'texas'
    //   },
    //   {
    //     name: 'stgeorge'
    //   },
    //   {
    //     name: 'victoria'
    //   }
    // ];
    // console.log(raceData);

    // for(var i=0; i<raceData.length; i++) {
    //   var race = raceData[i];
    //   $routeProvider.when('/' + race.name, {
    //     templateUrl: 'views/' + race.name + '.html',
    //     controller: function($rootScope, $scope) {
    //       $rootScope.menu = race.name;
    //       $scope.ericvalue = race.name;
    //     }
    //   });
    // }

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
          { 'bib': '885', 'starttime': '07:00:00' },
          { 'bib': '2640', 'starttime': '07:00:00' },
          { 'bib': '2686', 'starttime': '07:00:00' },
          { 'bib': '1922', 'starttime': '07:00:00' },
          { 'bib': '457', 'starttime': '07:00:00' }
        ]
      }
    };
      

    $routeProvider.when('/texas', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        $rootScope.menu = 'texas';
        $scope.raceData = raceData.texas;
      }
    })
    .when('/stgeorge', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        $rootScope.menu = 'stgeorge';
        $scope.raceData = raceData.stgeorge;
      }
    })
    .when('/victoria', {
      templateUrl: 'views/race-generic.html',
      controller: function($rootScope, $scope) {
        $rootScope.menu = 'victoria';
        $scope.raceData = raceData.stgeorge;
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
