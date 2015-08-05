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
      controller: function($scope, $rootScope, dataService) {
          if (!$rootScope.summaryData) {
            $rootScope.summaryData = {};
          }
          $rootScope.testData = 'eric';
          $scope.highlighted = 'highlighted';
          $scope.refreshData = function() {
            $scope.loadingstatus = 'loading';
            dataService.getRaceResults($scope.raceid, $scope.racename, $scope.bib, $scope.starttime).then(
              function(data) {
                $scope.data = data;
                $rootScope.summaryData[data.bib] = data.lastNextSplit;
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
