'use strict';

/**
 * @ngdoc directive
 * @name uiApp.directive:raceData
 * @description
 * # raceData
 */
angular.module('uiApp')
  .directive('raceData', function () {
    return {
      restrict: 'E',
      templateUrl: 'views/racedata.html',
      controller: function($scope, dataService) {

          $scope.highlighted = 'highlighted';
          $scope.refreshData = function() {
            $scope.loadingstatus = 'loading';
            dataService.getRaceResults($scope.raceid, $scope.racename, $scope.bib, $scope.starttime).then(
              function(data) {
                $scope.data = data;
                $scope.loadingstatus = '';
              }
            );

          };

          $scope.refreshData();

      },
      scope: {
      	raceid: '@',
        racename: '@',
        starttime: '@',
        bib: '=',
      }
    };
  });
