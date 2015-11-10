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
          // if (!$rootScope.summaryData) {
          //   $rootScope.summaryData = {};
          // }

          // $rootScope.summaryData[$scope.bib] = $scope.bib;

          $scope.highlighted = 'highlighted';
          $scope.refreshData = function() {
            //Remove item from the summary table            
            $rootScope.removeItemFromTable($scope.bib);
            $scope.loadingstatus = 'loading';
            dataService.getRaceResults($scope.raceid, $scope.racename, $scope.bib, $scope.starttime).then(
              function(data) {
                $scope.data = data;
                $scope.loadingstatus = '';
                                
                var latestUpdate = {
                    bib: data.bib,
                    totalDistance: data.lastNextSplit.totalDistance,
                    name: data.name,
                    currentSport: data.lastNextSplit.previous.sport,
                    nextCheckPointLoc: data.lastNextSplit.next.totalDistance, 
                    nextSport: data.lastNextSplit.next.sport,
                    nextCheckPointRaceTime: data.lastNextSplit.next.estimatedRaceTime,
                    doneCheck: data.lastNextSplit.complete
                };

                if (data.lastNextSplit.previous) {
                  latestUpdate.lastCheckPointLoc = data.lastNextSplit.previous.totalDistance; 
                  latestUpdate.lastCheckPointRaceTime = data.lastNextSplit.previous.raceTime;                                     
                }

                $rootScope.updateTableParams(latestUpdate);

              }
            );

          };

          $scope.refreshData();
          // console.log($rootScope.summaryData);

      },
      scope: {
      	raceid: '@',
        racename: '@',
        starttime: '@',
        bib: '='
      }
    };
  });
