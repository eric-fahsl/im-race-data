'use strict';

/**
 * @ngdoc directive
 * @name uiApp.directive:raceDataTable
 * @description
 * # raceDataTable
 */
angular.module('uiApp')
  .directive('raceDataTable', function () {
    return {
      restrict: 'E',
      templateUrl: 'views/racedatatable.html',
      scope: {
      	sport: '@',
        splits: '='
      }
    };
  });
