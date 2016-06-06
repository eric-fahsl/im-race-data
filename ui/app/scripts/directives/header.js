'use strict';

/**
 * @ngdoc directive
 * @name uiApp.directive:raceDataTable
 * @description
 * # raceDataTable
 */
angular.module('uiApp')
  .directive('header', function () {
    return {
      restrict: 'E',
      templateUrl: 'views/header.html',
      controller: function($scope) {
        var races = [];
        for (var i in window.raceData) {
          races.push(i);
        }
        $scope.races = races;
      }
    };
  });
